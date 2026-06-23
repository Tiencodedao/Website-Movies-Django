"""
api_views.py — REST API cho Cinema Mobile App (Flutter)

Xác thực: Bearer Token (Django signing — không cần thư viện ngoài)
Response format:
  { "success": true,  "data": {...} }
  { "success": false, "error": "..." }

Endpoints:
  GET  /api/movies/                         — Danh sách phim (đang chiếu + sắp chiếu)
  GET  /api/movies/<id>/                    — Chi tiết phim
  GET  /api/movies/<id>/showtimes/?date=    — Suất chiếu theo ngày
  GET  /api/showtimes/<id>/seats/           — Sơ đồ ghế
  GET  /api/genres/                         — Danh sách thể loại
  POST /api/login/                          — Đăng nhập → trả token
  POST /api/register/                       — Đăng ký tài khoản
  GET  /api/me/                             — Thông tin user (cần token)
  POST /api/booking/                        — Đặt vé (token tùy chọn)
  GET  /api/bills/<id>/                     — Chi tiết hóa đơn
"""

import json
import bcrypt
from datetime import date

from django.core import signing
from django.core.signing import BadSignature, SignatureExpired
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Phim, TheLoai, Phong, SuatChieu, HoaDon, CinemaUser


# ═══════════════════════════════════════════════════════════════
#  TOKEN HELPERS — Dùng Django signing (không cần JWT thư viện)
# ═══════════════════════════════════════════════════════════════

_TOKEN_SALT = 'cinema-mobile-api-v1'
_TOKEN_MAX_AGE = 86400 * 7  # Token hết hạn sau 7 ngày


def _create_token(user_id: int) -> str:
    """Tạo Bearer token từ user_id."""
    return signing.dumps({'user_id': user_id}, salt=_TOKEN_SALT)


def _get_user_from_request(request):
    """Lấy CinemaUser từ header 'Authorization: Bearer <token>'. Trả None nếu lỗi."""
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return None
    token = auth_header[7:].strip()
    try:
        data = signing.loads(token, salt=_TOKEN_SALT, max_age=_TOKEN_MAX_AGE)
        return CinemaUser.objects.get(pk=data['user_id'])
    except (BadSignature, SignatureExpired, CinemaUser.DoesNotExist, KeyError):
        return None


# ═══════════════════════════════════════════════════════════════
#  RESPONSE HELPERS
# ═══════════════════════════════════════════════════════════════

def _ok(data, status=200):
    return JsonResponse({'success': True, 'data': data}, status=status)


def _err(message, status=400):
    return JsonResponse({'success': False, 'error': message}, status=status)


