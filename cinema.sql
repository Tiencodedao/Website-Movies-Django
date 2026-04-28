-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: May 04, 2025 at 06:37 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cinema`
--

-- --------------------------------------------------------

--
-- Table structure for table `hoadon`
--

CREATE TABLE `hoadon` (
  `MaHoaDon` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `MaSuatChieu` int(11) NOT NULL,
  `Ghe` varchar(255) NOT NULL,
  `SoLuong` int(11) DEFAULT NULL,
  `ThanhTien` decimal(10,2) DEFAULT NULL,
  `guest_name` varchar(255) DEFAULT NULL,
  `guest_email` varchar(255) DEFAULT NULL,
  `guest_phone` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `hoadon`
--

INSERT INTO `hoadon` (`MaHoaDon`, `user_id`, `MaSuatChieu`, `Ghe`, `SoLuong`, `ThanhTien`, `guest_name`, `guest_email`, `guest_phone`) VALUES
(53635, NULL, 15, 'D05', 1, 75000.00, 'Chiến', 'Chien123@gmail.com', '0896745676'),
(203584, NULL, 7, 'D05', 1, 75000.00, 'Nguyen Van A', 'kimngoctien10112004@gmail.com', '0978436678'),
(469967, NULL, 17, 'C05,C06', 2, 150000.00, 'Duy', 'Duy@gmail.com', '0897689992'),
(574171, NULL, 6, 'D06', 1, 75000.00, 'Tin', 'Tin@gmail.com', '0874436471'),
(611389, NULL, 6, 'D06', 1, 75000.00, 'Kim Ngọc Tiến', 'kimngoctien10112004@gmail.com', '0344436471'),
(640938, NULL, 6, 'C04', 1, 75000.00, 'Tin', 'kimngoctien10112004@gmail.com', '0978436670'),
(919464, NULL, 19, 'B06', 1, 75000.00, 'Hiệp ', 'Hiep234@gmail.com', '0892045508'),
(939908, NULL, 6, 'D06', 1, 75000.00, 'Tin', 'Tin@gmail.com', '0874436471'),
(997884, NULL, 6, 'C03', 1, 75000.00, 'Nguyen Van B', 'kimngoctien10112004@gmail.com', '0978436678');

-- --------------------------------------------------------

--
-- Table structure for table `phim`
--

CREATE TABLE `phim` (
  `MaPhim` int(11) NOT NULL,
  `TenPhim` varchar(255) DEFAULT NULL,
  `MATL` int(11) NOT NULL,
  `NgayKhoiChieu` date DEFAULT NULL,
  `MoTa` text DEFAULT NULL,
  `Hinh` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `phim`
--

INSERT INTO `phim` (`MaPhim`, `TenPhim`, `MATL`, `NgayKhoiChieu`, `MoTa`, `Hinh`) VALUES
(16, 'Doremon ', 3, '2025-04-19', 'Thiếu nhi Japan', 'Doremon.jpg'),
(17, 'Black-pather', 1, '2025-04-19', 'Khoa học viễn tưởng', 'black-panther.jpg'),
(18, 'Batman and Superman', 1, '2025-04-20', 'Cuộc chiến sống còn thế giới mới', 'batman.webp'),
(19, 'Iron-man', 1, '2025-04-20', 'Siêu anh hùng của maver', 'iron-man.jpg'),
(20, 'Lật Mật', 2, '2025-04-20', 'Phim kể về gia đình ', 'Lat_mat.jpg'),
(21, 'Minecraft', 3, '2025-04-20', 'Trong thế giới của Minecraft, Steve và Alex phải đối mặt với những thử thách nguy hiểm khi họ tìm cách giải cứu thế giới khỏi sự tấn công của các mob hủy diệt. Họ sẽ phải đối đầu với Creeper, Enderman, và thậm chí là những quái vật mạnh mẽ trong thế giới mở của Minecraft. Liệu họ có thể tìm được cách để cứu lấy mọi thứ trước khi quá muộn? Đây là một cuộc phiêu lưu không thể bỏ qua cho những người yêu thích Minecraft!', 'minecraft.png'),
(22, 'Thám tử kiên', 2, '2025-04-20', 'Thám Tử Kiên là một nhân vật được yêu thích trong tác phẩm điện của ăn khách của NGƯỜI VỢ CUỐI CÙNG của Victor Vũ, Thám Tử Kiên: Kỳ Không Đầu sẽ là một phim Victor Vũ trở về với thể loại sở trường Kinh Dị - Trinh Thám sau những tác phẩm tình cảm lãng mạn trước đó.', 'tham_tu_kien.jpg'),
(26, 'Mortal Engines', 1, '2025-04-29', 'Phim hành động trong năm thế kĩ ', 'm9.jpg'),
(27, 'UnderWorld Blood Wars', 1, '2025-04-29', 'Các hội ma cà rồng còn lại đang trên bờ vực bị tiêu diệt bởi Lycans . Cả hai loài đều đang tìm kiếm Selene : ma cà rồng tìm kiếm công lý cho cái chết của Viktor , trong khi Lycans, do Marius lãnh đạo, có ý định sử dụng cô để tìm Eve, người có máu nắm giữ chìa khóa để xây dựng một đội quân lai giữa ma cà rồng và người sói.', 'Underworld_Blood_Wars.jpg'),
(28, 'Thor', 1, '2025-04-30', 'Năm 965, Odin (Anthony Hopkins), vị vua xứ Asgard, phát động chiến tranh chống bọn người khổng lồ băng (Frost Giants) xứ Jotunheim do Laufey (Colm Feore) cầm đầu, để ngăn chặn việc chúng đô hộ Chín Vương Quốc (Nine Realms), bắt đầu từ Trái Đất. Lực lượng Asgard đã đánh bại lũ khổng lồ và tịch thu nguồn năng lượng của chúng là Chiếc tráp mùa đông vĩnh cửu (Casket of Ancient Winters), mặc dù Odin mất mắt phải trong trận đánh cuối cùng ở Jotunheim.', 'Thor_poster.jpg'),
(29, 'The Lake', 1, '2025-04-30', 'Dưới Đáy Hồ – Lịch chiếu, mua vé, review phim kinh dị tại Moveek Xem lịch chiếu phim Dưới Đáy Hồ, mua vé online và đọc review phim kinh dị mới nhất tại Moveek – nền tảng đặt vé tiện lợi, cập nhật lịch chiếu toàn quốc. Dưới Đáy Hồ là phim kinh dị siêu nhiên đầu tiên tại Việt Nam khai thác chủ đề song trùng, lấy cảm hứng từ truyền thuyết rùng rợn về Hồ Đá Tử Thần – nơi gắn liền với nhiều vụ mất tích bí ẩn trong giới sinh viên. Trong một buổi chụp ảnh cưới, nhóm bạn trẻ gồm Tú (Karen Nguyễn), Trung (Kay Trần), Hùng (Thanh Duy) bất ngờ gặp thảm kịch. Sau đó, Tú bị cuốn vào vòng xoáy kỳ lạ, nơi những người xung quanh cô dần biến đổi, như thể đã trở thành một phiên bản khác. Ẩn sâu dưới đáy hồ là nơi những bản sao tà ác được sinh ra từ nỗi oán hận và chấp niệm chưa hóa giải. Khi bản sao tà ác của Tú trồi lên mặt nước, khát khao chiếm lấy cuộc sống thật của cô, Tú buộc phải đối mặt với quá khứ để giành lại chính mình...', 'the_lake.jpg'),
(30, 'Elio: Cậu Bé Đến Từ Trái Đất', 3, '2025-04-30', 'Elio là một cậu bé đam mê vũ trụ với trí tưởng tượng phong phú. Một hôm, cậu bất ngờ phải tham gia một cuộc phiêu lưu ngoài vũ trụ, nơi cậu phải xây dựng mối quan hệ mới với các dạng sống ngoài hành tinh. Elio phải vượt qua cuộc chiến ở quy mô liên thiên hà và khám phá ra con người thực sự của mình.', 'Elio.jpg'),
(31, 'Superman (2025)', 1, '2025-04-30', 'Superman, một phóng viên mới vào nghề ở Metropolis, bắt đầu hành trình hòa giải di sản Krypton của mình với hình ảnh con người Clark Kent.', 'Superman_2025.jpg'),
(32, 'Doctor Strange', 1, '2025-05-09', 'DOCTOR STRANGE là câu chuyện về bác sĩ Giải Phẫu Thần Kinh tên Stephen Vincent Strange. Cuộc đời anh thay đổi từ sau một tai nạn xe hơi khủng khiếp. Sau tai nạn đó, Stephen nhận ra mình có những năng lực bí ẩn cũng như biết thêm về thế giới ma thuật huyền bí. Từ một vị bác sĩ bình thường, Stephen Strange dần nhận được nhiều siêu năng lực để cứu trái đất khỏi những tai họa.', 'Doctor_Strange.jpg'),
(33, 'Spider-Man: No Way Home', 1, '2021-10-17', 'Spider-Man: No Way Home (Người Nhện: Không Còn Nhà) bắt đầu khi danh tính bị bại lộ, Peter Parker đến nhờ Doctor Strange giúp sức. Tuy nhiên, với loại bùa phép nguy hiểm, các vũ trụ va vào nhau và xuất hiện Green Globin, Doctor Octopus và Electro.', 'spiderman_no_way_home_ver18.jpg'),
(34, 'Phim Shin Cậu Bé Bút Chì', 3, '2025-05-02', 'Câu chuyện của bộ phim bắt đầu với Shinnosuke và những người bạn của Shin thuộc Đội đặc nhiệm Kasukabe trải qua một tuần ở lại \"Học viện Tư nhân Tenkasu Kasukabe\" (Còn gọi là \"Học viện Tenkasu\"), một trường nội trú ưu tú được quản lý bởi một AI hiện đại, \"Otsmun\". Tất cả các học sinh ban đầu được trao một huy hiệu với 1000 điểm và điểm của các em sẽ được Otsmun tăng hoặc giảm dựa trên hành vi và kết quả học tập của các em. Trong đó ai đó tấn công Kazama. Kết quả là trí thông minh của anh ta bị suy giảm và những vết cắn kỳ lạ để lại trên mông anh ta. Đội đặc nhiệm Kasukabe hợp lực với chủ tịch hội học sinh bỏ học của trường, Chishio Atsuki, một cựu vận động viên, để thành lập một nhóm thám tử và giải quyết bí ẩn', 'Shin2.png'),
(35, 'Chuyện Muông Thú Dạy Bé Cừu Bay', 3, '2025-04-25', 'Sống trong thế giới nơi chỉ có loài chim mới được phép bay đã giới hạn ước mơ của biết bao giống loài, điển hình là bé cừu nhỏ Woolina.Trên hành trình chinh phục giấc mơ không tưởng, Woolina đã sát cánh cùng hội bạn Beep Beep, Momo,..dù nhận lấy sự phản đối từ mọi người. Liệu với trái tim nhỏ bé đầy dũng cảm ấy, Woolina có phá vỡ được định kiến và hiện thực hóa được giấc mơ bay lượn tự do trên bầu trời nhỏ của mình?', 'cuu.png'),
(36, 'Quái Thú Đại Náo Sở Thú', 3, '2025-05-09', 'Một thiên thạch mang virus rơi xuống sở thú, biến các con vật thành Zombie kẹo dẻo. Cô sói Gracie và chú sư tử núi Dan đã hợp sức với nhóm bạn thú tìm cách cứu lấy sở thú. Cuối cùng, họ phát hiện ra âm nhạc chính là phương thuốc diệt virus hiệu quả nhất. Nhờ vậy, họ đã đẩy lùi được virus và đưa mọi thứ trở lại bình thường.', 'Night_of_Z.jpg'),
(37, 'Khủng Long Xanh ', 3, '2025-04-30', 'Khủng Nhong - một chú khủng long xanh với tính cách hiếu động, tò mò bị lạc mất cha mẹ và buộc phải lên đường tìm lại gia đình. Là một sinh vật sống trong cuốn truyện tranh do hoạ sĩ Tét vẽ - người đang muốn tẩy xóa những trang truyện tranh của mình sau lời phê bình từ nhà xuất bản, Khủng Nhong bắt đầu dịch chuyển từ cuốn truyện này sang cuốn truyện khác. Trên hành trình phiêu lưu qua những thế giới kỳ diệu, Khủng Nhong lần lượt gặp gỡ Phù Thuỷ Tinh Tú, Tiến Sĩ Tóc Búi và Giáo Sư Đầu Xù. Để cứu cha mẹ của Khủng Nhong, tất cả các nhân vật hoạt hình phải tin tưởng vào chính mình và thuyết phục hoạ sĩ Tét giữ lại “đứa con tinh thần” thay vì cố gắng sáng tác những gì ông không hề yêu thích.', 'Smok_Diplodok.webp'),
(38, 'Looney Tunes', 3, '2025-04-25', 'Vịt Daffy và heo Porky, bộ đôi lắm chiêu trong loạt phim hoạt hình kinh điển Looney Tunes, chính thức bước lên màn ảnh rộng với một phi vụ bùng nổ chưa từng có. Khi phát hiện nhà máy kẹo cao su trong thị trấn dính líu đến âm mưu thao túng Trái đất của người ngoài hành tinh, cả hai trở thành những anh hùng bất đắc sĩ và lao vào một hành trình hài hước, đầy hỗn loạn để cứu thế giới khỏi âm mưu xấu xa của kẻ thù.', 'Looney.webp'),
(39, 'Doraemon 2025', 3, '2025-05-23', 'Doraemon Movie 44 cũng là tác phẩm kỷ niệm 45 năm ra mắt loạt phim \"Doraemon the Movie\'\". Câu chuyện của phim kể về Doraemon, Nobita và những người bạn bước vào một bức tranh đến thế giới châu Âu thời Trung cổ. Trong bức tranh, họ gặp những đứa trẻ đến từ đất nước Artoria. Họ cũng chạm trán một con quỷ nhỏ có cánh tên là Chai. Cùng nhau, họ đối mặt với một kẻ thù mạnh mẽ để giành lấy một viên ngọc huyền thoại.', 'Doraemon2025.jpg'),
(40, 'Dế Mèn Phiêu Lưu Ký', 2, '2025-06-30', 'Tác phẩm văn học kinh điển của tác giả Tô Hoài và là tuổi thơ của bao thế hệ sắp được chuyển thể thành phiên bản hoạt hình 3D trên màn ảnh rộng.', 'Animation.jpg'),
(41, 'Thanh Gươm Diệt Quỷ: Vô Hạn Thành', 3, '2025-08-15', 'Cốt truyện sẽ được thông báo sau. Phần đầu tiên trong cốt truyện Infinity Castle.', 'Demon_Slayer.jpg'),
(42, 'Conan Movie 28', 3, '2025-07-25', 'Bộ phim Conan Movie 28 đã chính thức có lịch khởi chiếu tại Nhật Bản vào ngày 18 tháng 4 năm 2025. Hơn nữa, hình ảnh teaser do Gosho Aoyama vẽ cũng đã được phát hành! Với cảnh tượng được cho là vùng núi tuyết của tỉnh Nagano.', 'Conan Movie 28.jpg'),
(43, 'Lật Mặt 8: Vòng Tay Nắng', 2, '2025-04-30', 'Lật Mặt 8: Vòng Tay Nắng đang trong giai đoạn quay hình tại bối cảnh Bình Thuận, Ninh Thuận. Phần thứ 8 sẽ đa dạng chủ đề hơn các phần trước bao gồm hành động, hài, gia đình và yếu tố âm nhạc chiếm 30%. Lật Mặt 8: Vòng Tay Nắng cũng là lần đầu tiên đánh dấu sự xuất hiện của dàn diễn viên chính, thứ chính đông đảo hơn 40 diễn viên.', 'Lat_mat8.jpg'),
(44, 'Địa Đạo: Mặt Trời Trong Bóng Tối', 2, '2025-04-04', 'Năm 1967, giữa lúc Chiến tranh Việt Nam đang ở đỉnh điểm, đội du kích cách mạng 21 người trở thành mục tiêu “tìm và diệt” số 1 của quân đội Mỹ khi nhận nhiệm vụ bằng mọi giá phải bảo vệ một nhóm thông tin tình báo chiến lược mới đến ẩn náu tại căn cứ.', 'Dia_dao_VN.jpg'),
(45, 'Chị Dâu', 2, '2025-04-24', 'Chuyện bắt đầu khi bà Nhị - con dâu cả của gia đình quyết định nhân dịp đám giỗ của mẹ chồng, tụ họp cả bốn chị em gái - con ruột trong nhà lại để thông báo chuyện sẽ tự bỏ tiền túi ra sửa sang căn nhà từ đường cũ kỹ trước khi bão về. Vấn đề này khiến cho nội bộ gia đình bắt đầu có những lục đục, chị dâu và các em chồng cũng xảy ra mâu thuẫn, bất hoà.', 'Chi_Dau.jpg'),
(46, 'Ký Ức Máu', 2, '2025-05-01', 'Bác sĩ Man, một nhà tâm lý học có khả năng khám phá bí mật tiềm thức của bệnh nhân qua việc tư vấn. Một ngày nọ ông gặp tài xế Choi và cảm thấy kỳ lạ. Choi nhận lời tư vấn của Man, từ đó ông dần khám phá ra sự thật rùng rợn đằng sau chứng mất ngủ và ảo giác của ông Choi.', 'My Heart - Thriller.jpg'),
(47, 'Công Tử Bạc Liêu', 2, '2025-04-24', 'Lấy cảm hứng từ giai thoại nổi tiếng của nhân vật được mệnh danh là thiên hạ đệ nhất chơi ngông, Công Tử Bạc Liêu là bộ phim tâm lý hài hước, lấy bối cảnh Nam Kỳ Lục Tỉnh xưa của Việt Nam. BA HƠN - Con trai được thương yêu hết mực của ông Hội đồng Lịnh vốn là chủ ngân hàng đầu tiên tại Việt Nam, sau khi du học Pháp về đã sử dụng cả gia sản của mình vào những trò vui tiêu khiển, ăn chơi trác tán – nên được người dân gọi bằng cái tên Công Tử Bạc Liêu.', 'Cong_Tu_Bac_Lieu.jpg'),
(48, 'Chốt Đơn', 2, '2025-06-20', 'Hoàng Linh (Nguyễn Thúc Thuỳ Tiên) - Giám đốc của một công ty Livestream đang trên đà phát triển, gặp được ông An “newbie” (Quyền Linh) - một nhân viên quá tuổi với ngành. Câu chuyện thú vị tiêu biểu cho khái niệm “generation gap”, nhưng khi họ tìm được sự hoà hợp trong công việc, cuộc sống sẽ tạo nên nhiều thay đổi bất ngờ.', 'Chot_don.jpg'),
(49, 'Quỷ Nhập Tràng', 2, '2025-04-19', 'Phim lấy cảm hứng từ câu chuyện có thật và “truyền thuyết kinh dị nhất về người chết sống lại” - Ở một ngôi làng vùng cao, cặp vợ chồng Quang và Như sống bằng nghề mai táng. Cuộc sống yên bình của họ bị xáo trộn khi phát hiện một cỗ quan tài vô chủ trên mảnh đất nhà mình. Từ đây, những hiện tượng kỳ lạ bắt đầu xảy ra và ám ảnh cả ngôi làng.', 'The_Corpse.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `phong`
--

CREATE TABLE `phong` (
  `MaPhong` int(11) NOT NULL,
  `TenPhong` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `phong`
--

INSERT INTO `phong` (`MaPhong`, `TenPhong`) VALUES
(1, 'Phòng 1'),
(2, 'Phòng 2'),
(3, 'Phòng 3'),
(4, 'Phòng 4'),
(6, 'Phòng 6'),
(7, 'Phòng 7');

-- --------------------------------------------------------

--
-- Table structure for table `suatchieu`
--

CREATE TABLE `suatchieu` (
  `MaSuatChieu` int(11) NOT NULL,
  `MaPhim` int(11) DEFAULT NULL,
  `MaPhong` int(11) DEFAULT NULL,
  `NgayChieu` date DEFAULT NULL,
  `GioBatDau` time DEFAULT NULL,
  `GiaVe` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `suatchieu`
--

INSERT INTO `suatchieu` (`MaSuatChieu`, `MaPhim`, `MaPhong`, `NgayChieu`, `GioBatDau`, `GiaVe`) VALUES
(6, 30, 1, '2025-05-02', '19:00:00', 75000.00),
(7, 16, 2, '2025-05-03', '10:00:00', 75000.00),
(10, 22, 2, '2025-05-08', '01:03:00', 75000.00),
(11, 28, 3, '2025-05-10', '14:00:00', 75000.00),
(12, 32, 4, '2025-05-07', NULL, 75000.00),
(13, 16, 2, '2025-05-08', NULL, 75000.00),
(14, 16, 2, '2025-05-04', '10:00:00', 75000.00),
(15, 16, 1, '2025-05-04', '10:00:00', 75000.00),
(16, 22, 3, '2025-05-03', '22:00:00', 75000.00),
(17, 21, 2, '2025-05-04', '22:00:00', 75000.00),
(18, 16, 1, '2025-05-04', '03:37:00', 75000.00),
(19, 18, 2, '2025-05-04', '03:45:00', 75000.00),
(20, 18, 2, '2025-05-06', '19:00:00', 75000.00);

-- --------------------------------------------------------

--
-- Table structure for table `theloai`
--

CREATE TABLE `theloai` (
  `MATL` int(11) NOT NULL,
  `TENTL` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `theloai`
--

INSERT INTO `theloai` (`MATL`, `TENTL`) VALUES
(1, 'Hành Động'),
(2, 'Việt Nam'),
(3, 'Hoạt hình');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `user_role` varchar(50) DEFAULT NULL,
  `user_name` varchar(255) DEFAULT NULL,
  `user_email` varchar(255) DEFAULT NULL,
  `user_password` varchar(255) DEFAULT NULL,
  `IsStaff` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `user_role`, `user_name`, `user_email`, `user_password`, `IsStaff`) VALUES
(5, 'Admin', 'Tiến', 'kimngoctien10112004@gmail.com', 'Tien123@', 0),
(7, 'Customer', 'Chiến', 'chien123@gmail.com', '$2y$10$c5NUUtvs.Es9M6VTO6gEzeuoQHmjR.WdVehy3igckPV.ClsolZRPS', 0),
(8, 'Admin', 'Hiệp', 'hiep@gmail.com', '$2y$10$5Lcv0fVp3UD3OWFDkox5w.IMolXQdgQOaHiQL5O8fV9qH9td7nmc.', 0),
(9, 'Admin', 'Duy', 'Duy@gmail.com', 'Duy123@', 0),
(13, 'Customer', 'Nguyen Van A', 'NguyenVanA@gmail.com', '$2y$10$yubjVMcP0RPzQ1Gp89QiYuSzFFCkhmIAnnQevM0.doYF6ez7qs8Ai', 0),
(14, 'Customer', 'Nguyen Van B', 'NguyenB@gmail.com', '$2y$10$IQm6LSIoBTD.6PBMJ5gw9eHdlZSoiUQep4reQYc7ZfwnPtos5PeXa', 0);

-- --------------------------------------------------------

--
-- Table structure for table `ve`
--

CREATE TABLE `ve` (
  `MaVe` int(11) NOT NULL,
  `MaPhim` int(11) DEFAULT NULL,
  `GiaVe` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `hoadon`
--
ALTER TABLE `hoadon`
  ADD PRIMARY KEY (`MaHoaDon`),
  ADD KEY `fk_hoadon_user` (`user_id`),
  ADD KEY `fk_hoadon_suatchieu` (`MaSuatChieu`);

--
-- Indexes for table `phim`
--
ALTER TABLE `phim`
  ADD PRIMARY KEY (`MaPhim`,`MATL`),
  ADD KEY `FK_Phim_TheLoai` (`MATL`);

--
-- Indexes for table `phong`
--
ALTER TABLE `phong`
  ADD PRIMARY KEY (`MaPhong`);

--
-- Indexes for table `suatchieu`
--
ALTER TABLE `suatchieu`
  ADD PRIMARY KEY (`MaSuatChieu`),
  ADD KEY `MaPhim` (`MaPhim`),
  ADD KEY `MaPhong` (`MaPhong`);

--
-- Indexes for table `theloai`
--
ALTER TABLE `theloai`
  ADD PRIMARY KEY (`MATL`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `user_email` (`user_email`);

--
-- Indexes for table `ve`
--
ALTER TABLE `ve`
  ADD PRIMARY KEY (`MaVe`),
  ADD KEY `MaPhim` (`MaPhim`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `hoadon`
--
ALTER TABLE `hoadon`
  MODIFY `MaHoaDon` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=997885;

--
-- AUTO_INCREMENT for table `phim`
--
ALTER TABLE `phim`
  MODIFY `MaPhim` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=50;

--
-- AUTO_INCREMENT for table `phong`
--
ALTER TABLE `phong`
  MODIFY `MaPhong` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `suatchieu`
--
ALTER TABLE `suatchieu`
  MODIFY `MaSuatChieu` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `theloai`
--
ALTER TABLE `theloai`
  MODIFY `MATL` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `ve`
--
ALTER TABLE `ve`
  MODIFY `MaVe` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `hoadon`
--
ALTER TABLE `hoadon`
  ADD CONSTRAINT `fk_hoadon_suatchieu` FOREIGN KEY (`MaSuatChieu`) REFERENCES `suatchieu` (`MaSuatChieu`),
  ADD CONSTRAINT `fk_hoadon_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  ADD CONSTRAINT `hoadon_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  ADD CONSTRAINT `hoadon_ibfk_2` FOREIGN KEY (`MaSuatChieu`) REFERENCES `suatchieu` (`MaSuatChieu`);

--
-- Constraints for table `phim`
--
ALTER TABLE `phim`
  ADD CONSTRAINT `FK_Phim_TheLoai` FOREIGN KEY (`MATL`) REFERENCES `theloai` (`MATL`);

--
-- Constraints for table `suatchieu`
--
ALTER TABLE `suatchieu`
  ADD CONSTRAINT `suatchieu_ibfk_1` FOREIGN KEY (`MaPhim`) REFERENCES `phim` (`MaPhim`),
  ADD CONSTRAINT `suatchieu_ibfk_2` FOREIGN KEY (`MaPhong`) REFERENCES `phong` (`MaPhong`);

--
-- Constraints for table `ve`
--
ALTER TABLE `ve`
  ADD CONSTRAINT `ve_ibfk_1` FOREIGN KEY (`MaPhim`) REFERENCES `phim` (`MaPhim`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
