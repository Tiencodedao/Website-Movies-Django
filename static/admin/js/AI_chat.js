// === PHẦN KHAI BÁO HÀM TƯƠNG ĐƯƠNG PYTHON ===

// --- Dữ liệu phim mẫu (Giống trong Python) ---
const movies_data = [
    {"title": "Avengers: Endgame", "genre": "Hành động, Phiêu lưu, Khoa học viễn tưởng", "desc": "Các siêu anh hùng còn lại tập hợp để đảo ngược thiệt hại gây ra bởi Thanos."},
    {"title": "Parasite (Ký Sinh Trùng)", "genre": "Chính kịch, Hài kịch đen, Giật gân", "desc": "Một gia đình nghèo tìm cách xâm nhập vào cuộc sống của một gia đình giàu có."},
    {"title": "Spider-Man: No Way Home", "genre": "Hành động, Phiêu lưu, Khoa học viễn tưởng", "desc": "Peter Parker đối mặt với các ác nhân từ các vũ trụ khác."},
    {"title": "Inception", "genre": "Hành động, Khoa học viễn tưởng, Giật gân", "desc": "Một tên trộm chuyên đánh cắp thông tin bằng cách xâm nhập vào tiềm thức."},
    {"title": "Spirited Away (Vùng Đất Linh Hồn)", "genre": "Hoạt hình, Phiêu lưu, Kỳ ảo", "desc": "Một cô bé lạc vào thế giới linh hồn và phải tìm cách giải cứu cha mẹ mình."},
    {"title": "The Dark Knight", "genre": "Hành động, Tội phạm, Chính kịch", "desc": "Batman đối đầu với kẻ thù nguy hiểm Joker."},
    {"title": "Your Name (Tên Cậu Là Gì?)", "genre": "Hoạt hình, Lãng mạn, Kỳ ảo", "desc": "Hai học sinh trung học hoán đổi cơ thể một cách bí ẩn."},
    {"title": "Mắt Biếc", "genre": "Lãng mạn, Chính kịch", "desc": "Câu chuyện tình yêu đơn phương của Ngạn dành cho Hà Lan."},
    {"title": "Bố Già", "genre": "Hài kịch, Chính kịch, Gia đình", "desc": "Câu chuyện về cuộc sống và tình cảm gia đình trong một xóm lao động."},
    {"title": "Interstellar", "genre": "Khoa học viễn tưởng, Phiêu lưu, Chính kịch", "desc": "Một nhóm nhà du hành vũ trụ tìm kiếm một hành tinh mới cho nhân loại."},
    {"title": "Lật Mặt: 48H", "genre": "Hành động, Hài kịch", "desc": "Một người đàn ông phải bảo vệ gia đình khỏi sự truy đuổi của băng đảng."},
    {"title": "Em và Trịnh", "genre": "Tiểu sử, Âm nhạc, Lãng mạn", "desc": "Bộ phim về cuộc đời và những nàng thơ của nhạc sĩ Trịnh Công Sơn."}
];

// --- Các hàm chức năng viết bằng JavaScript ---

function jsSayHello() {
    return "Xin chào Việt Nam";
}