def _require_auth(func):
    """Decorator: endpoint bắt buộc phải có token hợp lệ."""
    def wrapper(request, *args, **kwargs):
        user = _get_user_from_request(request)
        if not user:
            return _err('Chưa đăng nhập. Vui lòng cung cấp Bearer token.', status=401)
        request.api_user = user
        return func(request, *args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


# ═══════════════════════════════════════════════════════════════
#  SERIALIZERS — Hàm chuyển model → dict (JSON)
# ═══════════════════════════════════════════════════════════════

def _serialize_movie(m: Phim) -> dict:
    return {
        'id':               m.MaPhim,
        'ten_phim':         m.TenPhim,
        'hinh':             m.Hinh,
        'trailer':          m.Trailer,
        'mo_ta':            m.MoTa,
        'thoi_luong':       m.ThoiLuong,
        'ngay_khoi_chieu':  str(m.NgayKhoiChieu) if m.NgayKhoiChieu else None,
        'the_loai':         m.MaTL.TenTL if m.MaTL else None,
        'the_loai_id':      m.MaTL.MaTL  if m.MaTL else None,
    }


def _serialize_movie_short(m: Phim) -> dict:
    """Phiên bản rút gọn dùng cho related movies, coming soon list."""
    return {
        'id':               m.MaPhim,
        'ten_phim':         m.TenPhim,
        'hinh':             m.Hinh,
        'ngay_khoi_chieu':  str(m.NgayKhoiChieu) if m.NgayKhoiChieu else None,
        'the_loai':         m.MaTL.TenTL if m.MaTL else None,
    }


# ═══════════════════════════════════════════════════════════════
#  MOVIES
# ═══════════════════════════════════════════════════════════════

def api_movies(request):
    """
    GET /api/movies/
    Trả về danh sách phim đang chiếu và sắp chiếu.
    Query params tùy chọn:
      ?genre=<ten_the_loai>  — lọc theo thể loại
    """
    today = date.today()
    genre_filter = request.GET.get('genre', '').strip()

    qs = Phim.objects.select_related('MaTL').order_by('-NgayKhoiChieu')
    if genre_filter:
        qs = qs.filter(MaTL__TenTL=genre_filter)

    now_playing = [_serialize_movie_short(m) for m in qs if m.NgayKhoiChieu and m.NgayKhoiChieu <= today]
    coming_soon = [_serialize_movie_short(m) for m in qs if m.NgayKhoiChieu and m.NgayKhoiChieu > today]

    return _ok({
        'now_playing': now_playing,
        'coming_soon': coming_soon,
        'total': len(now_playing) + len(coming_soon),
    })


def api_movie_detail(request, movie_id):
    """
    GET /api/movies/<movie_id>/
    Chi tiết phim + danh sách ngày có suất chiếu + phim liên quan.
    """
    try:
        movie = Phim.objects.select_related('MaTL').get(pk=movie_id)
    except Phim.DoesNotExist:
        return _err('Phim không tồn tại', status=404)

    # Phim liên quan cùng thể loại
    related = []
    if movie.MaTL:
        related = [
            _serialize_movie_short(m)
            for m in Phim.objects.filter(MaTL=movie.MaTL)
                                 .exclude(pk=movie_id)
                                 .order_by('?')[:4]
        ]

    # Các ngày có suất chiếu
    available_dates = list(
        SuatChieu.objects.filter(MaPhim=movie)
                         .values_list('NgayChieu', flat=True)
                         .distinct()
                         .order_by('NgayChieu')
    )

    return _ok({
        'movie':           _serialize_movie(movie),
        'related_movies':  related,
        'available_dates': [str(d) for d in available_dates],
    })


def api_showtimes(request, movie_id):
    """
    GET /api/movies/<movie_id>/showtimes/?date=YYYY-MM-DD
    Trả về danh sách phòng chiếu và giờ chiếu trong ngày đó.
    Mặc định là ngày hôm nay nếu không truyền date.
    """
    date_str = request.GET.get('date', str(date.today()))

    try:
        movie = Phim.objects.get(pk=movie_id)
    except Phim.DoesNotExist:
        return _err('Phim không tồn tại', status=404)

    showtimes_qs = (
        SuatChieu.objects
                 .filter(MaPhim=movie, NgayChieu=date_str)
                 .select_related('MaPhong')
                 .order_by('MaPhong', 'GioBatDau')
    )

    # Nhóm theo phòng chiếu
    rooms: dict = {}
    for st in showtimes_qs:
        rid = st.MaPhong.MaPhong
        if rid not in rooms:
            rooms[rid] = {
                'room_id':   rid,
                'ten_phong': st.MaPhong.TenPhong,
                'showtimes': [],
            }
        rooms[rid]['showtimes'].append({
            'showtime_id':  st.MaSuatChieu,
            'gio_bat_dau':  str(st.GioBatDau)[:5],   # "HH:MM"
            'gia_ve':       int(st.GiaVe),
        })

    return _ok({
        'movie_id': movie_id,
        'date':     date_str,
        'rooms':    list(rooms.values()),
    })


# ═══════════════════════════════════════════════════════════════
#  SEATS
# ═══════════════════════════════════════════════════════════════

def api_seats(request, showtime_id):
    """
    GET /api/showtimes/<showtime_id>/seats/
    Trả về sơ đồ ghế 8×10 với trạng thái đã đặt / còn trống.
    """
    try:
        showtime = SuatChieu.objects.select_related('MaPhim', 'MaPhong').get(pk=showtime_id)
    except SuatChieu.DoesNotExist:
        return _err('Suất chiếu không tồn tại', status=404)

    # Tổng hợp ghế đã đặt từ tất cả hóa đơn của suất chiếu này
    booked_seats: list[str] = []
    for bill in HoaDon.objects.filter(MaSuatChieu=showtime):
        if bill.Ghe:
            booked_seats.extend(s.strip() for s in bill.Ghe.split(','))

    # Build seat map 8 hàng × 10 cột
    rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    seat_map = [
        {
            'id':     f'{row}{col}',
            'row':    row,
            'col':    col,
            'booked': f'{row}{col}' in booked_seats,
        }
        for row in rows
        for col in range(1, 11)
    ]

    return _ok({
        'showtime_id':  showtime_id,
        'movie':        showtime.MaPhim.TenPhim,
        'room':         showtime.MaPhong.TenPhong,
        'date':         str(showtime.NgayChieu),
        'time':         str(showtime.GioBatDau)[:5],
        'gia_ve':       int(showtime.GiaVe),
        'booked_seats': booked_seats,
        'seat_map':     seat_map,
        'total_seats':  len(rows) * 10,
        'available':    len(rows) * 10 - len(booked_seats),
    })


# ═══════════════════════════════════════════════════════════════
#  GENRES
# ═══════════════════════════════════════════════════════════════

def api_genres(request):
    """GET /api/genres/ — Danh sách tất cả thể loại phim."""
    genres = TheLoai.objects.all().order_by('TenTL')
    return _ok([{'id': g.MaTL, 'ten': g.TenTL} for g in genres])


# ═══════════════════════════════════════════════════════════════
#  AUTH
# ═══════════════════════════════════════════════════════════════

@csrf_exempt
@require_http_methods(['POST'])
def api_login(request):
    """
    POST /api/login/
    Body JSON: { "email": "...", "password": "..." }
    Trả về: { "token": "...", "user": {...} }
    """
    try:
        body = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return _err('Request body không hợp lệ (cần JSON)', status=400)

    email    = body.get('email', '').strip()
    password = body.get('password', '')

    if not email or not password:
        return _err('Vui lòng nhập email và mật khẩu', status=400)

    try:
        user = CinemaUser.objects.get(user_email=email)
        if bcrypt.checkpw(password.encode(), user.user_password.encode()):
            token = _create_token(user.user_id)
            return _ok({
                'token': token,
                'user': {
                    'id':       user.user_id,
                    'name':     user.user_name,
                    'email':    user.user_email,
                    'is_staff': bool(user.IsStaff),
                },
            })
        return _err('Email hoặc mật khẩu không đúng', status=401)
    except CinemaUser.DoesNotExist:
        return _err('Email hoặc mật khẩu không đúng', status=401)


@csrf_exempt
@require_http_methods(['POST'])
def api_register(request):
    """
    POST /api/register/
    Body JSON: { "name": "...", "email": "...", "password": "..." }
    Trả về token ngay sau khi đăng ký thành công.
    """
    try:
        body = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return _err('Request body không hợp lệ (cần JSON)', status=400)

    name     = body.get('name', '').strip()
    email    = body.get('email', '').strip()
    password = body.get('password', '')

    if not name or not email or not password:
        return _err('Vui lòng nhập đầy đủ họ tên, email và mật khẩu', status=400)

    if len(password) < 6:
        return _err('Mật khẩu phải có ít nhất 6 ký tự', status=400)

    if CinemaUser.objects.filter(user_email=email).exists():
        return _err('Email này đã được sử dụng', status=409)

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    user = CinemaUser.objects.create(
        user_name=name,
        user_email=email,
        user_password=hashed,
        user_role='customer',
        IsStaff=False,
    )
    token = _create_token(user.user_id)
    return _ok({
        'token': token,
        'user': {
            'id':       user.user_id,
            'name':     user.user_name,
            'email':    user.user_email,
            'is_staff': False,
        },
    }, status=201)


@_require_auth
def api_me(request):
    """
    GET /api/me/
    Header: Authorization: Bearer <token>
    Trả về thông tin tài khoản hiện tại.
    """
    user = request.api_user
    return _ok({
        'id':       user.user_id,
        'name':     user.user_name,
        'email':    user.user_email,
        'role':     user.user_role,
        'is_staff': bool(user.IsStaff),
    })


# ═══════════════════════════════════════════════════════════════
#  BOOKING
# ═══════════════════════════════════════════════════════════════

@csrf_exempt
@require_http_methods(['POST'])
def api_booking(request):
    """
    POST /api/booking/
    Header (tùy chọn): Authorization: Bearer <token>
    Body JSON:
      {
        "showtime_id": 1,
        "seats": "A1,A2,B3",
        "seat_count": 3,
        "guest_name": "Nguyen Van A",
        "guest_email": "a@gmail.com",
        "guest_phone": "0901234567"
      }
    Nếu có token thì tự động điền guest_name/email từ tài khoản.
    """
    try:
        body = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return _err('Request body không hợp lệ (cần JSON)', status=400)

    showtime_id = body.get('showtime_id')
    seats       = body.get('seats', '').strip()
    seat_count  = body.get('seat_count', 0)
    guest_name  = body.get('guest_name', '').strip()
    guest_email = body.get('guest_email', '').strip()
    guest_phone = body.get('guest_phone', '').strip()

    # Nếu đã đăng nhập → tự điền thông tin
    user = _get_user_from_request(request)
    if user:
        guest_name  = guest_name  or user.user_name
        guest_email = guest_email or user.user_email

    # Validate
    if not showtime_id:
        return _err('Thiếu showtime_id', status=400)
    if not seats:
        return _err('Chưa chọn ghế', status=400)
    if not seat_count or int(seat_count) <= 0:
        return _err('Số lượng ghế không hợp lệ', status=400)
    if not guest_name or not guest_email or not guest_phone:
        return _err('Vui lòng nhập đầy đủ họ tên, email và số điện thoại', status=400)

    try:
        showtime = SuatChieu.objects.select_related('MaPhim', 'MaPhong').get(pk=showtime_id)
    except SuatChieu.DoesNotExist:
        return _err('Suất chiếu không tồn tại', status=404)

    # Kiểm tra xung đột ghế
    booked: list[str] = []
    for bill in HoaDon.objects.filter(MaSuatChieu=showtime):
        if bill.Ghe:
            booked.extend(s.strip() for s in bill.Ghe.split(','))

    requested = [s.strip() for s in seats.split(',')]
    conflicts  = [s for s in requested if s in booked]
    if conflicts:
        return _err(f'Ghế đã bị đặt bởi người khác: {", ".join(conflicts)}', status=409)

    total = int(seat_count) * int(showtime.GiaVe)
    bill  = HoaDon.objects.create(
        MaSuatChieu = showtime,
        Ghe         = seats,
        SoLuong     = int(seat_count),
        ThanhTien   = total,
        guest_name  = guest_name,
        guest_email = guest_email,
        guest_phone = guest_phone,
    )

    qr_data = (
        f"HD#{bill.MaHoaDon}"
        f"|PHIM:{showtime.MaPhim.TenPhim}"
        f"|GHE:{bill.Ghe}"
        f"|NGAY:{showtime.NgayChieu}"
        f"|GIO:{showtime.GioBatDau}"
    )

    return _ok({
        'bill_id':     bill.MaHoaDon,
        'movie':       showtime.MaPhim.TenPhim,
        'movie_img':   showtime.MaPhim.Hinh,
        'room':        showtime.MaPhong.TenPhong,
        'date':        str(showtime.NgayChieu),
        'time':        str(showtime.GioBatDau)[:5],
        'seats':       seats,
        'seat_count':  int(seat_count),
        'gia_ve':      int(showtime.GiaVe),
        'total':       total,
        'guest_name':  guest_name,
        'guest_email': guest_email,
        'guest_phone': guest_phone,
        'qr_data':     qr_data,
    }, status=201)


def api_bill_detail(request, bill_id):
    """
    GET /api/bills/<bill_id>/
    Chi tiết hóa đơn + thông tin để render QR code.
    """
    try:
        bill = HoaDon.objects.select_related(
            'MaSuatChieu',
            'MaSuatChieu__MaPhim',
            'MaSuatChieu__MaPhong',
        ).get(pk=bill_id)
    except HoaDon.DoesNotExist:
        return _err('Hóa đơn không tồn tại', status=404)

    st = bill.MaSuatChieu
    qr_data = (
        f"HD#{bill.MaHoaDon}"
        f"|PHIM:{st.MaPhim.TenPhim}"
        f"|GHE:{bill.Ghe}"
        f"|NGAY:{st.NgayChieu}"
        f"|GIO:{st.GioBatDau}"
    )

    return _ok({
        'bill_id':     bill.MaHoaDon,
        'movie':       st.MaPhim.TenPhim,
        'movie_img':   st.MaPhim.Hinh,
        'room':        st.MaPhong.TenPhong,
        'date':        str(st.NgayChieu),
        'time':        str(st.GioBatDau)[:5],
        'seats':       bill.Ghe,
        'seat_count':  bill.SoLuong,
        'gia_ve':      int(st.GiaVe),
        'total':       int(bill.ThanhTien),
        'guest_name':  bill.guest_name,
        'guest_email': bill.guest_email,
        'guest_phone': bill.guest_phone,
        'qr_data':     qr_data,
    })
