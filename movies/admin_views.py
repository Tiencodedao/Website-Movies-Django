import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Sum, Q
from django.conf import settings

from .models import Phim, TheLoai, Phong, SuatChieu, HoaDon, CinemaUser
from .forms import PhimForm, PhongForm, SuatChieuForm, HoaDonForm, CinemaUserForm, TheLoaiForm


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('login')
        if not request.session.get('is_staff'):
            return redirect('index')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


@admin_required
def admin_dashboard(request):
    from datetime import date
    today = date.today()
    total_movies = Phim.objects.count()
    total_bills = HoaDon.objects.count()
    total_users = CinemaUser.objects.count()
    total_revenue = HoaDon.objects.aggregate(total=Sum('ThanhTien'))['total'] or 0
    total_shows = SuatChieu.objects.count()

    recent_movies = Phim.objects.select_related('MaTL').order_by('-MaPhim')[:5]
    recent_bills = HoaDon.objects.select_related(
        'MaSuatChieu__MaPhim', 'MaSuatChieu__MaPhong'
    ).order_by('-MaHoaDon')[:5]
    recent_users = CinemaUser.objects.order_by('-user_id')[:5]

    return render(request, 'admin_panel/dashboard.html', {
        'total_movies': total_movies, 'total_bills': total_bills,
        'total_users': total_users, 'total_revenue': total_revenue,
        'total_shows': total_shows,
        'recent_movies': recent_movies, 'recent_bills': recent_bills,
        'recent_users': recent_users,
        'admin_name': request.session.get('user_name', 'Admin'),
        'today': today,
    })



# ── MOVIES ──────────────────────────────────────────────
@admin_required
def admin_movies(request):
    search = request.GET.get('q', '')
    qs = Phim.objects.select_related('MaTL').order_by('-MaPhim')
    if search:
        qs = qs.filter(TenPhim__icontains=search)
    paginator = Paginator(qs, 10)
    movies = paginator.get_page(request.GET.get('page', 1))
    return render(request, 'admin_panel/movies.html', {
        'movies': movies, 'search': search,
        'admin_name': request.session.get('user_name', 'Admin'),
    })


@admin_required
def admin_create_movie(request):
    form = PhimForm()
    if request.method == 'POST':
        form = PhimForm(request.POST)
        hinh_file = request.FILES.get('hinh_file')
        if form.is_valid():
            movie = form.save(commit=False)
            if hinh_file:
                upload_dir = os.path.join(settings.BASE_DIR, 'static', 'admin', 'img', 'uploads')
                os.makedirs(upload_dir, exist_ok=True)
                with open(os.path.join(upload_dir, hinh_file.name), 'wb') as f:
                    for chunk in hinh_file.chunks():
                        f.write(chunk)
                movie.Hinh = hinh_file.name
            movie.save()
            messages.success(request, 'Thêm phim thành công!')
            return redirect('admin_movies')
    return render(request, 'admin_panel/create_movie.html', {
        'form': form, 'admin_name': request.session.get('user_name', 'Admin'),
    })


@admin_required
def admin_edit_movie(request, movie_id):
    movie = get_object_or_404(Phim, pk=movie_id)
    form = PhimForm(instance=movie)
    if request.method == 'POST':
        form = PhimForm(request.POST, instance=movie)
        hinh_file = request.FILES.get('hinh_file')
        if form.is_valid():
            m = form.save(commit=False)
            if hinh_file:
                upload_dir = os.path.join(settings.BASE_DIR, 'static', 'admin', 'img', 'uploads')
                os.makedirs(upload_dir, exist_ok=True)
                with open(os.path.join(upload_dir, hinh_file.name), 'wb') as f:
                    for chunk in hinh_file.chunks():
                        f.write(chunk)
                m.Hinh = hinh_file.name
            m.save()
            messages.success(request, 'Cập nhật phim thành công!')
            return redirect('admin_movies')
    return render(request, 'admin_panel/edit_movie.html', {
        'form': form, 'movie': movie, 'admin_name': request.session.get('user_name', 'Admin'),
    })


@admin_required
def admin_delete_movie(request, movie_id):
    movie = get_object_or_404(Phim, pk=movie_id)
    if request.method == 'POST':
        movie.delete()
        messages.success(request, 'Đã xóa phim!')
        return redirect('admin_movies')
    return render(request, 'admin_panel/confirm_delete.html', {
        'item': movie, 'item_name': movie.TenPhim, 'cancel_url': 'admin_movies',
        'admin_name': request.session.get('user_name', 'Admin'),
    })


