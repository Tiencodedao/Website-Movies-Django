from django.db import models


class TheLoai(models.Model):
    """Bảng theloai"""
    MaTL = models.AutoField(primary_key=True, db_column='MATL')
    TenTL = models.CharField(max_length=100, db_column='TENTL')

    class Meta:
        db_table = 'theloai'
        managed = False

    def __str__(self):
        return self.TenTL


class Phim(models.Model):
    """Bảng phim"""
    MaPhim = models.AutoField(primary_key=True, db_column='MaPhim')
    TenPhim = models.CharField(max_length=255, db_column='TenPhim')
    MaTL = models.ForeignKey(
        TheLoai, on_delete=models.SET_NULL, null=True, blank=True,
        db_column='MATL', related_name='phim_set'
    )
    NgayKhoiChieu = models.DateField(null=True, blank=True, db_column='NgayKhoiChieu')
    MoTa = models.TextField(null=True, blank=True, db_column='MoTa')
    Hinh = models.CharField(max_length=255, null=True, blank=True, db_column='Hinh')
    Trailer = models.CharField(max_length=500, null=True, blank=True, db_column='Trailer')
    ThoiLuong = models.IntegerField(null=True, blank=True, db_column='ThoiLuong', default=120)

    class Meta:
        db_table = 'phim'
        managed = False

    def __str__(self):
        return self.TenPhim


class Phong(models.Model):
    """Bảng phong"""
    MaPhong = models.AutoField(primary_key=True, db_column='MaPhong')
    TenPhong = models.CharField(max_length=100, db_column='TenPhong')

    class Meta:
        db_table = 'phong'
        managed = False

    def __str__(self):
        return self.TenPhong


class SuatChieu(models.Model):
    """Bảng suatchieu"""
    MaSuatChieu = models.AutoField(primary_key=True, db_column='MaSuatChieu')
    MaPhim = models.ForeignKey(
        Phim, on_delete=models.CASCADE,
        db_column='MaPhim', related_name='suatchieu_set'
    )
    MaPhong = models.ForeignKey(
        Phong, on_delete=models.CASCADE,
        db_column='MaPhong', related_name='suatchieu_set'
    )
    NgayChieu = models.DateField(db_column='NgayChieu')
    GioBatDau = models.TimeField(db_column='GioBatDau')
    GiaVe = models.DecimalField(max_digits=10, decimal_places=0, db_column='GiaVe')

    class Meta:
        db_table = 'suatchieu'
        managed = False

    def __str__(self):
        return f"{self.MaPhim.TenPhim} - {self.NgayChieu} {self.GioBatDau}"


class CinemaUser(models.Model):
    """Bảng users"""
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=150)
    user_email = models.EmailField(unique=True)
    user_password = models.CharField(max_length=255)
    user_role = models.CharField(max_length=50, default='customer')
    IsStaff = models.BooleanField(default=False)

    class Meta:
        db_table = 'users'
        managed = False

    def __str__(self):
        return self.user_name


class HoaDon(models.Model):
    """Bảng hoadon"""
    MaHoaDon = models.AutoField(primary_key=True, db_column='MaHoaDon')
    MaSuatChieu = models.ForeignKey(
        SuatChieu, on_delete=models.CASCADE,
        db_column='MaSuatChieu', related_name='hoadon_set'
    )
    Ghe = models.CharField(max_length=255, db_column='Ghe')
    SoLuong = models.IntegerField(db_column='SoLuong')
    ThanhTien = models.DecimalField(max_digits=12, decimal_places=0, db_column='ThanhTien')
    guest_name = models.CharField(max_length=150, null=True, blank=True)
    guest_email = models.EmailField(null=True, blank=True)
    guest_phone = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        db_table = 'hoadon'
        managed = False

    def __str__(self):
        return f"HD#{self.MaHoaDon} - {self.guest_name}"


class Ve(models.Model):
    """Bảng ve"""
    MaVe = models.AutoField(primary_key=True, db_column='MaVe')
    MaPhim = models.ForeignKey(
        Phim, on_delete=models.CASCADE,
        db_column='MaPhim', related_name='ve_set'
    )
    GiaVe = models.DecimalField(max_digits=10, decimal_places=0, db_column='GiaVe')

    class Meta:
        db_table = 've'
        managed = False
