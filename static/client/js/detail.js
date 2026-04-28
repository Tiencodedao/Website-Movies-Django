// JavaScript cho trang chi tiết phim

// Khi cuộn trang, thêm class shadow cho header
window.addEventListener('scroll', function() {
    const header = document.querySelector('header');
    if (window.scrollY > 0) {
        header.classList.add('shadow');
    } else {
        header.classList.remove('shadow');
    }
});

// Menu Mobile Toggle
let menu = document.querySelector('#menu-icon');
let navbar = document.querySelector('.navbar');

menu.onclick = () => {
    menu.classList.toggle('bx-x');
    navbar.classList.toggle('active');
};

window.onscroll = () => {
    menu.classList.remove('bx-x');
    navbar.classList.remove('active');
};

// Cuộn đến phần trailer
function scrollToTrailer() {
    document.getElementById('trailer').scrollIntoView({
        behavior: 'smooth'
    });
}

// Chọn ngày
document.addEventListener('DOMContentLoaded', function() {
    const dateItems = document.querySelectorAll('.date-item');
    dateItems.forEach(item => {
        item.addEventListener('click', function() {
            dateItems.forEach(el => el.classList.remove('active'));
            this.classList.add('active');
            // Ở đây bạn có thể gọi AJAX để cập nhật lịch chiếu theo ngày
        });
    });
});

// Chọn suất chiếu
function selectTimeSlot(element, time) {
    const selectedDate = document.querySelector('.date-item.active').getAttribute('data-date');
    // Lấy mã phim từ URL (sẽ được định nghĩa trong PHP)
    // Chuyển đến trang đặt vé với các tham số
    window.location.href = `chair.php?id=${movieId}&date=${selectedDate}&time=${time}`;
}
