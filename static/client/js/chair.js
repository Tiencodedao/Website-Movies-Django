function selectSeat(seat) {
    seat.classList.toggle("selected");
    updateSeatInfo();
}

function updateSeatInfo() {
    let selectedSeats = document.querySelectorAll('.seat.selected');
    let totalTickets = selectedSeats.length;
    let totalMoney = totalTickets * 50000; // assuming each seat costs 50,000 VND

    document.getElementById('total_ticket').innerText = totalTickets;
    document.getElementById('total_money').innerText = totalMoney.toLocaleString() + " VNĐ";
}