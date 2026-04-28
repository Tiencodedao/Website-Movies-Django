from django import forms
from .models import Phim, Phong, SuatChieu, HoaDon, CinemaUser, TheLoai


class TheLoaiForm(forms.ModelForm):
    class Meta:
        model = TheLoai
        fields = ['TenTL']
        widgets = {'TenTL': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Tên thể loại'})}
        labels = {'TenTL': 'Tên thể loại'}


class PhimForm(forms.ModelForm):
    class Meta:
        model = Phim
        fields = ['TenPhim', 'MaTL', 'NgayKhoiChieu', 'MoTa', 'Hinh', 'Trailer', 'ThoiLuong']
        widgets = {
            'TenPhim': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Tên phim'}),
            'MaTL': forms.Select(attrs={'class': 'form-input'}),
            'NgayKhoiChieu': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'MoTa': forms.Textarea(attrs={'class': 'form-input', 'rows': 4}),
            'Hinh': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Tên file ảnh'}),
            'Trailer': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'URL YouTube Embed (vd: https://www.youtube.com/embed/abc123)'}),
            'ThoiLuong': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Thời lượng (phút)', 'min': 1}),
        }
        labels = {
            'TenPhim': 'Tên phim', 'MaTL': 'Thể loại', 'NgayKhoiChieu': 'Ngày khởi chiếu',
            'MoTa': 'Mô tả', 'Hinh': 'Ảnh (tên file)', 'Trailer': 'Link Trailer', 'ThoiLuong': 'Thời lượng (phút)',
        }


class PhongForm(forms.ModelForm):
    class Meta:
        model = Phong
        fields = ['TenPhong']
        widgets = {'TenPhong': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Tên phòng chiếu'})}
        labels = {'TenPhong': 'Tên phòng'}


class SuatChieuForm(forms.ModelForm):
    class Meta:
        model = SuatChieu
        fields = ['MaPhim', 'MaPhong', 'NgayChieu', 'GioBatDau', 'GiaVe']
        widgets = {
            'MaPhim': forms.Select(attrs={'class': 'form-input'}),
            'MaPhong': forms.Select(attrs={'class': 'form-input'}),
            'NgayChieu': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'GioBatDau': forms.TimeInput(attrs={'class': 'form-input', 'type': 'time'}),
            'GiaVe': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Giá vé (VNĐ)'}),
        }
        labels = {
            'MaPhim': 'Phim', 'MaPhong': 'Phòng chiếu', 'NgayChieu': 'Ngày chiếu',
            'GioBatDau': 'Giờ bắt đầu', 'GiaVe': 'Giá vé',
        }


class HoaDonForm(forms.ModelForm):
    class Meta:
        model = HoaDon
        fields = ['MaSuatChieu', 'Ghe', 'SoLuong', 'ThanhTien', 'guest_name', 'guest_email', 'guest_phone']
        widgets = {
            'MaSuatChieu': forms.Select(attrs={'class': 'form-input'}),
            'Ghe': forms.TextInput(attrs={'class': 'form-input'}),
            'SoLuong': forms.NumberInput(attrs={'class': 'form-input', 'min': 1}),
            'ThanhTien': forms.NumberInput(attrs={'class': 'form-input'}),
            'guest_name': forms.TextInput(attrs={'class': 'form-input'}),
            'guest_email': forms.EmailInput(attrs={'class': 'form-input'}),
            'guest_phone': forms.TextInput(attrs={'class': 'form-input'}),
        }
        labels = {
            'MaSuatChieu': 'Suất chiếu', 'Ghe': 'Ghế', 'SoLuong': 'Số lượng',
            'ThanhTien': 'Thành tiền', 'guest_name': 'Họ tên khách',
            'guest_email': 'Email khách', 'guest_phone': 'SĐT khách',
        }


class CinemaUserForm(forms.ModelForm):
    class Meta:
        model = CinemaUser
        fields = ['user_name', 'user_email', 'user_role', 'IsStaff']
        widgets = {
            'user_name': forms.TextInput(attrs={'class': 'form-input'}),
            'user_email': forms.EmailInput(attrs={'class': 'form-input'}),
            'user_role': forms.Select(
                choices=[('customer', 'Khách hàng'), ('staff', 'Nhân viên'), ('admin', 'Quản trị viên')],
                attrs={'class': 'form-input'}
            ),
            'IsStaff': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }
        labels = {
            'user_name': 'Họ tên', 'user_email': 'Email',
            'user_role': 'Vai trò', 'IsStaff': 'Là nhân viên/admin',
        }