function jsSayToday() {
    const today = new Date();
    const options = { year: 'numeric', month: '2-digit', day: '2-digit' };
    // Định dạng lại theo dd/mm/yyyy hoặc tùy ý
    const formattedDate = today.toLocaleDateString('vi-VN', options).replace(/\//g, '-'); // vd: 13-04-2025
    return `Hôm nay là ngày ${formattedDate.split('-')[0]} tháng ${formattedDate.split('-')[1]} năm ${formattedDate.split('-')[2]}`;
}

function jsSayTime() {
    const now = new Date();
    const options = { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false };
    const formattedTime = now.toLocaleTimeString('vi-VN', options); // vd: 18:02:50
    return `Bây giờ là ${formattedTime.split(':')[0]} giờ ${formattedTime.split(':')[1]} phút ${formattedTime.split(':')[2]} giây`;
}

function jsSayEquation(numberStr) {
    try {
        const number = parseFloat(numberStr);
        if (isNaN(number)) return "Vui lòng nhập một số hợp lệ.";
        if (number >= 0) {
            const squareRoot = Math.sqrt(number);
            // toFixed(1) để làm tròn 1 chữ số thập phân
            return `Căn bậc 2 của ${number} là ${squareRoot.toFixed(1)}.`;
        } else {
            return "Không thể tính căn bậc 2 của số âm trong số thực.";
        }
    } catch (e) {
        return "Đã xảy ra lỗi khi tính căn bậc 2.";
    }
}

function jsSayDelta(aStr, bStr, cStr) {
    try {
        const a = parseFloat(aStr);
        const b = parseFloat(bStr);
        const c = parseFloat(cStr);
        if (isNaN(a) || isNaN(b) || isNaN(c)) return "Vui lòng nhập các hệ số hợp lệ.";

        if (a === 0) {
            if (b === 0) {
                return (c === 0) ? "Phương trình có vô số nghiệm." : "Phương trình vô nghiệm.";
            } else {
                const x = -c / b;
                return `Phương trình bậc nhất có nghiệm: x = ${x.toFixed(2)}`;
            }
        } else {
            const delta = b * b - 4 * a * c;
            if (delta > 0) {
                const x1 = (-b + Math.sqrt(delta)) / (2 * a);
                const x2 = (-b - Math.sqrt(delta)) / (2 * a);
                return `Phương trình có hai nghiệm phân biệt: x1 = ${x1.toFixed(2)}, x2 = ${x2.toFixed(2)}`;
            } else if (delta === 0) {
                const x = -b / (2 * a);
                return `Phương trình có nghiệm kép: x = ${x.toFixed(2)}`;
            } else {
                return "Phương trình vô nghiệm";
            }
        }
    } catch (e) {
        return "Đã xảy ra lỗi khi giải phương trình.";
    }
}

function jsSayPerimeterSquare(canhStr) {
    try {
        const canh = parseFloat(canhStr);
        if (isNaN(canh)) return "Vui lòng nhập một số hợp lệ cho cạnh hình vuông.";
        const perimeter = 4 * canh;
        return `Chu vi hình vuông là: ${perimeter}`;
    } catch (e) {
        return "Lỗi tính chu vi hình vuông.";
    }
}

function jsSayPerimeterRectangle(daiStr, rongStr) {
     try {
        const dai = parseFloat(daiStr);
        const rong = parseFloat(rongStr);
        if (isNaN(dai) || isNaN(rong)) return "Vui lòng nhập các giá trị hợp lệ.";
        const perimeter = 2 * (dai + rong);
        return `Chu vi hình chữ nhật là: ${perimeter}`;
    } catch (e) {
        return "Lỗi tính chu vi hình chữ nhật.";
    }
}

function jsSayPrimeNumber(numberStr) {
    try {
        const number = parseInt(numberStr, 10);
        if (isNaN(number)) return "Vui lòng nhập một số nguyên hợp lệ.";
        if (number < 2) {
            return `${number} không phải là số nguyên tố.`;
        }
        for (let i = 2; i <= Math.sqrt(number); i++) {
            if (number % i === 0) {
                return `${number} không phải là số nguyên tố.`;
            }
        }
        return `${number} là số nguyên tố.`;
    } catch (e) {
        return "Lỗi kiểm tra số nguyên tố.";
    }
}

function jsSayDaysBetweenDates(date1Str, date2Str) {
    try {
        // new Date() có thể hiểu định dạng YYYY-MM-DD
        const date1 = new Date(date1Str);
        const date2 = new Date(date2Str);
        // Kiểm tra xem date có hợp lệ không
        if (isNaN(date1.getTime()) || isNaN(date2.getTime())) {
             return "Vui lòng nhập ngày theo định dạng YYYY-MM-DD.";
        }
        // Tính mili giây giữa 2 ngày, chia cho số mili giây trong 1 ngày
        const diffTime = Math.abs(date2 - date1);
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        return `Số ngày giữa hai ngày là: ${diffDays} ngày`;
    } catch (e) {
        return "Vui lòng nhập ngày theo định dạng YYYY-MM-DD.";
    }
}

function jsGoogleSearch(query) {
     appendMessage('ai', `Ok, để tôi tìm kiếm "${query}" cho bạn.`);
     window.open(`https://www.google.com/search?q=${encodeURIComponent(query)}`, '_blank');
     // Không cần trả về gì vì đã mở tab mới
}

function jsOpenFacebook() {
     appendMessage('ai', `Ok, đang mở Facebook...`);
     window.open("https://www.facebook.com", '_blank');
}

function jsOpenYoutube() {
      appendMessage('ai', `Ok, đang mở YouTube...`);
      window.open("https://www.youtube.com", '_blank'); // URL đúng
}

// --- Hàm tư vấn phim bằng JavaScript ---
function jsRecommendMovies(user_message) {
    const genres_vn = {
        "hành động": "hành động",
        "phiêu lưu": "phiêu lưu",
        "khoa học viễn tưởng": "khoa học viễn tưởng", "viễn tưởng": "khoa học viễn tưởng", "sci-fi": "khoa học viễn tưởng",
        "chính kịch": "chính kịch", "drama": "chính kịch",
        "hài kịch": "hài kịch", "hài": "hài kịch", "comedy": "hài kịch",
        "giật gân": "giật gân", "thriller": "giật gân",
        "hoạt hình": "hoạt hình", "anime": "hoạt hình",
        "kỳ ảo": "kỳ ảo", "fantasy": "kỳ ảo",
        "tội phạm": "tội phạm", "crime": "tội phạm",
        "lãng mạn": "lãng mạn", "tình cảm": "lãng mạn", "romance": "lãng mạn",
        "gia đình": "gia đình",
        "tiểu sử": "tiểu sử", "biography": "tiểu sử",
        "âm nhạc": "âm nhạc", "musical": "âm nhạc"
        // Thêm các từ khóa và thể loại khác nếu cần
    };

    let found_genre = null;
    const message_lower = user_message.toLowerCase(); // Chuyển sang chữ thường để dễ so khớp

    for (const keyword in genres_vn) {
        if (message_lower.includes(keyword)) { // Dùng includes để linh hoạt hơn
            found_genre = genres_vn[keyword];
            break;
        }
    }

    let recommendations = [];
    let response = "";

    if (found_genre) {
        recommendations = movies_data.filter(movie =>
            movie.genre.toLowerCase().includes(found_genre)
        );
        if (recommendations.length === 0) {
            response = `Xin lỗi, tôi chưa có phim thể loại '${found_genre}' nào. Bạn thử thể loại khác nhé?`;
        } else {
            recommendations.sort(() => 0.5 - Math.random()); // Xáo trộn ngẫu nhiên
            response = `Đây là một vài gợi ý phim thể loại '${found_genre}' cho bạn:\n`;
            recommendations.slice(0, 3).forEach(movie => { // Lấy tối đa 3 phim
                response += `- ${movie.title}: ${movie.desc}\n`;
            });
        }
    } else {
        // Gợi ý ngẫu nhiên nếu không hỏi thể loại cụ thể
        const random_movies = movies_data.sort(() => 0.5 - Math.random()).slice(0, 3);
        response = "Bạn muốn xem phim thể loại nào? Hoặc đây là một vài gợi ý ngẫu nhiên:\n";
        random_movies.forEach(movie => {
            response += `- ${movie.title} (${movie.genre}): ${movie.desc}\n`;
        });
    }
    return response.trim(); // Trả về chuỗi kết quả
}


// --- Hàm xử lý tin nhắn chính bằng JavaScript ---
function jsProcessMessage(user_message) {
    const message = user_message.toLowerCase().trim();

    // 1. Kiểm tra các lệnh về phim trước
    const movie_keywords = ["phim", "movie", "tư vấn phim", "suggest movie", "recommend movie", "gợi ý phim", "phim hay"];
    if (movie_keywords.some(keyword => message.includes(keyword))) {
        return jsRecommendMovies(message);
    }

    // 2. Các câu trả lời/lệnh cố định
    if (message === "hey ai" || message === "heyai") return "Tôi có thể giúp gì được cho bạn?";
    if (message === "bạn là ai" || message === "hello" || message === "hi") return "Tôi là trợ lý ảo của bạn, chạy hoàn toàn bằng JavaScript!";
    if (message === "ngày hôm nay là gì" || message === "hôm nay ngày mấy") return jsSayToday();
    if (message === "mấy giờ rồi" || message === "giờ") return jsSayTime();
    if (message === "cảm ơn") return "Không có gì! Tôi luôn sẵn sàng giúp bạn.";
    if (message === "bạn khỏe không") return "Tôi là một chương trình JavaScript, luôn khỏe! Cảm ơn bạn đã hỏi.";
    if (message === "bạn làm được gì") return "Tôi có thể tính toán, cho biết ngày giờ, kiểm tra số, tư vấn phim,...";
    if (message === "xin chào" || message === "chào") return jsSayHello();

    if (message.startsWith("tính số ngày giữa")) {
         // Ví dụ: tính số ngày giữa 2024-01-10 và 2024-04-13
         const match = message.match(/giữa\s*(\d{4}-\d{2}-\d{2})\s*và\s*(\d{4}-\d{2}-\d{2})/);
         return match ? jsSayDaysBetweenDates(match[1], match[2]) : "Nhập dạng: tính số ngày giữa YYYY-MM-DD và YYYY-MM-DD";
    }

    // 4. Các lệnh mở web
     if (message.startsWith("tìm kiếm")) {
        const query = message.substring("tìm kiếm".length).trim();
        jsGoogleSearch(query); // Hàm này sẽ tự mở tab và thêm tin nhắn AI
        return null; // Trả về null để không thêm tin nhắn AI trùng lặp
    }
     if (message === "mở youtube") {
        jsOpenYoutube();
        return null;
    }


    // 5. Nếu không khớp lệnh nào
    return "Xin lỗi, tôi chưa hiểu yêu cầu của bạn. Hãy thử hỏi về phim, hoặc ngày giờ.";
}


// === PHẦN XỬ LÝ CHATBOX (ĐÃ CẬP NHẬT ĐỂ DÙNG JS) ===

// 1. Chọn các phần tử HTML (Giữ nguyên)
const chatBox = document.querySelector('main .chat-box');
const chatForm = document.querySelector('main .content-data form');
const chatInput = chatForm ? chatForm.querySelector('input') : null;
const sendButton = chatForm ? chatForm.querySelector('.btn-send') : null;

// 2. Hàm appendMessage (Giữ nguyên hoặc cải tiến nếu muốn)
// ... (Sao chép hàm appendMessage từ câu trả lời trước vào đây) ...
function appendMessage(sender, message) {
    // ... (Nội dung hàm appendMessage như cũ) ...
     if (!chatBox) {
        console.error("Phần tử .chat-box không tìm thấy!");
        return;
    }

    const msgDiv = document.createElement('div');
    msgDiv.classList.add('msg');
    if (sender === 'me') {
        msgDiv.classList.add('me');
    }

    let imageHtml = '';
    if (sender !== 'me') {
        // Sử dụng ảnh cục bộ thay vì link online
        imageHtml = '<img src="img/a1.jpg" alt="">'; // Bỏ dấu / ở đầu
    }

    const chatDiv = document.createElement('div');
    chatDiv.classList.add('chat');

    const profileDiv = document.createElement('div');
    profileDiv.classList.add('profile');

    const timeSpan = document.createElement('span');
    timeSpan.classList.add('time');
    const now = new Date();
    timeSpan.textContent = `${now.getHours()}:${now.getMinutes().toString().padStart(2, '0')}`;

    let usernameSpanHtml = '';
    if (sender !== 'me') {
        usernameSpanHtml = '<span class="username">Bot Chém Gió</span> '; // Đổi tên để phân biệt
    }

    profileDiv.innerHTML = usernameSpanHtml;
    profileDiv.appendChild(timeSpan);

    const p = document.createElement('p');
     if (typeof message === 'string') {
        message.split('\n').forEach((line, index) => {
            if (index > 0) p.appendChild(document.createElement('br'));
            p.appendChild(document.createTextNode(line));
        });
    } else {
         p.textContent = '[Lỗi: Tin nhắn không hợp lệ]';
         console.error("Invalid message type:", message);
    }


    chatDiv.appendChild(profileDiv);
    chatDiv.appendChild(p);

    msgDiv.innerHTML = imageHtml;
    msgDiv.appendChild(chatDiv);

    chatBox.appendChild(msgDiv);

    chatBox.scrollTop = chatBox.scrollHeight;
}


// 3. Xử lý sự kiện submit (Thay đổi phần xử lý)
if (chatForm && chatInput) {
    chatForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const userInput = chatInput.value.trim();

        if (userInput === '') return;

        // Hiển thị tin nhắn người dùng
        appendMessage('me', userInput);
        chatInput.value = '';

        // Gọi hàm xử lý bằng JavaScript thay vì fetch
        const aiReply = jsProcessMessage(userInput);

        // Chỉ hiển thị tin nhắn AI nếu hàm xử lý trả về kết quả (không phải null)
        if (aiReply !== null) {
             // Thêm một độ trễ nhỏ để mô phỏng AI đang "suy nghĩ" (tùy chọn)
            setTimeout(() => {
                appendMessage('ai', aiReply);
            }, 300); // Chờ 300 mili giây
        }
    });
} else {
    if (!chatForm) console.error("Không tìm thấy form chat trong main .content-data!");
    if (!chatInput) console.error("Không tìm thấy input trong form chat!");
}

