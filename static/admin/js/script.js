// SIDEBAR DROPDOWN
const allDropdown = document.querySelectorAll('#sidebar .side-dropdown');
const sidebar = document.getElementById('sidebar');

allDropdown.forEach(item=> {
	const a = item.parentElement.querySelector('a:first-child');
	a.addEventListener('click', function (e) {
		e.preventDefault();

		if(!this.classList.contains('active')) {
			allDropdown.forEach(i=> {
				const aLink = i.parentElement.querySelector('a:first-child');

				aLink.classList.remove('active');
				i.classList.remove('show');
			})
		}

		this.classList.toggle('active');
		item.classList.toggle('show');
	})
})





// SIDEBAR COLLAPSE
const toggleSidebar = document.querySelector('nav .toggle-sidebar');
const allSideDivider = document.querySelectorAll('#sidebar .divider');

if(sidebar.classList.contains('hide')) {
	allSideDivider.forEach(item=> {
		item.textContent = '-'
	})
	allDropdown.forEach(item=> {
		const a = item.parentElement.querySelector('a:first-child');
		a.classList.remove('active');
		item.classList.remove('show');
	})
} else {
	allSideDivider.forEach(item=> {
		item.textContent = item.dataset.text;
	})
}

toggleSidebar.addEventListener('click', function () {
	sidebar.classList.toggle('hide');

	if(sidebar.classList.contains('hide')) {
		allSideDivider.forEach(item=> {
			item.textContent = '-'
		})

		allDropdown.forEach(item=> {
			const a = item.parentElement.querySelector('a:first-child');
			a.classList.remove('active');
			item.classList.remove('show');
		})
	} else {
		allSideDivider.forEach(item=> {
			item.textContent = item.dataset.text;
		})
	}
})




sidebar.addEventListener('mouseleave', function () {
	if(this.classList.contains('hide')) {
		allDropdown.forEach(item=> {
			const a = item.parentElement.querySelector('a:first-child');
			a.classList.remove('active');
			item.classList.remove('show');
		})
		allSideDivider.forEach(item=> {
			item.textContent = '-'
		})
	}
})



sidebar.addEventListener('mouseenter', function () {
	if(this.classList.contains('hide')) {
		allDropdown.forEach(item=> {
			const a = item.parentElement.querySelector('a:first-child');
			a.classList.remove('active');
			item.classList.remove('show');
		})
		allSideDivider.forEach(item=> {
			item.textContent = item.dataset.text;
		})
	}
})




// PROFILE DROPDOWN
const profile = document.querySelector('nav .profile');
const imgProfile = profile.querySelector('img');
const dropdownProfile = profile.querySelector('.profile-link');

imgProfile.addEventListener('click', function () {
	dropdownProfile.classList.toggle('show');
})




// MENU
const allMenu = document.querySelectorAll('main .content-data .head .menu');

allMenu.forEach(item=> {
	const icon = item.querySelector('.icon');
	const menuLink = item.querySelector('.menu-link');

	icon.addEventListener('click', function () {
		menuLink.classList.toggle('show');
	})
})



window.addEventListener('click', function (e) {
	if(e.target !== imgProfile) {
		if(e.target !== dropdownProfile) {
			if(dropdownProfile.classList.contains('show')) {
				dropdownProfile.classList.remove('show');
			}
		}
	}

	allMenu.forEach(item=> {
		const icon = item.querySelector('.icon');
		const menuLink = item.querySelector('.menu-link');

		if(e.target !== icon) {
			if(e.target !== menuLink) {
				if (menuLink.classList.contains('show')) {
					menuLink.classList.remove('show')
				}
			}
		}
	})
})





// PROGRESSBAR
const allProgress = document.querySelectorAll('main .card .progress');

allProgress.forEach(item=> {
	item.style.setProperty('--value', item.dataset.value)
})






// APEXCHART
var options = {
  series: [{
  name: 'series1',
  data: [31, 40, 28, 51, 42, 109, 100]
}, {
  name: 'series2',
  data: [11, 32, 45, 32, 34, 52, 41]
}],
  chart: {
  height: 350,
  type: 'area'
},
dataLabels: {
  enabled: false
},
stroke: {
  curve: 'smooth'
},
xaxis: {
  type: 'datetime',
  categories: ["2018-09-19T00:00:00.000Z", "2018-09-19T01:30:00.000Z", "2018-09-19T02:30:00.000Z", "2018-09-19T03:30:00.000Z", "2018-09-19T04:30:00.000Z", "2018-09-19T05:30:00.000Z", "2018-09-19T06:30:00.000Z"]
},
tooltip: {
  x: {
    format: 'dd/MM/yy HH:mm'
  },
},
};

var chart = new ApexCharts(document.querySelector("#chart"), options);
chart.render();





// --- PHẦN XỬ LÝ ACTION MENU ---
// (Đặt vào tệp script.js của bạn)

// Hàm để bật/tắt menu
function toggleActionMenu(button) {
    const menu = button.nextElementSibling; // Lấy ul.action-menu ngay sau button
     if (!menu || !menu.classList.contains('action-menu')) {
         console.error("Không tìm thấy phần tử menu hợp lệ ngay sau nút này.", button);
         return; // Dừng lại nếu không tìm thấy menu
     }

    const isShown = menu.classList.contains('show');

    // Đóng tất cả các menu khác đang mở
    closeAllActionMenus();

    // Nếu menu này chưa mở thì mở nó ra
    if (!isShown) {
        menu.classList.add('show');
        button.setAttribute('aria-expanded', 'true');
    }
    // Nếu đang mở thì nó sẽ được đóng bởi closeAllActionMenus() hoặc click outside
    // Không cần else ở đây nếu closeAllActionMenus() chạy trước
     button.setAttribute('aria-expanded', menu.classList.contains('show')); // Cập nhật trạng thái cuối cùng
}

// Hàm đóng tất cả các menu đang mở
function closeAllActionMenus() {
    document.querySelectorAll('.action-menu.show').forEach(openMenu => {
        openMenu.classList.remove('show');
        const correspondingButton = openMenu.previousElementSibling;
        if (correspondingButton && correspondingButton.classList.contains('action-button')) {
             correspondingButton.setAttribute('aria-expanded', 'false');
        }
    });
}

// Đóng menu nếu click ra ngoài phạm vi của action container
window.addEventListener('click', function(e) {
    if (!e.target.closest('.action-container')) { // Kiểm tra nếu click không nằm trong container nào
        closeAllActionMenus();
    }
    // Xử lý trường hợp click vào nút action button thì không bị window listener đóng ngay
     else if (e.target.closest('.action-button')) {
        // Nếu click vào nút action, hàm toggleActionMenu đã xử lý, không cần làm gì thêm ở đây
        // để tránh việc đóng ngay menu vừa mở.
     }
});

 // Nếu bạn KHÔNG dùng onclick="toggleActionMenu(this)" trong HTML,
 // bạn cần thêm đoạn mã này để lắng nghe sự kiện click trên các nút:
 /*
 document.querySelectorAll('.action-button').forEach(button => {
     button.addEventListener('click', function(event) {
         event.stopPropagation(); // Ngăn sự kiện click lan ra window listener ngay lập tức
         toggleActionMenu(this); // Gọi hàm toggle khi nút được click
     });
 });
 */

// --- KẾT THÚC PHẦN XỬ LÝ ACTION MENU ---

// --- (Các phần code JS khác của bạn) ---