# ── ROOMS ───────────────────────────────────────────────
@admin_required
def admin_rooms(request):
    rooms = Phong.objects.all()
    return render(request, 'admin_panel/rooms.html', {
        'rooms': rooms, 'admin_name': request.session.get('user_name', 'Admin'),
    })


@admin_required
def admin_create_room(request):
    form = PhongForm()
    if request.method == 'POST':
        form = PhongForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thêm phòng chiếu thành công!')
            return redirect('admin_rooms')
    return render(request, 'admin_panel/create_room.html', {
        'form': form, 'admin_name': request.session.get('user_name', 'Admin'),
    })


@admin_required
def admin_edit_room(request, room_id):
    room = get_object_or_404(Phong, pk=room_id)
    form = PhongForm(instance=room)
    if request.method == 'POST':
        form = PhongForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cập nhật phòng thành công!')
            return redirect('admin_rooms')
    return render(request, 'admin_panel/edit_room.html', {
        'form': form, 'room': room, 'admin_name': request.session.get('user_name', 'Admin'),
    })


@admin_required
def admin_delete_room(request, room_id):
    room = get_object_or_404(Phong, pk=room_id)
    if request.method == 'POST':
        room.delete()
        messages.success(request, 'Đã xóa phòng!')
        return redirect('admin_rooms')
    return render(request, 'admin_panel/confirm_delete.html', {
        'item': room, 'item_name': room.TenPhong, 'cancel_url': 'admin_rooms',
        'admin_name': request.session.get('user_name', 'Admin'),
    })


# ── SHOWS ───────────────────────────────────────────────
@admin_required
def admin_shows(request):
    qs = SuatChieu.objects.select_related('MaPhim', 'MaPhong').order_by('-NgayChieu', 'GioBatDau')
    paginator = Paginator(qs, 10)
    shows = paginator.get_page(request.GET.get('page', 1))
    return render(request, 'admin_panel/shows.html', {
        'shows': shows, 'admin_name': request.session.get('user_name', 'Admin'),
    })


@admin_required
def admin_create_show(request):
    form = SuatChieuForm()
    if request.method == 'POST':
        form = SuatChieuForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thêm suất chiếu thành công!')
            return redirect('admin_shows')
    return render(request, 'admin_panel/create_show.html', {
        'form': form, 'admin_name': request.session.get('user_name', 'Admin'),
    })


@admin_required
def admin_edit_show(request, show_id):
    show = get_object_or_404(SuatChieu, pk=show_id)
    form = SuatChieuForm(instance=show)
    if request.method == 'POST':
        form = SuatChieuForm(request.POST, instance=show)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cập nhật suất chiếu thành công!')
            return redirect('admin_shows')
    return render(request, 'admin_panel/edit_show.html', {
        'form': form, 'show': show, 'admin_name': request.session.get('user_name', 'Admin'),
    })


@admin_required
def admin_delete_show(request, show_id):
    show = get_object_or_404(SuatChieu, pk=show_id)
    if request.method == 'POST':
        show.delete()
        messages.success(request, 'Đã xóa suất chiếu!')
        return redirect('admin_shows')
    return render(request, 'admin_panel/confirm_delete.html', {
        'item': show, 'item_name': f"{show.MaPhim.TenPhim} - {show.NgayChieu}",
        'cancel_url': 'admin_shows', 'admin_name': request.session.get('user_name', 'Admin'),
    })


# ── BILLS ───────────────────────────────────────────────
@admin_required
def admin_bills(request):
    search = request.GET.get('q', '')
    qs = HoaDon.objects.select_related('MaSuatChieu__MaPhim', 'MaSuatChieu__MaPhong').order_by('-MaHoaDon')
    if search:
        qs = qs.filter(
            Q(guest_name__icontains=search) | Q(guest_email__icontains=search) |
            Q(guest_phone__icontains=search) | Q(MaSuatChieu__MaPhim__TenPhim__icontains=search)
        )
    paginator = Paginator(qs, 10)
    bills = paginator.get_page(request.GET.get('page', 1))
    return render(request, 'admin_panel/bills.html', {
        'bills': bills, 'search': search, 'admin_name': request.session.get('user_name', 'Admin'),
    })


