import os
from datetime import date, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings

from .models import Phim, TheLoai, Phong, SuatChieu, HoaDon, CinemaUser


# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────

def get_current_user(request):
    user_id = request.session.get('user_id')
    if user_id:
        try:
            return CinemaUser.objects.get(pk=user_id)
        except CinemaUser.DoesNotExist:
            pass
    return None


# ─────────────────────────────────────────────
#  CLIENT VIEWS
# ─────────────────────────────────────────────

def index_view(request):
    today = date.today()
    now_playing = Phim.objects.filter(NgayKhoiChieu__lte=today).select_related('MaTL').order_by('-NgayKhoiChieu')[:10]
    coming_soon = Phim.objects.filter(NgayKhoiChieu__gt=today).select_related('MaTL').order_by('NgayKhoiChieu')[:10]
    return render(request, 'client/index.html', {
        'now_playing': now_playing,
        'coming_soon': coming_soon,
        'current_user': get_current_user(request),
    })


def coming_view(request):
    today = date.today()
    coming_movies = Phim.objects.filter(
        NgayKhoiChieu__gt=today
    ).select_related('MaTL').order_by('NgayKhoiChieu')
    return render(request, 'client/coming.html', {
        'coming_movies': coming_movies,
        'current_user': get_current_user(request),
    })


def newsletter_view(request):
    # Bản tin mẫu (mock data - có thể thay bằng DB sau này)
    recent_newsletters = [
        {
            'date': 'T4/2026',
            'title': '🔥 Top 10 phim bom tấn tháng 4/2026',
            'desc': 'Điểm lại những bộ phim hot nhất tháng 4 và lịch chiếu sắp tới',
        },
        {
            'date': 'T3/2026',
            'title': '🎬 Phim Marvel mới & Ưu đãi vé tháng 3',
            'desc': 'Cập nhật về các siêu phẩm Marvel và chương trình giảm giá hấp dẫn',
        },
        {
            'date': 'T2/2026',
            'title': '🌟 Review: 5 phim không thể bỏ qua trong tháng 2',
            'desc': 'Những bộ phim được đánh giá cao nhất bởi chuyên gia điện ảnh',
        },
    ]
    return render(request, 'client/newsletter.html', {
        'recent_newsletters': recent_newsletters,
        'current_user': get_current_user(request),
    })


def movie_list_view(request):
    from collections import OrderedDict
    # Lọc theo tên thể loại, giống PHP gốc $_GET['filter']
    filter_name = request.GET.get('filter', '').strip()
    genres = TheLoai.objects.all()

    # Lấy phim, lọc nếu có
    movies_qs = Phim.objects.select_related('MaTL').order_by('-NgayKhoiChieu')
    if filter_name:
        movies_qs = movies_qs.filter(MaTL__TenTL=filter_name)

    # Nhóm theo thể loại
    grouped = OrderedDict()
    for m in movies_qs:
        gname = m.MaTL.TenTL if m.MaTL else 'Khác'
        grouped.setdefault(gname, []).append(m)
    genres_with_movies = [{'genre_name': k, 'movies': v} for k, v in grouped.items()]

    return render(request, 'client/movies.html', {
        'genres_with_movies': genres_with_movies,
        'genres': genres,
        'filter_name': filter_name,
        'current_user': get_current_user(request),
    })



def movie_detail_view(request, movie_id):
    today = date.today()
    movie = get_object_or_404(Phim.objects.select_related('MaTL'), pk=movie_id)

    related_movies = []
    if movie.MaTL:
        related_movies = list(Phim.objects.filter(MaTL=movie.MaTL).exclude(pk=movie_id).order_by('?')[:4])

    available_dates = list(
        SuatChieu.objects.filter(MaPhim=movie)
        .values_list('NgayChieu', flat=True).distinct().order_by('NgayChieu')
    )

    first_available = available_dates[0] if available_dates else today
    selected_date_str = request.GET.get('date', str(first_available))
    selected_room_id = request.GET.get('room', '')
    selected_time = request.GET.get('time', '')

    rooms_with_shows = list(
        SuatChieu.objects.filter(MaPhim=movie, NgayChieu=selected_date_str)
        .values_list('MaPhong_id', flat=True).distinct()
    )

    if not selected_room_id or (selected_room_id.isdigit() and int(selected_room_id) not in rooms_with_shows):
        selected_room_id = str(rooms_with_shows[0]) if rooms_with_shows else ''

    selected_room_name = ''
    if selected_room_id:
        try:
            p = Phong.objects.get(pk=selected_room_id)
            selected_room_name = p.TenPhong
        except Phong.DoesNotExist:
            pass

    showtimes = []
    if selected_room_id:
        showtimes = list(
            SuatChieu.objects.filter(
                MaPhim=movie, MaPhong_id=selected_room_id, NgayChieu=selected_date_str
            ).values_list('GioBatDau', flat=True).order_by('GioBatDau')
        )

    all_rooms = list(Phong.objects.all())

    # Duyệt 7 ngày từ ngày có suất chiếu sớm nhất (hoặc hôm nay)
    weekday_names = ['Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6', 'Thứ 7', 'Chủ Nhật']
    week_days = []
    for i in range(7):
        d = first_available + timedelta(days=i)
        is_available = d in available_dates
        week_days.append({
            'date': d, 
            'label': weekday_names[d.weekday()],
            'is_available': is_available, 
            'is_selected': str(d) == selected_date_str,
        })

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    part = request.GET.get('part', '')

    if is_ajax:
        if part == 'rooms':
            return render(request, 'client/partials/rooms_partial.html', {
                'all_rooms': all_rooms, 'rooms_with_shows': rooms_with_shows, 'selected_room_id': selected_room_id,
            })
        elif part == 'times':
            return render(request, 'client/partials/times_partial.html', {
                'showtimes': showtimes, 'selected_time': selected_time,
            })
        elif part == 'booking-info':
            return render(request, 'client/partials/booking_info_partial.html', {
                'movie': movie, 'selected_date': selected_date_str,
                'selected_room_name': selected_room_name, 'selected_room_id': selected_room_id,
                'selected_time': selected_time,
            })

    return render(request, 'client/detail.html', {
        'movie': movie, 'related_movies': related_movies,
        'available_dates': available_dates, 'week_days': week_days,
        'all_rooms': all_rooms, 'rooms_with_shows': rooms_with_shows,
        'selected_date': selected_date_str, 'selected_room_id': selected_room_id,
        'selected_room_name': selected_room_name, 'selected_time': selected_time,
        'showtimes': showtimes, 'current_user': get_current_user(request),
    })


def chair_view(request):
    movie_id = request.GET.get('id')
    room_id = request.GET.get('room')
    date_str = request.GET.get('date')
    time_str = request.GET.get('time')

    movie = get_object_or_404(Phim, pk=movie_id)
    room = get_object_or_404(Phong, pk=room_id)
    showtime = SuatChieu.objects.filter(
        MaPhim=movie, MaPhong=room, NgayChieu=date_str, GioBatDau=time_str
    ).first()

    booked_seats = []
    if showtime:
        for bill in HoaDon.objects.filter(MaSuatChieu=showtime):
            if bill.Ghe:
                booked_seats.extend([s.strip() for s in bill.Ghe.split(',')])

    rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    cols = list(range(1, 11))

    # Build seat map với trạng thái đã đặt
    seat_map = []
    for row in rows:
        row_seats = []
        for col in cols:
            sid = f"{row}{col}"
            row_seats.append({
                'id': sid,
                'label': col,
                'booked': sid in booked_seats,
            })
        seat_map.append({'row': row, 'seats': row_seats})

    return render(request, 'client/chair.html', {
        'movie': movie, 'room': room, 'showtime': showtime,
        'date': date_str, 'time': time_str, 'booked_seats': booked_seats,
        'rows': rows, 'cols': cols, 'seat_map': seat_map,
        'current_user': get_current_user(request),
    })