@admin_required
def admin_edit_bill(request, bill_id):
    bill = get_object_or_404(HoaDon, pk=bill_id)
    form = HoaDonForm(instance=bill)
    if request.method == 'POST':
        form = HoaDonForm(request.POST, instance=bill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cập nhật hóa đơn thành công!')
            return redirect('admin_bills')
    return render(request, 'admin_panel/edit_bill.html', {
        'form': form, 'bill': bill, 'admin_name': request.session.get('user_name', 'Admin'),
    })


@admin_required
def admin_delete_bill(request, bill_id):
    bill = get_object_or_404(HoaDon, pk=bill_id)
    if request.method == 'POST':
        bill.delete()
        messages.success(request, 'Đã xóa hóa đơn!')
        return redirect('admin_bills')
    return render(request, 'admin_panel/confirm_delete.html', {
        'item': bill, 'item_name': f"Hóa đơn #{bill.MaHoaDon}",
        'cancel_url': 'admin_bills', 'admin_name': request.session.get('user_name', 'Admin'),
    })


# ── USERS ───────────────────────────────────────────────
@admin_required
def admin_users(request):
    search = request.GET.get('q', '')
    qs = CinemaUser.objects.all().order_by('user_id')
    if search:
        qs = qs.filter(Q(user_name__icontains=search) | Q(user_email__icontains=search))
    paginator = Paginator(qs, 10)
    users = paginator.get_page(request.GET.get('page', 1))
    return render(request, 'admin_panel/users.html', {
        'users': users, 'search': search, 'admin_name': request.session.get('user_name', 'Admin'),
    })


@admin_required
def admin_create_user(request):
    form = CinemaUserForm()
    if request.method == 'POST':
        form = CinemaUserForm(request.POST)
        password = request.POST.get('password', '')
        if form.is_valid():
            import bcrypt
            hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            user = form.save(commit=False)
            user.user_password = hashed
            user.save()
            messages.success(request, 'Thêm tài khoản thành công!')
            return redirect('admin_users')
    return render(request, 'admin_panel/create_user.html', {
        'form': form, 'admin_name': request.session.get('user_name', 'Admin'),
    })


@admin_required
def admin_edit_user(request, user_id):
    edit_user = get_object_or_404(CinemaUser, pk=user_id)
    form = CinemaUserForm(instance=edit_user)
    if request.method == 'POST':
        form = CinemaUserForm(request.POST, instance=edit_user)
        if form.is_valid():
            user_obj = form.save(commit=False)
            new_password = request.POST.get('password', '').strip()
            if new_password:
                import bcrypt
                user_obj.user_password = bcrypt.hashpw(
                    new_password.encode(), bcrypt.gensalt()
                ).decode()
            user_obj.save()
            messages.success(request, 'Cập nhật tài khoản thành công!')
            return redirect('admin_users')
    return render(request, 'admin_panel/edit_user.html', {
        'form': form, 'edit_user': edit_user, 'admin_name': request.session.get('user_name', 'Admin'),
    })


@admin_required
def admin_delete_user(request, user_id):
    user = get_object_or_404(CinemaUser, pk=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Đã xóa tài khoản!')
        return redirect('admin_users')
    return render(request, 'admin_panel/confirm_delete.html', {
        'item': user, 'item_name': user.user_name,
        'cancel_url': 'admin_users', 'admin_name': request.session.get('user_name', 'Admin'),
    })


# ── GENRES ──────────────────────────────────────────────
@admin_required
def admin_genres(request):
    genres = TheLoai.objects.all().order_by('MaTL')
    return render(request, 'admin_panel/genres.html', {
        'genres': genres, 'admin_name': request.session.get('user_name', 'Admin'),
    })


@admin_required
def admin_create_genre(request):
    form = TheLoaiForm()
    if request.method == 'POST':
        form = TheLoaiForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thêm thể loại thành công!')
            return redirect('admin_genres')
    return render(request, 'admin_panel/create_genre.html', {
        'form': form, 'admin_name': request.session.get('user_name', 'Admin'),
    })


@admin_required
def admin_edit_genre(request, genre_id):
    genre = get_object_or_404(TheLoai, pk=genre_id)
    form = TheLoaiForm(instance=genre)
    if request.method == 'POST':
        form = TheLoaiForm(request.POST, instance=genre)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cập nhật thể loại thành công!')
            return redirect('admin_genres')
    return render(request, 'admin_panel/edit_genre.html', {
        'form': form, 'genre': genre, 'admin_name': request.session.get('user_name', 'Admin'),
    })


@admin_required
def admin_delete_genre(request, genre_id):
    genre = get_object_or_404(TheLoai, pk=genre_id)
    if request.method == 'POST':
        genre.delete()
        messages.success(request, 'Đã xóa thể loại!')
        return redirect('admin_genres')
    return render(request, 'admin_panel/confirm_delete.html', {
        'item': genre, 'item_name': genre.TenTL, 'cancel_url': 'admin_genres',
        'admin_name': request.session.get('user_name', 'Admin'),
    })