def payment_view(request):
    if request.method == 'POST':
        movie_id = request.POST.get('movie_id')
        room_id = request.POST.get('room_id')
        date_str = request.POST.get('date')
        time_str = request.POST.get('time')
        seats = request.POST.get('seats', '')
        seat_count = int(request.POST.get('seat_count', 0))

        movie = get_object_or_404(Phim, pk=movie_id)
        room = get_object_or_404(Phong, pk=room_id)
        showtime = get_object_or_404(SuatChieu, MaPhim=movie, MaPhong=room, NgayChieu=date_str, GioBatDau=time_str)
        total = seat_count * int(showtime.GiaVe)

        request.session['booking'] = {
            'movie_id': movie_id, 'room_id': room_id, 'date': date_str,
            'time': time_str, 'seats': seats, 'seat_count': seat_count,
            'showtime_id': showtime.MaSuatChieu, 'gia_ve': int(showtime.GiaVe), 'total': total,
        }

        return render(request, 'client/payment.html', {
            'movie': movie, 'room': room, 'showtime': showtime,
            'seats': seats, 'seat_count': seat_count, 'total': total,
            'date': date_str, 'time': time_str, 'current_user': get_current_user(request),
        })
    return redirect('index')


def confirm_view(request):
    if request.method == 'POST':
        booking = request.session.get('booking')
        if not booking:
            return redirect('index')

        payment_method = request.POST.get('payment_method', 'tien_mat')
        payment_labels = {
            'momo': 'MoMo',
            'vnpay': 'VNPay',
            'card': 'Thẻ ngân hàng',
            'tien_mat': 'Tiền mặt',
        }

        showtime = get_object_or_404(SuatChieu, pk=booking['showtime_id'])
        bill = HoaDon.objects.create(
            MaSuatChieu=showtime, Ghe=booking['seats'], SoLuong=booking['seat_count'],
            ThanhTien=booking['total'],
            guest_name=request.POST.get('guest_name', ''),
            guest_email=request.POST.get('guest_email', ''),
            guest_phone=request.POST.get('guest_phone', ''),
        )
        del request.session['booking']

        qr_data = f"HD#{bill.MaHoaDon}|PHIM:{showtime.MaPhim.TenPhim}|GHE:{bill.Ghe}|NGAY:{showtime.NgayChieu}|GIO:{showtime.GioBatDau}"

        return render(request, 'client/confirm.html', {
            'bill': bill,
            'movie': showtime.MaPhim,
            'room': showtime.MaPhong,
            'showtime': showtime,
            'payment_method': payment_labels.get(payment_method, payment_method),
            'gia_ve': booking.get('gia_ve', 0),
            'qr_data': qr_data,
            'current_user': get_current_user(request),
        })
    return redirect('index')


# ─────────────────────────────────────────────
#  AUTH VIEWS
# ─────────────────────────────────────────────

def login_view(request):
    if request.session.get('user_id'):
        return redirect('index')

    login_error = register_error = ''
    active_tab = 'login'

    if request.method == 'POST':
        action = request.POST.get('action', 'login')
        if action == 'login':
            email = request.POST.get('email', '')
            password = request.POST.get('password', '')
            try:
                user = CinemaUser.objects.get(user_email=email)
                import bcrypt
                if bcrypt.checkpw(password.encode(), user.user_password.encode()):
                    request.session['user_id'] = user.user_id
                    request.session['user_name'] = user.user_name
                    request.session['is_staff'] = bool(user.IsStaff)
                    return redirect('admin_dashboard' if user.IsStaff else 'index')
                else:
                    login_error = 'Email hoặc mật khẩu không đúng!'
            except CinemaUser.DoesNotExist:
                login_error = 'Email hoặc mật khẩu không đúng!'
            active_tab = 'login'

        elif action == 'register':
            name = request.POST.get('name', '')
            email = request.POST.get('email', '')
            password = request.POST.get('password', '')
            if CinemaUser.objects.filter(user_email=email).exists():
                register_error = 'Email này đã được sử dụng!'
                active_tab = 'register'
            else:
                import bcrypt
                hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
                user = CinemaUser.objects.create(
                    user_name=name, user_email=email,
                    user_password=hashed, user_role='customer', IsStaff=False,
                )
                request.session['user_id'] = user.user_id
                request.session['user_name'] = user.user_name
                request.session['is_staff'] = False
                return redirect('index')

    return render(request, 'client/login.html', {
        'login_error': login_error, 'register_error': register_error, 'active_tab': active_tab,
    })


def logout_view(request):
    request.session.flush()
    return redirect('index')
