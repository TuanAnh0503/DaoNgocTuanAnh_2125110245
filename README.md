# PyClaw Assistant

> Chatbot dòng lệnh viết bằng Python thuần: trả lời theo lệnh, tính toán biểu thức an toàn, giải phương trình bậc 1 và bậc 2, đồng thời lưu toàn bộ lịch sử trò chuyện vào cơ sở dữ liệu SQLite.

---

## Mục lục

1. [Giới thiệu](#1-giới-thiệu)
2. [Tính năng](#2-tính-năng)
3. [Yêu cầu hệ thống](#3-yêu-cầu-hệ-thống)
4. [Cài đặt và chạy từng bước (Windows + VS Code)](#4-cài-đặt-và-chạy-từng-bước-windows--vs-code)
5. [Hướng dẫn sử dụng](#5-hướng-dẫn-sử-dụng)
6. [Chi tiết từng lệnh](#6-chi-tiết-từng-lệnh)
7. [Cách hoạt động bên trong](#7-cách-hoạt-động-bên-trong)
8. [Cơ sở dữ liệu](#8-cơ-sở-dữ-liệu)
9. [Cấu trúc dự án và tham chiếu hàm](#9-cấu-trúc-dự-án-và-tham-chiếu-hàm)
10. [Bảo mật](#10-bảo-mật)
11. [Danh sách kiểm thử](#11-danh-sách-kiểm-thử)
12. [Xử lý sự cố](#12-xử-lý-sự-cố)
13. [Hạn chế đã biết](#13-hạn-chế-đã-biết)
14. [Hướng dẫn mở rộng](#14-hướng-dẫn-mở-rộng)
15. [Hướng phát triển](#15-hướng-phát-triển)
16. [Câu hỏi thường gặp](#16-câu-hỏi-thường-gặp)
17. [Nhật ký thay đổi](#17-nhật-ký-thay-đổi)
18. [Phụ lục A: Giải thích mã nguồn theo từng khối](#18-phụ-lục-a-giải-thích-mã-nguồn-theo-từng-khối)
19. [Phụ lục B: Nền tảng toán học của lệnh giai](#19-phụ-lục-b-nền-tảng-toán-học-của-lệnh-giai)
20. [Phụ lục C: Phiên làm việc mẫu đầy đủ](#20-phụ-lục-c-phiên-làm-việc-mẫu-đầy-đủ)
21. [Phụ lục D: Kiểm thử tự động bằng unittest](#21-phụ-lục-d-kiểm-thử-tự-động-bằng-unittest)
22. [Phụ lục E: Đóng gói thành file .exe](#22-phụ-lục-e-đóng-gói-thành-file-exe-windows)
23. [Phụ lục F: Quản lý phiên bản bằng Git](#23-phụ-lục-f-quản-lý-phiên-bản-bằng-git)
24. [Phụ lục G: Bài tập thực hành có hướng dẫn](#24-phụ-lục-g-bài-tập-thực-hành-có-hướng-dẫn)
25. [Phụ lục H: Các quyết định thiết kế](#25-phụ-lục-h-các-quyết-định-thiết-kế)
26. [Phụ lục I: Bảng thuật ngữ](#26-phụ-lục-i-bảng-thuật-ngữ)
27. [Giấy phép và đóng góp](#27-giấy-phép-và-đóng-góp)

---

## 1. Giới thiệu

**PyClaw Assistant** là một trợ lý trò chuyện chạy trong cửa sổ Terminal. Bạn gõ một dòng, chương trình phân tích dòng đó theo các lệnh đã định nghĩa sẵn và trả lời ngay.

Đây **không phải** chatbot AI trả lời tự do. PyClaw hoạt động theo luật cố định (kiểu `if / elif`), nhờ đó:

- Chạy hoàn toàn offline, không cần Internet hay API key.
- Kết quả luôn dự đoán được.
- Mã nguồn ngắn, dễ đọc, rất phù hợp để học Python (xử lý chuỗi, `ast`, `sqlite3`, vòng lặp nhập xuất).

Toàn bộ chương trình nằm trong **một file duy nhất**: `main.py`.

---

## 2. Tính năng

| Nhóm | Mô tả |
|------|-------|
| Chào hỏi | Nhận biết các câu `xin chao`, `xin chào`, `chào`, `chao`, `hello`, `hi` |
| Thời gian | Lệnh `gio` hiển thị giờ, phút, giây và ngày hiện tại |
| Máy tính | Lệnh `tinh` tính biểu thức số học, **không dùng `eval()`** |
| Giải phương trình | Lệnh `giai` giải phương trình bậc 1 và bậc 2 theo ẩn `x` |
| Lịch sử | Mọi tin nhắn được lưu vào SQLite, lệnh `lichsu` xem 10 tin gần nhất |
| An toàn | Giới hạn số mũ, giới hạn kích thước kết quả, bắt lỗi chia cho 0 và cú pháp sai |
| Ổn định | Dòng trống bị bỏ qua, không phân biệt chữ hoa chữ thường, thoát bằng `thoat`, `exit` hoặc `quit` |

---

## 3. Yêu cầu hệ thống

- **Hệ điều hành:** Windows, macOS hoặc Linux (hướng dẫn bên dưới viết cho Windows).
- **Python:** phiên bản 3.8 trở lên.
- **Thư viện ngoài:** không cần. Chương trình chỉ dùng thư viện chuẩn:
  - `ast`: phân tích cú pháp biểu thức.
  - `operator`: các hàm phép toán tương ứng.
  - `re`: biểu thức chính quy để chuẩn hóa phương trình.
  - `sqlite3`: lưu lịch sử.
  - `datetime`: lấy giờ và đóng dấu thời gian.
- **Công cụ khuyến nghị:** Visual Studio Code (dùng Terminal tích hợp).

---

## 4. Cài đặt và chạy từng bước (Windows + VS Code)

### Bước 1: Kiểm tra Python đã được cài chưa

Mở Terminal và gõ:

```powershell
python --version
```

- Nếu hiện `Python 3.x.x` (từ 3.8 trở lên): chuyển sang Bước 2.
- Nếu báo không nhận ra lệnh: thử `py --version`. Nếu vẫn lỗi, tải Python tại python.org, khi cài nhớ tích chọn **Add Python to PATH**, rồi mở lại Terminal.

### Bước 2: Tạo thư mục dự án

Ví dụ tạo thư mục `D:\Pthiong`. Có thể tạo bằng File Explorer hoặc bằng lệnh:

```powershell
mkdir D:\Pthiong
```

### Bước 3: Đặt file mã nguồn

1. Lưu file `main.py` vào thư mục `D:\Pthiong`.
2. (Tùy chọn) lưu cả `README.md` vào cùng thư mục.

Kiểm tra file đã có chưa:

```powershell
Test-Path "D:\Pthiong\main.py"
```

Kết quả `True` nghĩa là file tồn tại.

### Bước 4: Mở dự án trong VS Code

1. Mở VS Code.
2. Chọn **File > Open Folder** và chọn `D:\Pthiong`.
3. Nhấn vào `main.py` ở thanh bên trái để mở.

### Bước 5: Mở Terminal tích hợp

Nhấn **Ctrl + `** (phím dấu huyền, nằm dưới phím Esc) hoặc chọn **Terminal > New Terminal**.

> **Quan trọng:** hãy chạy chương trình bằng Terminal của VS Code. Nếu chạy bằng nút "Run" ở một số môi trường, chương trình có thể không nhận được dữ liệu nhập và sẽ in thông báo "Không nhận được dữ liệu nhập từ terminal".

### Bước 6: Chạy chương trình

```powershell
cd D:\Pthiong
python main.py
```

Nếu máy báo không nhận lệnh `python`, dùng:

```powershell
py main.py
```

### Bước 7: Kiểm tra màn hình khởi động

Bạn sẽ thấy:

```
========================================
       PYCLAW ASSISTANT
========================================
Nhập 'help' để xem hướng dẫn.
Nhập 'thoat' để kết thúc.

Bạn:
```

Gõ `help` rồi nhấn Enter. Nếu danh sách lệnh có dòng `giai`, bạn đang chạy đúng phiên bản mới.

### Bước 8: Thoát chương trình

Gõ `thoat` (hoặc `exit`, `quit`) rồi nhấn Enter. Nếu chương trình bị treo, nhấn **Ctrl + C**.

> **Lưu ý khi sửa code:** Python chỉ đọc file `main.py` một lần lúc khởi động. Sau khi sửa và lưu (Ctrl + S), bạn phải **thoát và chạy lại** thì thay đổi mới có hiệu lực.

---

## 5. Hướng dẫn sử dụng

Chương trình chạy theo vòng lặp:

1. Hiện dấu nhắc `Bạn:` và chờ bạn gõ.
2. Nhận dòng nhập, xóa khoảng trắng thừa hai đầu.
3. Nếu dòng trống: bỏ qua, nhắc lại `Bạn:`.
4. Nếu là `thoat`, `exit`, `quit`: kết thúc.
5. Nếu là `lichsu`: in lịch sử rồi quay lại bước 1.
6. Còn lại: lưu tin nhắn của bạn, tạo câu trả lời, lưu câu trả lời, in ra màn hình.

### Bảng tóm tắt lệnh

| Lệnh | Chức năng | Ví dụ |
|------|-----------|-------|
| `help` | Xem danh sách lệnh | `help` |
| `gio` | Xem giờ và ngày hiện tại | `gio` |
| `tinh <biểu thức>` | Tính biểu thức số học | `tinh 12 * (3 + 2)` |
| `giai <phương trình>` | Giải phương trình bậc 1, bậc 2 | `giai x^2 - 5x + 6 = 0` |
| `lichsu` | Xem 10 tin nhắn gần nhất | `lichsu` |
| `thoat` / `exit` / `quit` | Kết thúc chương trình | `thoat` |
| `xin chao`, `chào`, `hello`, `hi`... | Chào hỏi | `hi` |

### Quy tắc chung

- **Không phân biệt chữ hoa, chữ thường:** `GIO`, `Gio`, `gio` đều hoạt động. `TINH 2+2` cũng chạy bình thường.
- **Khoảng trắng thừa hai đầu được bỏ qua.**
- Lệnh `tinh` và `giai` **bắt buộc có một dấu cách** sau tên lệnh. Gõ riêng `tinh` mà không kèm biểu thức sẽ nhận câu trả lời mặc định "Mình chưa hiểu yêu cầu này".
- Câu không khớp lệnh nào sẽ nhận: `Mình chưa hiểu yêu cầu này. Hãy nhập 'help' để xem các lệnh hiện có.`

---

## 6. Chi tiết từng lệnh

### 6.1. `help`

Hiển thị danh sách lệnh:

```
Bạn: help
PyClaw: Các lệnh có sẵn:
- help: xem hướng dẫn
- gio: xem giờ hiện tại
- tinh <biểu thức>: tính toán, ví dụ tinh 12 * (3 + 2)
- giai <phương trình>: giải phương trình bậc 1, bậc 2,
    ví dụ giai 2x + 6 = 0 hoặc giai x^2 - 5x + 6 = 0
- lichsu: xem lịch sử
- thoat: kết thúc chương trình
```

### 6.2. `gio`

Trả về giờ hệ thống theo định dạng `HH:MM:SS, ngày DD/MM/YYYY`:

```
Bạn: gio
PyClaw: Bây giờ là 12:51:55, ngày 28/10/2026.
```

### 6.3. Chào hỏi

Các câu được nhận biết (sau khi chuyển về chữ thường): `xin chao`, `xin chào`, `chào`, `chao`, `hello`, `hi`.

```
Bạn: xin chao
PyClaw: Chào bạn! Mình là PyClaw Assistant. Gõ 'help' để xem lệnh.
```

Chương trình so khớp **nguyên câu**, nên `xin chao ban` sẽ không được nhận biết.

### 6.4. `tinh <biểu thức>`: máy tính

#### Phép toán được hỗ trợ

| Ký hiệu | Ý nghĩa | Ví dụ | Kết quả |
|---------|---------|-------|---------|
| `+` | Cộng | `tinh 5 + 3` | `8` |
| `-` | Trừ | `tinh 5 - 3` | `2` |
| `*` | Nhân | `tinh 4 * 6` | `24` |
| `/` | Chia | `tinh 10/4` | `2.5` |
| `//` | Chia lấy phần nguyên | `tinh 7//2` | `3` |
| `%` | Chia lấy dư | `tinh 7 % 3` | `1` |
| `**` | Lũy thừa | `tinh 2**3` | `8` |
| `( )` | Dấu ngoặc | `tinh 12 * (3 + 2)` | `60` |
| `-`, `+` (một ngôi) | Số âm, số dương | `tinh -5 + 2` | `-3` |

Chỉ chấp nhận **số nguyên và số thực**. Chuỗi, tên biến, tên hàm đều bị từ chối.

#### Ví dụ thành công

```
Bạn: tinh 12 * (3 + 2)
PyClaw: Kết quả: 60

Bạn: tinh 10/4
PyClaw: Kết quả: 2.5

Bạn: tinh -5 + 2
PyClaw: Kết quả: -3
```

#### Các trường hợp báo lỗi

| Nhập | Phản hồi | Nguyên nhân |
|------|----------|-------------|
| `tinh 5 / 0` | `Không tính được: division by zero` | Chia cho 0 |
| `tinh 2**11` | `Không tính được: Số mũ quá lớn.` | Số mũ lớn hơn 10 |
| `tinh (11**10)**10` | `Không tính được: Kết quả quá lớn.` | Kết quả vượt 10^100 |
| `tinh abc` | `Không tính được: Biểu thức không hợp lệ.` | Có tên biến, không phải số |
| `tinh 'a'` | `Không tính được: Chỉ hỗ trợ số.` | Có chuỗi ký tự |
| `tinh 1 +` | `Không tính được: invalid syntax (<unknown>, line 1)` | Sai cú pháp |

#### Lưu ý về số thực

Máy tính biểu diễn số thực bằng dấu phẩy động nên có thể có sai số nhỏ:

```
Bạn: tinh 0.1+0.2
PyClaw: Kết quả: 0.30000000000000004
```

Đây là hành vi chuẩn của Python và các ngôn ngữ lập trình khác, không phải lỗi của PyClaw.

### 6.5. `giai <phương trình>`: giải phương trình

#### Cú pháp nhập

- Ẩn **luôn là `x`**.
- Phải có **đúng một dấu `=`**, hai vế đều không được để trống.
- Lũy thừa viết bằng `^` hoặc `**`: `x^2`, `x**2`.
- Được phép **bỏ dấu nhân** giữa hệ số và ẩn, hoặc trước dấu ngoặc: `2x`, `3(x+1)`, `(x+1)(x-2)`.
- Số thập phân dùng dấu chấm hoặc dấu phẩy: `0.5x` hoặc `0,5x`.
- Được phép có dấu cách: `2 x + 4 = 0` vẫn hiểu là `2*x + 4 = 0`.
- Hai vế có thể chứa cả `x` ở mỗi vế, ví dụ `2(x+1) = x + 5`.
- Có thể chia cho một số: `x/2 = 3`. Không thể chia cho biểu thức chứa `x`.
- Số mũ chỉ được là `0`, `1` hoặc `2`.

#### Quy ước nhận dạng bậc

Chương trình đưa phương trình về dạng `ax² + bx + c = 0` rồi xét:

| Điều kiện | Loại | Cách giải |
|-----------|------|-----------|
| `a ≠ 0` | Bậc 2 | Tính `Delta = b² - 4ac` |
| `a = 0`, `b ≠ 0` | Bậc 1 | `x = -c / b` |
| `a = 0`, `b = 0`, `c = 0` | Đồng nhất | Vô số nghiệm |
| `a = 0`, `b = 0`, `c ≠ 0` | Mâu thuẫn | Vô nghiệm |

Với bậc 2:

| Delta | Kết luận | Công thức |
|-------|----------|-----------|
| `Delta > 0` | Hai nghiệm phân biệt | `x1 = (-b - √Delta) / 2a`, `x2 = (-b + √Delta) / 2a` |
| `Delta = 0` | Nghiệm kép | `x = -b / 2a` |
| `Delta < 0` | Vô nghiệm (trong tập số thực) | Không có |

#### Ví dụ có kết quả đã kiểm chứng

**Phương trình bậc 1**

```
Bạn: giai 2x + 6 = 0
PyClaw: Phương trình bậc 1: 2x + 6 = 0
Nghiệm: x = -3
```

```
Bạn: giai 2(x+1) = x + 5
PyClaw: Phương trình bậc 1: 1x - 3 = 0
Nghiệm: x = 3
```

```
Bạn: giai 0.5x = 3
PyClaw: Phương trình bậc 1: 0.5x - 3 = 0
Nghiệm: x = 6
```

**Phương trình bậc 2, hai nghiệm**

```
Bạn: giai x^2 - 5x + 6 = 0
PyClaw: Phương trình bậc 2: 1x² - 5x + 6 = 0
Delta = 1
Hai nghiệm: x1 = 2, x2 = 3
```

```
Bạn: giai 2x^2 - 3x - 2 = 0
PyClaw: Phương trình bậc 2: 2x² - 3x - 2 = 0
Delta = 25
Hai nghiệm: x1 = -0.5, x2 = 2
```

```
Bạn: giai -x^2 + 4 = 0
PyClaw: Phương trình bậc 2: -1x² + 0x + 4 = 0
Delta = 16
Hai nghiệm: x1 = 2, x2 = -2
```

**Nghiệm kép**

```
Bạn: giai (x+1)^2 = 0
PyClaw: Phương trình bậc 2: 1x² + 2x + 1 = 0
Delta = 0
Nghiệm kép: x = -1
```

**Nghiệm vô tỉ (làm tròn 6 chữ số có nghĩa)**

```
Bạn: giai x^2 - 2 = 0
PyClaw: Phương trình bậc 2: 1x² + 0x - 2 = 0
Delta = 8
Hai nghiệm: x1 = -1.41421, x2 = 1.41421
```

**Vô nghiệm**

```
Bạn: giai x^2 + x + 1 = 0
PyClaw: Phương trình bậc 2: 1x² + 1x + 1 = 0
Delta = -3
Delta < 0: phương trình vô nghiệm (trong số thực).
```

```
Bạn: giai x = x + 1
PyClaw: Phương trình vô nghiệm.
```

**Vô số nghiệm**

```
Bạn: giai 3 = 3
PyClaw: Phương trình có vô số nghiệm.
```

#### Các trường hợp báo lỗi

| Nhập | Phản hồi | Nguyên nhân |
|------|----------|-------------|
| `giai x + 1` | `Không giải được: Phương trình cần đúng một dấu '='.` | Thiếu dấu `=` |
| `giai = 5` | `Không giải được: Hai vế của phương trình không được để trống.` | Một vế trống |
| `giai x^3 = 1` | `Không giải được: Số mũ phải là số nguyên 0, 1 hoặc 2.` | Số mũ lớn hơn 2 |
| `giai x*x*x = 1` | `Không giải được: Chỉ hỗ trợ phương trình bậc 1 và bậc 2.` | Tích tạo ra bậc 3 |
| `giai abc = 1` | `Không giải được: Chỉ hỗ trợ ẩn x, không hiểu 'abc'.` | Ẩn khác `x` |
| `giai x2 = 4` | `Không giải được: Chỉ hỗ trợ ẩn x, không hiểu 'x2'.` | Viết `x2` thay vì `x^2` |
| `giai x / 0 = 1` | `Không giải được: chia cho 0` | Chia cho 0 |

> **Mẹo:** muốn viết bình phương hãy dùng `x^2` hoặc `x*x`. Đừng viết `x2`.

### 6.6. `lichsu`

In ra tối đa 10 tin nhắn gần nhất, theo thứ tự cũ đến mới, mỗi dòng có dạng `[thời gian] vai trò: nội dung`:

```
Bạn: lichsu

--- 10 tin nhắn gần nhất ---
[2026-10-28T12:51:50] user: gio
[2026-10-28T12:51:50] assistant: Bây giờ là 12:51:50, ngày 28/10/2026.
[2026-10-28T12:51:58] user: giai x^2 - 5x + 6 = 0
[2026-10-28T12:51:58] assistant: Phương trình bậc 2: 1x² - 5x + 6 = 0
Delta = 1
Hai nghiệm: x1 = 2, x2 = 3
```

- `user`: tin bạn gõ. `assistant`: câu trả lời của PyClaw.
- Mỗi lượt hỏi đáp tạo ra 2 dòng, nên 10 tin tương đương khoảng 5 lượt.
- Nếu chưa có gì: `Chưa có lịch sử trò chuyện.`

### 6.7. `thoat`, `exit`, `quit`

```
Bạn: thoat
PyClaw đã kết thúc.
```

---

## 7. Cách hoạt động bên trong

### 7.1. Luồng xử lý một tin nhắn

```
Người dùng gõ một dòng
        |
        v
  strip() khoảng trắng
        |
   +----+-----------------------------+
   | dòng trống?  ----> bỏ qua, nhập lại
   | thoat/exit/quit? --> thoát vòng lặp
   | lichsu?  ----> show_history(), nhập lại
   +----+-----------------------------+
        |
        v
  save_message("user", ...)
        |
        v
  reply(message) --> chọn nhánh theo lệnh
        |
        v
  save_message("assistant", ...)
        |
        v
  in "PyClaw: ..." ra màn hình
```

### 7.2. Hàm `reply()` kiểm tra theo thứ tự

1. Chào hỏi.
2. `help`.
3. `gio`.
4. Bắt đầu bằng `tinh ` (gọi `calculate`).
5. Bắt đầu bằng `giai ` (gọi `solve_equation`).
6. Không khớp: trả về câu mặc định.

Chương trình dùng hai biến: `text` (bản gốc đã `strip`, dùng để lấy biểu thức) và `lower` (bản chữ thường, dùng để so khớp lệnh). Nhờ vậy lệnh không phân biệt hoa thường mà biểu thức người dùng nhập vẫn giữ nguyên.

### 7.3. Máy tính an toàn: vì sao không dùng `eval()`

`eval()` thực thi **bất kỳ đoạn mã Python nào**, nên nếu cho người dùng nhập vào `eval()` thì họ có thể chạy lệnh nguy hiểm (xóa file, đọc dữ liệu...). PyClaw thay bằng cách:

1. `ast.parse(expression, mode="eval")` biến chuỗi thành **cây cú pháp** (chưa chạy gì cả).
2. Hàm `evaluate()` duyệt cây đệ quy, chỉ chấp nhận 4 loại nút:
   - `Constant`: chỉ nhận `int` và `float`.
   - `BinOp`: phép toán hai ngôi, phải có trong từ điển `OPERATORS`.
   - `UnaryOp`: dấu `+` hoặc `-` một ngôi.
   - `Expression`: nút gốc.
3. Mọi nút khác (gọi hàm, tên biến, chuỗi, danh sách...) đều bị từ chối bằng `ValueError`.
4. Hai lớp chặn thêm: số mũ lớn hơn 10 bị từ chối, kết quả lớn hơn 10^100 bị từ chối (tránh làm treo máy bằng phép tính khổng lồ).

### 7.4. Bộ giải phương trình: từng bước

Ví dụ với đầu vào `2(x+1) = x + 5`.

**Bước 1: tách hai vế** bằng dấu `=`: vế trái `2(x+1)`, vế phải `x + 5`.

**Bước 2: chuẩn hóa từng vế** bằng `prepare_side()`:

| Thao tác | Ví dụ |
|----------|-------|
| Chuyển chữ thường | `X` thành `x` |
| Đổi dấu phẩy thập phân thành dấu chấm | `0,5x` thành `0.5x` |
| Đổi `^` thành `**` | `x^2` thành `x**2` |
| Chèn dấu nhân giữa số hoặc `)` và `x` | `2x` thành `2*x` |
| Chèn dấu nhân giữa `x` và `(` | `x(` thành `x*(` |
| Chèn dấu nhân giữa số hoặc `)` và `(` | `2(` thành `2*(`, `)(` thành `)*(` |

Kết quả: `2*(x+1)` và `x + 5`.

**Bước 2b: ghép thành một biểu thức duy nhất** bằng cách chuyển hết sang một vế: `(2*(x+1)) - (x + 5)`.

**Bước 3: phân tích thành đa thức** bằng `parse_poly()`. Hàm này duyệt cây `ast` giống máy tính, nhưng thay vì trả về số, nó trả về **từ điển hệ số** dạng `{bậc: hệ số}`:

- Hằng số `5` thành `{0: 5.0}`.
- Biến `x` thành `{1: 1.0}`.
- Cộng, trừ: cộng hoặc trừ hệ số cùng bậc (`poly_add`).
- Nhân: nhân từng cặp hạng tử, cộng số bậc (`poly_mul`).
- Lũy thừa: số mũ phải là 0, 1 hoặc 2, thực hiện bằng cách nhân lặp.
- Chia: chỉ được chia cho một hằng số khác 0.
- Sau mỗi phép nhân hoặc lũy thừa, `check_degree` từ chối nếu có hạng tử bậc lớn hơn 2.

Với ví dụ trên: `2*(x+1)` thành `{1: 2, 0: 2}`, `x + 5` thành `{1: 1, 0: 5}`, hiệu là `{1: 1, 0: -3}`.

**Bước 4: lấy hệ số** `a`, `b`, `c` (làm tròn 10 chữ số thập phân để tránh sai số nhỏ), ở ví dụ là `a = 0`, `b = 1`, `c = -3`.

**Bước 5: kết luận** theo bảng ở mục 6.5: `a = 0` và `b ≠ 0` nên là phương trình bậc 1, `x = -c / b = 3`.

### 7.5. Định dạng số

Hàm `fmt()` làm tròn đến 10 chữ số thập phân, đổi `-0.0` thành `0`, rồi in theo định dạng `.6g` (tối đa 6 chữ số có nghĩa). Do đó `2.0` hiển thị là `2`, và `1.4142135...` hiển thị là `1.41421`.

Hàm `sign_fmt()` thêm dấu cho hạng tử: số âm hiện `- 5`, số không âm hiện `+ 5`, giúp dòng mô tả phương trình đẹp (`x² - 5x + 6` thay vì `x² + -5x + 6`).

---

## 8. Cơ sở dữ liệu

### 8.1. Vị trí file

Dữ liệu nằm trong file **`pyclaw.db`**. Đường dẫn được khai báo bằng `DB_NAME = "pyclaw.db"` (đường dẫn **tương đối**), nghĩa là file được tạo trong **thư mục hiện hành của Terminal** lúc bạn chạy chương trình.

> Hãy luôn `cd D:\Pthiong` trước khi chạy. Nếu chạy từ thư mục khác, chương trình sẽ tạo thêm một file `pyclaw.db` mới ở đó và bạn sẽ thấy lịch sử "biến mất".

File được tạo tự động ở lần chạy đầu tiên (hàm `setup_database()` dùng `CREATE TABLE IF NOT EXISTS`).

### 8.2. Cấu trúc bảng `messages`

| Cột | Kiểu | Ràng buộc | Mô tả |
|-----|------|-----------|-------|
| `id` | INTEGER | Khóa chính, tự tăng | Số thứ tự tin nhắn |
| `role` | TEXT | NOT NULL | `user` hoặc `assistant` |
| `content` | TEXT | NOT NULL | Nội dung tin nhắn |
| `created_at` | TEXT | NOT NULL | Thời gian, dạng ISO 8601 đến giây, ví dụ `2026-10-28T12:51:55` |

### 8.3. Những gì được lưu và không được lưu

| Được lưu | Không được lưu |
|----------|----------------|
| Mọi tin nhắn của bạn (kể cả câu bot không hiểu) | Dòng trống |
| Mọi câu trả lời của PyClaw | Lệnh `lichsu` |
| | Lệnh `thoat`, `exit`, `quit` |

### 8.4. Cách xem và quản lý dữ liệu

**Cách 1: dùng Python** (không cần cài thêm gì):

```powershell
python -c "import sqlite3; [print(r) for r in sqlite3.connect('pyclaw.db').execute('SELECT * FROM messages')]"
```

**Cách 2: dùng công cụ giao diện** như DB Browser for SQLite hoặc tiện ích mở rộng SQLite Viewer trong VS Code, mở file `pyclaw.db`.

**Xóa toàn bộ lịch sử bằng Python:**

```powershell
python -c "import sqlite3; db=sqlite3.connect('pyclaw.db'); db.execute('DELETE FROM messages'); db.commit()"
```

**Hoặc đơn giản hơn:** thoát chương trình rồi xóa file `pyclaw.db`. Lần chạy sau sẽ tự tạo file mới, trống.

---

## 9. Cấu trúc dự án và tham chiếu hàm

### 9.1. Cấu trúc thư mục

```
Pthiong/
├── main.py        # toàn bộ mã nguồn
├── test_main.py   # 19 bài kiểm thử tự động (xem mục 21)
├── pyclaw.db      # cơ sở dữ liệu SQLite, tự tạo khi chạy lần đầu
└── README.md      # tài liệu này
```

### 9.2. Hằng số

| Tên | Giá trị | Vai trò |
|-----|---------|---------|
| `DB_NAME` | `"pyclaw.db"` | Tên file cơ sở dữ liệu |
| `OPERATORS` | từ điển | Ánh xạ nút `ast` sang hàm của module `operator`, đóng vai trò danh sách phép toán được phép |

### 9.3. Tham chiếu hàm

| Hàm | Tham số | Trả về | Mô tả |
|-----|---------|--------|-------|
| `calculate(expression)` | chuỗi biểu thức | số (`int` hoặc `float`) | Tính biểu thức số học bằng cây `ast`. Ném `ValueError` nếu không hợp lệ, `SyntaxError` nếu sai cú pháp, `ZeroDivisionError` nếu chia cho 0 |
| `poly_add(p, q, sign=1)` | hai đa thức, dấu | đa thức | Cộng (`sign=1`) hoặc trừ (`sign=-1`) hai đa thức dạng từ điển |
| `poly_mul(p, q)` | hai đa thức | đa thức | Nhân hai đa thức |
| `check_degree(poly)` | đa thức | đa thức | Ném `ValueError` nếu có hạng tử bậc lớn hơn 2 |
| `parse_poly(expression)` | chuỗi biểu thức theo `x` | đa thức `{bậc: hệ số}` | Phân tích biểu thức thành đa thức, không dùng `eval()` |
| `prepare_side(text)` | một vế của phương trình | chuỗi chuẩn hóa | Chèn dấu nhân, đổi `^` thành `**`, đổi dấu phẩy thập phân |
| `fmt(number)` | số | chuỗi | Làm tròn và định dạng `.6g` |
| `sign_fmt(number)` | số | chuỗi | Định dạng có dấu `+` hoặc `-` |
| `solve_equation(equation)` | chuỗi phương trình | chuỗi kết quả | Giải phương trình bậc 1 và bậc 2 |
| `setup_database()` | không | không | Tạo bảng `messages` nếu chưa có |
| `save_message(role, content)` | vai trò, nội dung | không | Thêm một dòng vào bảng `messages` |
| `show_history()` | không | không | In 10 tin nhắn gần nhất |
| `reply(message)` | chuỗi người dùng nhập | chuỗi trả lời | Chọn câu trả lời theo lệnh |
| `main()` | không | không | Vòng lặp chính: nhận lệnh, lưu, trả lời |

---

## 10. Bảo mật

| Vấn đề | Cách xử lý |
|--------|------------|
| Chạy mã tùy ý | Không dùng `eval()` hay `exec()`. Chỉ duyệt cây `ast` với danh sách nút và phép toán cho phép |
| Treo máy do số quá lớn | Số mũ tối đa 10 (máy tính) và 2 (giải phương trình); kết quả lớn hơn 10^100 bị từ chối |
| SQL Injection | Mọi câu lệnh SQL dùng tham số `?` thay vì nối chuỗi |
| Dữ liệu nhập sai | Bắt `ValueError`, `SyntaxError`, `ZeroDivisionError`, `OverflowError` và trả về thông báo gọn |
| Lỗi đầu vào đóng | Bắt `EOFError` và `OSError` khi `input()` không đọc được, in hướng dẫn rồi thoát an toàn |

**Lưu ý quyền riêng tư:** lịch sử được lưu **nguyên văn, không mã hóa** trong `pyclaw.db`. Đừng gõ mật khẩu hay thông tin nhạy cảm vào PyClaw.

---

## 11. Danh sách kiểm thử

Có hai cách kiểm thử: thủ công (bảng dưới đây) và tự động bằng `test_main.py` (xem mục 21).

Chạy chương trình rồi thử lần lượt. Cột phải là kết quả mong đợi.

### Chào hỏi và lệnh cơ bản

| Nhập | Kết quả mong đợi |
|------|------------------|
| `xin chao` | `Chào bạn! Mình là PyClaw Assistant. Gõ 'help' để xem lệnh.` |
| `hi` | Giống dòng trên |
| `help` | Danh sách lệnh, có dòng `giai` |
| `GIO` | Giờ và ngày hiện tại |
| (nhấn Enter, dòng trống) | Không phản hồi, hiện lại `Bạn:` |
| `abc` | `Mình chưa hiểu yêu cầu này. Hãy nhập 'help' để xem các lệnh hiện có.` |
| `tinh` | Giống dòng trên (thiếu biểu thức) |

### Máy tính

| Nhập | Kết quả mong đợi |
|------|------------------|
| `tinh 12 * (3 + 2)` | `Kết quả: 60` |
| `tinh 10/4` | `Kết quả: 2.5` |
| `tinh 7//2` | `Kết quả: 3` |
| `tinh 7 % 3` | `Kết quả: 1` |
| `tinh 2**3` | `Kết quả: 8` |
| `tinh -5 + 2` | `Kết quả: -3` |
| `tinh 5 / 0` | `Không tính được: division by zero` |
| `tinh 2**11` | `Không tính được: Số mũ quá lớn.` |
| `tinh (11**10)**10` | `Không tính được: Kết quả quá lớn.` |
| `tinh abc` | `Không tính được: Biểu thức không hợp lệ.` |
| `TINH 2+2` | `Kết quả: 4` |

### Giải phương trình

| Nhập | Kết quả mong đợi |
|------|------------------|
| `giai 2x + 6 = 0` | `x = -3` |
| `giai x^2 - 5x + 6 = 0` | `x1 = 2, x2 = 3` |
| `giai x^2 + 2x + 1 = 0` | Nghiệm kép `x = -1` |
| `giai x^2 + 1 = 0` | Vô nghiệm (Delta = -4) |
| `giai 2(x+1) = x + 5` | `x = 3` |
| `giai 3x^2 = 12` | `x1 = -2, x2 = 2` |
| `giai x = x + 1` | `Phương trình vô nghiệm.` |
| `giai 3 = 3` | `Phương trình có vô số nghiệm.` |
| `giai x^3 = 1` | Báo lỗi số mũ |
| `giai x + 1` | Báo thiếu dấu `=` |

### Lịch sử và thoát

| Thao tác | Kết quả mong đợi |
|----------|------------------|
| `lichsu` sau vài câu hỏi | Hiện các tin nhắn gần nhất kèm thời gian |
| `thoat`, chạy lại, `lichsu` | Vẫn thấy tin nhắn của lần chạy trước |
| `thoat` | `PyClaw đã kết thúc.` |

---

## 12. Xử lý sự cố

| Triệu chứng | Nguyên nhân thường gặp | Cách khắc phục |
|-------------|------------------------|----------------|
| `python` không được nhận ra | Python chưa cài hoặc chưa thêm vào PATH | Thử `py main.py`. Nếu vẫn lỗi, cài lại Python và tích **Add Python to PATH** |
| `help` không có dòng `giai` | Đang chạy bản code cũ | Thoát chương trình, dán code mới, lưu (Ctrl + S), chạy lại. Mở file bằng Ctrl + F tìm `giai` để xác nhận |
| Sửa code rồi mà không thấy đổi | Chưa chạy lại chương trình | Thoát bằng `thoat` hoặc Ctrl + C, rồi chạy lại `python main.py` |
| Tab file có dấu chấm tròn | Chưa lưu file | Nhấn Ctrl + S |
| `Không nhận được dữ liệu nhập từ terminal` | Chạy ở môi trường không có bàn phím nhập (ví dụ một số nút Run) | Chạy bằng Terminal của VS Code |
| `lichsu` báo chưa có lịch sử dù đã chat | Chạy từ thư mục khác nên đọc file `pyclaw.db` khác | `cd` về đúng thư mục dự án rồi chạy lại |
| `SyntaxError` ngay khi chạy | Dán thiếu hoặc thừa dòng, sai thụt lề | Dán lại toàn bộ file, kiểm tra tab thụt lề thống nhất 4 dấu cách |
| `NameError: name 'xxx' is not defined` | Thiếu một hàm hoặc biến khi dán code | Dán lại đầy đủ file `main.py` mới nhất |
| Chữ tiếng Việt hiện lỗi font | Terminal dùng bảng mã không hỗ trợ UTF-8 | Chạy `chcp 65001` trước khi chạy chương trình, hoặc dùng Terminal của VS Code |
| `giai` ra `1.23457e+06` | Định dạng `.6g` hiển thị số lớn kiểu khoa học | Đây là hành vi dự kiến, xem mục 13 |
| Treo, không phản hồi | Đang chờ nhập | Nhấn Ctrl + C để thoát |

---

## 13. Hạn chế đã biết

- **Không phải chatbot AI:** chỉ hiểu các lệnh cố định. Câu chào phải khớp nguyên câu.
- **Chỉ bậc 1 và bậc 2:** phương trình bậc 3 trở lên bị từ chối.
- **Chỉ một ẩn `x`:** chưa giải hệ phương trình, chưa hỗ trợ ẩn khác.
- **Chỉ nghiệm thực:** khi Delta < 0, chương trình báo vô nghiệm chứ chưa hiện nghiệm phức.
- **Định dạng `.6g`:** làm tròn 6 chữ số có nghĩa, nên số rất lớn hoặc rất nhỏ hiển thị kiểu khoa học (ví dụ `1234567x = 1` cho `x = 8.1e-07`) và nghiệm vô tỉ chỉ là gần đúng.
- **So sánh số thực:** việc xét `Delta = 0` dùng số thực dấu phẩy động, nên với hệ số thập phân đặc biệt có thể chênh sai số cực nhỏ.
- **Không có hàm toán học:** chưa hỗ trợ `sqrt()`, `sin()`, `log()`... (phép chia cho một số vẫn dùng được, ví dụ `giai x/2 + x/3 = 1`).
- **Lịch sử không mã hóa** và `lichsu` chỉ xem được 10 tin gần nhất.
- **Chạy một người dùng**, một phiên mỗi lần.

---

## 14. Hướng dẫn mở rộng

> Muốn luyện tập có hướng dẫn chi tiết hơn, xem các bài tập ở mục 24.

### 14.1. Thêm một lệnh mới (ví dụ `ngay`)

**Bước 1:** mở `main.py`, tìm hàm `reply()`.

**Bước 2:** thêm nhánh mới **trước** câu trả lời mặc định (đoạn `return ("Mình chưa hiểu yêu cầu này...`):

```python
    if lower == "ngay":
        return datetime.now().strftime("Hôm nay là ngày %d/%m/%Y.")
```

**Bước 3:** thêm dòng mô tả vào chuỗi trả về của `help`:

```python
            "- ngay: xem ngày hôm nay\n"
```

**Bước 4:** lưu file, thoát và chạy lại, thử gõ `ngay`.

### 14.2. Thêm câu chào mới

Thêm chuỗi vào bộ trong `reply()`:

```python
    if lower in ("xin chao", "xin chào", "chào", "chao", "hello", "hi", "alo"):
```

### 14.3. Đổi số tin hiển thị trong `lichsu`

Trong `show_history()` đổi `LIMIT 10` thành số mong muốn, và đổi dòng chữ `--- 10 tin nhắn gần nhất ---` cho khớp.

### 14.4. Nới hoặc siết giới hạn an toàn

Trong `calculate()`:

- Số mũ tối đa: đổi `abs(right) > 10`.
- Kích thước kết quả tối đa: đổi `abs(result) > 10**100`.

### 14.5. Đổi số chữ số hiển thị

Trong `fmt()`, đổi `:.6g` thành `:.10g` để hiện 10 chữ số có nghĩa.

### 14.6. Đổi tên hoặc vị trí file dữ liệu

Sửa `DB_NAME = "pyclaw.db"`. Để luôn lưu cạnh `main.py` bất kể chạy từ đâu, có thể dùng:

```python
import os
DB_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pyclaw.db")
```

---

## 15. Hướng phát triển

- [ ] Giải hệ hai phương trình hai ẩn.
- [ ] Hiển thị nghiệm phức khi Delta < 0.
- [ ] Hỗ trợ phân số chính xác (module `fractions`).
- [ ] Thêm lệnh `ghichu` để lưu và xem ghi chú cá nhân.
- [ ] Thêm lệnh `xoalichsu` để xóa lịch sử từ trong chương trình.
- [ ] Cho phép chọn số tin nhắn cần xem, ví dụ `lichsu 20`.
- [ ] Kết nối API AI để trả lời tự do mọi câu hỏi.
- [ ] Đóng gói thành file `.exe` (ví dụ bằng PyInstaller) để chạy không cần cài Python.
- [ ] Viết kiểm thử tự động bằng `unittest` hoặc `pytest`.

---

## 16. Câu hỏi thường gặp

**PyClaw có cần Internet không?**
Không. Mọi thứ chạy trên máy bạn.

**Dữ liệu của tôi có bị gửi đi đâu không?**
Không. Tin nhắn chỉ lưu trong file `pyclaw.db` ngay trong thư mục dự án.

**Vì sao `tinh` không dùng `eval()` cho nhanh?**
Vì `eval()` chạy được mọi đoạn mã Python, rất nguy hiểm nếu đầu vào không được kiểm soát. Cây `ast` cho phép chỉ chấp nhận đúng các phép toán đã liệt kê.

**Tôi có thể gõ hoa, gõ thường tùy ý không?**
Có. Tên lệnh không phân biệt hoa thường. Với `giai`, chữ `X` hoa cũng được hiểu là `x`.

**Vì sao `giai x2 = 4` báo lỗi?**
Vì `x2` được hiểu là một tên biến khác. Hãy viết `x^2` hoặc `x*x`.

**Vì sao nghiệm hiện `1.41421` mà không phải `√2`?**
PyClaw trả về giá trị gần đúng, làm tròn 6 chữ số có nghĩa.

**Làm sao xóa lịch sử?**
Thoát chương trình và xóa file `pyclaw.db`, hoặc dùng lệnh ở mục 8.4.

**Làm sao đổi lời chào hoặc thêm lệnh mới?**
Xem mục 14.

**Chương trình dùng được trên macOS hoặc Linux không?**
Được. Mã nguồn không phụ thuộc Windows. Chỉ cần thay `python` bằng `python3` nếu hệ thống yêu cầu.

---

## 17. Nhật ký thay đổi

| Phiên bản | Nội dung |
|-----------|----------|
| 1.0 | Bản đầu: chào hỏi, `help`, `gio`, `tinh` (máy tính an toàn bằng `ast`), lưu lịch sử SQLite |
| 1.1 | Dọn mã trong `reply()` (gộp chào hỏi lặp, dùng một biến `lower`), kích hoạt lệnh `lichsu` |
| 1.2 | Thêm lệnh `giai`: giải phương trình bậc 1 và bậc 2, hiển thị Delta và nghiệm |

---

## 18. Phụ lục A: Giải thích mã nguồn theo từng khối

Phần này đi qua `main.py` từ trên xuống dưới, giải thích **vì sao** mỗi khối được viết như vậy. Rất hữu ích nếu bạn muốn hiểu sâu hoặc tự sửa code.

### A.1. Phần import

```python
import ast
import operator
import re
import sqlite3
from datetime import datetime
```

| Thư viện | Dùng để làm gì |
|----------|----------------|
| `ast` | Biến chuỗi biểu thức thành cây cú pháp để duyệt an toàn |
| `operator` | Cung cấp sẵn các hàm `add`, `sub`, `mul`... tương ứng với phép toán |
| `re` | Biểu thức chính quy, dùng để chèn dấu nhân (`2x` thành `2*x`) |
| `sqlite3` | Cơ sở dữ liệu nhúng, lưu lịch sử vào một file duy nhất |
| `datetime` | Lấy giờ hiện tại cho lệnh `gio` và đóng dấu thời gian tin nhắn |

### A.2. Từ điển `OPERATORS`

```python
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ...
}
```

Đây là **danh sách trắng** (whitelist). Khi duyệt cây, nếu gặp phép toán không nằm trong từ điển này, chương trình từ chối. Muốn cho phép thêm phép toán nào, chỉ cần thêm vào đây (ví dụ `ast.BitXor: operator.xor`).

### A.3. Hàm `calculate()`

Cấu trúc gồm một hàm ngoài và một hàm lồng bên trong:

1. `ast.parse(expression, mode="eval")` trả về một nút `ast.Expression`. Bước này **chỉ phân tích cú pháp**, tuyệt đối chưa tính toán gì. Nếu chuỗi sai cú pháp, nó ném `SyntaxError`.
2. Hàm `evaluate(node)` duyệt đệ quy (tự gọi lại chính nó cho các nút con):
   - **`ast.Expression`**: nút gốc, đi tiếp vào `node.body`.
   - **`ast.Constant`**: nút chứa giá trị cụ thể. Điều kiện `type(node.value) in (int, float)` dùng `type(...)` thay vì `isinstance` để **loại cả `True` và `False`** (kiểu `bool` là con của `int` nên `isinstance(True, int)` là `True`, còn `type(True)` là `bool`).
   - **`ast.BinOp`**: phép toán hai ngôi như `a + b`. Hàm tính `left`, `right` trước, kiểm tra giới hạn, rồi gọi hàm tương ứng trong `OPERATORS`.
   - **`ast.UnaryOp`**: phép toán một ngôi, chủ yếu là dấu trừ trước số (`-5` được Python hiểu là `UnaryOp(USub, 5)`).
   - Mọi loại nút khác rơi xuống `raise ValueError("Biểu thức không hợp lệ.")`.

Hai lớp bảo vệ đáng chú ý:

```python
if op_type is ast.Pow and abs(right) > 10:
    raise ValueError("Số mũ quá lớn.")
...
if abs(result) > 10**100:
    raise ValueError("Kết quả quá lớn.")
```

Nếu không có chúng, người dùng gõ `tinh 9**9**9` có thể khiến máy tính toán rất lâu và ngốn bộ nhớ.

### A.4. Nhóm hàm đa thức (`poly_add`, `poly_mul`, `check_degree`, `parse_poly`)

Một đa thức được biểu diễn bằng từ điển `{bậc: hệ số}`:

| Đa thức | Biểu diễn |
|---------|-----------|
| `3x² - 5x + 2` | `{2: 3.0, 1: -5.0, 0: 2.0}` |
| `x + 5` | `{1: 1.0, 0: 5.0}` |
| `7` | `{0: 7.0}` |

- `poly_add(p, q, sign)`: duyệt từng hạng tử của `q` rồi cộng vào bản sao của `p` (nhân thêm `sign` để dùng chung cho phép trừ).
- `poly_mul(p, q)`: nhân **từng cặp** hạng tử, cộng số bậc, nhân hệ số, gom lại theo bậc. Ví dụ `(x + 1) * (x - 2)` cho `x² - x - 2`.
- `check_degree(poly)`: từ chối nếu có hạng tử bậc lớn hơn 2 mà hệ số khác 0. Dùng ngưỡng `1e-12` thay vì so với đúng `0` để bỏ qua sai số cực nhỏ.
- `parse_poly(expression)`: có cấu trúc **giống `calculate`**, chỉ khác là mỗi nút trả về một đa thức thay vì một số. Nút `Name` chỉ nhận tên `x`.

### A.5. `prepare_side()`

Đây là bước "dịch" cách viết toán học thông thường sang cú pháp Python hợp lệ. Có 3 biểu thức chính quy:

| Mẫu (regex) | Thay bằng | Tác dụng |
|-------------|-----------|----------|
| `(\d\|\))\s*x` | `\1*x` | `2x` thành `2*x`, `)x` thành `)*x` |
| `x\s*\(` | `x*(` | `x(` thành `x*(` |
| `(\d\|\))\s*\(` | `\1*(` | `2(` thành `2*(`, `)(` thành `)*(` |

Thứ tự thay thế quan trọng: đổi `^` thành `**` được làm **trước** để phần còn lại luôn gặp cú pháp Python.

### A.6. `fmt()`, `sign_fmt()` và `solve_equation()`

- `fmt(number)`: `round(number, 10)` để loại sai số thừa (ví dụ `2.0000000000001` thành `2.0`), đổi `-0.0` thành `0.0` bằng cách gán lại, rồi in dạng `.6g`.
- `sign_fmt(number)`: trả về `"+ 5"` hoặc `"- 5"` để chuỗi mô tả phương trình đẹp.
- `solve_equation(equation)`:
  1. Kiểm tra đúng một dấu `=`.
  2. Tách hai vế, kiểm tra không trống.
  3. Ghép `(vế trái) - (vế phải)` rồi gọi `parse_poly`.
  4. Lấy `a`, `b`, `c`, rẽ nhánh theo bảng ở mục 6.5.

### A.7. Các hàm cơ sở dữ liệu

```python
with sqlite3.connect(DB_NAME) as db:
    db.execute(...)
```

Dùng `with` giúp thao tác được **tự động commit** (lưu) khi khối lệnh kết thúc suôn sẻ, hoặc rollback (hoàn tác) nếu có lỗi. Lưu ý: với `sqlite3`, `with` **không tự đóng kết nối**, nhưng với chương trình nhỏ này kết nối sẽ được giải phóng khi biến `db` ra khỏi phạm vi.

Câu lệnh chèn dùng dấu `?` làm chỗ giữ chỗ để truyền tham số riêng, **không nối chuỗi**, nhờ vậy miễn nhiễm với SQL Injection:

```python
db.execute("INSERT INTO messages (role, content, created_at) VALUES (?, ?, ?)",
           (role, content, datetime.now().isoformat(timespec="seconds")))
```

`show_history()` lấy `ORDER BY id DESC LIMIT 10` (10 dòng **mới nhất**, xếp mới đến cũ), sau đó gọi `reversed(rows)` để in theo thứ tự cũ đến mới cho dễ đọc.

### A.8. Hàm `reply()`

Hàm nhận chuỗi, trả về chuỗi, **không in ra màn hình và không ghi dữ liệu**. Việc tách như vậy giúp hàm dễ kiểm thử (xem mục 21): chỉ cần gọi `reply("hi")` và so sánh kết quả.

### A.9. Hàm `main()`

- `setup_database()` chạy đầu tiên để chắc chắn bảng tồn tại.
- Vòng lặp `while True` chạy mãi đến khi gặp `break`.
- `input("Bạn: ")` nằm trong `try` để bắt `EOFError` và `OSError` (xảy ra khi môi trường không có đầu vào chuẩn).
- Thứ tự kiểm tra trong vòng lặp: dòng trống, lệnh thoát, lệnh `lichsu`, rồi mới lưu và trả lời. Vì `lichsu` được xử lý **trước** `save_message`, lệnh này không bị ghi vào lịch sử.
- Dòng cuối `if __name__ == "__main__": main()` đảm bảo `main()` chỉ tự chạy khi bạn chạy trực tiếp file, còn khi file khác `import main` (như trong kiểm thử) thì **không** tự chạy chương trình.

---

## 19. Phụ lục B: Nền tảng toán học của lệnh `giai`

### B.1. Công thức nghiệm phương trình bậc 2

Xét `ax² + bx + c = 0` với `a ≠ 0`.

1. Chia hai vế cho `a`: `x² + (b/a)x + c/a = 0`.
2. Chuyển hạng tử tự do sang phải: `x² + (b/a)x = -c/a`.
3. Cộng `(b/2a)²` vào hai vế để tạo bình phương đủ: `(x + b/2a)² = b²/4a² - c/a = (b² - 4ac) / 4a²`.
4. Đặt `Delta = b² - 4ac`. Khi đó `(x + b/2a)² = Delta / 4a²`.

Từ dòng cuối suy ra:

| Trường hợp | Vì sao |
|------------|--------|
| `Delta > 0` | Vế phải dương nên có hai căn bậc hai khác nhau: `x = (-b ± √Delta) / 2a` |
| `Delta = 0` | Vế phải bằng 0 nên chỉ có một giá trị: `x = -b / 2a` (nghiệm kép) |
| `Delta < 0` | Bình phương của số thực không thể âm nên không có nghiệm thực |

### B.2. Ví dụ tính tay rồi đối chiếu với chương trình

Giải `2x² - 3x - 2 = 0`.

1. Hệ số: `a = 2`, `b = -3`, `c = -2`.
2. `Delta = (-3)² - 4 * 2 * (-2) = 9 + 16 = 25`, `√Delta = 5`.
3. `x1 = (3 - 5) / 4 = -0.5`, `x2 = (3 + 5) / 4 = 2`.
4. Đối chiếu bằng cách gõ `giai 2x^2 - 3x - 2 = 0`, kết quả phải là `x1 = -0.5, x2 = 2`.

### B.3. Định lý Viète: cách tự kiểm tra nghiệm

Với hai nghiệm `x1`, `x2` của `ax² + bx + c = 0`:

- Tổng: `x1 + x2 = -b / a`
- Tích: `x1 * x2 = c / a`

Ở ví dụ trên: tổng `-0.5 + 2 = 1.5` và `-b/a = 3/2 = 1.5`; tích `-0.5 * 2 = -1` và `c/a = -2/2 = -1`. Khớp.

### B.4. Vì sao đưa mọi phương trình về dạng "vế trái trừ vế phải"

Mọi phương trình một ẩn có thể viết lại dưới dạng `P(x) = 0` với `P` là một đa thức. PyClaw lấy `vế trái - vế phải` để tạo `P(x)`, nên không quan trọng `x` nằm ở vế nào. Ví dụ `2(x+1) = x + 5` thành `2x + 2 - x - 5 = x - 3`, nên `P(x) = x - 3` và nghiệm là `x = 3`.

### B.5. Số học dấu phẩy động và độ chính xác

Máy tính lưu số thực theo chuẩn IEEE 754 (kiểu `float` của Python), nên nhiều số thập phân không biểu diễn chính xác, ví dụ `0.1 + 0.2 = 0.30000000000000004`. PyClaw giảm ảnh hưởng này bằng cách làm tròn 10 chữ số thập phân trước khi so sánh hệ số với 0 và bằng cách in 6 chữ số có nghĩa.

---

## 20. Phụ lục C: Phiên làm việc mẫu đầy đủ

Một phiên trò chuyện điển hình (thời gian trong phần lịch sử chỉ mang tính minh họa):

```
========================================
       PYCLAW ASSISTANT
========================================
Nhập 'help' để xem hướng dẫn.
Nhập 'thoat' để kết thúc.

Bạn: xin chao
PyClaw: Chào bạn! Mình là PyClaw Assistant. Gõ 'help' để xem lệnh.

Bạn: tinh 12 * (3 + 2)
PyClaw: Kết quả: 60

Bạn: giai 2x + 6 = 0
PyClaw: Phương trình bậc 1: 2x + 6 = 0
Nghiệm: x = -3

Bạn: giai x^2 - 5x + 6 = 0
PyClaw: Phương trình bậc 2: 1x² - 5x + 6 = 0
Delta = 1
Hai nghiệm: x1 = 2, x2 = 3

Bạn: giai x^3 = 1
PyClaw: Không giải được: Số mũ phải là số nguyên 0, 1 hoặc 2.

Bạn: lichsu

--- 10 tin nhắn gần nhất ---
[2026-10-28T12:50:01] user: xin chao
[2026-10-28T12:50:01] assistant: Chào bạn! Mình là PyClaw Assistant. Gõ 'help' để xem lệnh.
[2026-10-28T12:50:09] user: tinh 12 * (3 + 2)
[2026-10-28T12:50:09] assistant: Kết quả: 60
[2026-10-28T12:50:20] user: giai 2x + 6 = 0
[2026-10-28T12:50:20] assistant: Phương trình bậc 1: 2x + 6 = 0
Nghiệm: x = -3
[2026-10-28T12:50:35] user: giai x^2 - 5x + 6 = 0
[2026-10-28T12:50:35] assistant: Phương trình bậc 2: 1x² - 5x + 6 = 0
Delta = 1
Hai nghiệm: x1 = 2, x2 = 3
[2026-10-28T12:50:41] user: giai x^3 = 1
[2026-10-28T12:50:41] assistant: Không giải được: Số mũ phải là số nguyên 0, 1 hoặc 2.

Bạn: thoat
PyClaw đã kết thúc.
```

---

## 21. Phụ lục D: Kiểm thử tự động bằng `unittest`

Ngoài danh sách kiểm thử thủ công ở mục 11, dự án có kèm file **`test_main.py`** gồm **19 bài kiểm thử tự động**.

### D.1. Cách chạy

1. Đặt `test_main.py` **cùng thư mục** với `main.py`.
2. Mở Terminal tại thư mục đó và chạy:

```powershell
cd D:\Pthiong
python -m unittest test_main -v
```

3. Kết quả mong đợi: mỗi bài in `ok`, cuối cùng là:

```
Ran 19 tests in 0.0xxs

OK
```

Nếu có bài thất bại, chương trình in `FAIL` kèm dòng so sánh giá trị mong đợi và giá trị thực tế.

### D.2. Các nhóm kiểm thử

| Lớp | Số bài | Kiểm tra |
|-----|--------|----------|
| `TestCalculate` | 5 | Phép toán cơ bản, chia cho 0, giới hạn số mũ và kết quả, từ chối đầu vào không phải số (kể cả `__import__('os')`), lỗi cú pháp |
| `TestSolveEquation` | 6 | Bậc 1, bậc 2 hai nghiệm, nghiệm kép, vô nghiệm, trường hợp suy biến, các đầu vào bị từ chối |
| `TestReply` | 5 | Chào hỏi, `help` có `giai`, không phân biệt hoa thường, câu không hiểu, thông báo lỗi |
| `TestDatabase` | 3 | Lịch sử rỗng, lưu rồi đọc lại đúng thứ tự, giới hạn 10 tin |

### D.3. Kiểm thử cơ sở dữ liệu không làm hỏng dữ liệu thật

Lớp `TestDatabase` tạo một **file tạm** bằng `tempfile.mkstemp`, trỏ `main.DB_NAME` sang file đó trong `setUp()`, rồi xóa file và khôi phục tên cũ trong `tearDown()`. Nhờ vậy chạy kiểm thử **không đụng đến** `pyclaw.db` chứa lịch sử thật của bạn.

### D.4. Vì sao kiểm thử được là nhờ cách tổ chức mã

- `reply()`, `calculate()`, `solve_equation()` là các **hàm thuần**: nhận chuỗi, trả về kết quả, không in, không ghi file. Gọi trực tiếp và so sánh kết quả là đủ.
- Dòng `if __name__ == "__main__":` giúp `import main` không khởi động vòng lặp nhập.

---

## 22. Phụ lục E: Đóng gói thành file `.exe` (Windows)

Mục tiêu: chạy PyClaw trên máy không cài Python. Dùng công cụ **PyInstaller**.

### Bước 1: Cài PyInstaller

```powershell
pip install pyinstaller
```

### Bước 2: Đóng gói

```powershell
cd D:\Pthiong
pyinstaller --onefile --name PyClaw main.py
```

- `--onefile`: gom tất cả vào **một file `.exe`** duy nhất.
- `--name PyClaw`: đặt tên file kết quả là `PyClaw.exe`.

### Bước 3: Lấy file kết quả

File nằm ở `D:\Pthiong\dist\PyClaw.exe`. Hai thư mục `build` và file `PyClaw.spec` sinh ra là phụ, có thể xóa.

### Bước 4: Chạy thử

Nhấp đúp `PyClaw.exe` hoặc chạy trong Terminal:

```powershell
.\dist\PyClaw.exe
```

### Lưu ý quan trọng

- File `pyclaw.db` được tạo **trong thư mục hiện hành** lúc chạy. Với `.exe`, nếu nhấp đúp thì đó thường là thư mục chứa file `.exe`. Nếu muốn cố định vị trí, dùng cách ở mục 14.6.
- Một số phần mềm diệt virus có thể cảnh báo nhầm file `.exe` do PyInstaller tạo ra. Đây là hiện tượng thường gặp, bạn có thể tự đóng gói từ mã nguồn của mình để yên tâm.
- Khi chạy bằng cách nhấp đúp, cửa sổ sẽ **đóng ngay** khi chương trình kết thúc. Nếu muốn giữ cửa sổ mở, hãy chạy `.exe` từ trong Terminal.
- Mỗi lần sửa `main.py` phải đóng gói lại.

---

## 23. Phụ lục F: Quản lý phiên bản bằng Git

### Bước 1: Khởi tạo

```powershell
cd D:\Pthiong
git init
```

### Bước 2: Tạo file `.gitignore`

Tạo file tên `.gitignore` cùng thư mục, nội dung:

```
pyclaw.db
__pycache__/
dist/
build/
*.spec
```

Lý do: không nên đưa **lịch sử trò chuyện riêng tư** (`pyclaw.db`), file tạm và file đóng gói lên kho mã.

### Bước 3: Lưu phiên bản đầu tiên

```powershell
git add main.py README.md test_main.py .gitignore
git commit -m "PyClaw: ban dau co tinh, giai phuong trinh, lich su"
```

### Bước 4: Quy trình mỗi khi sửa code

1. Sửa và lưu file.
2. Chạy kiểm thử: `python -m unittest test_main`.
3. `git add` và `git commit -m "mô tả ngắn thay đổi"`.

### Bước 5: Xem lịch sử thay đổi

```powershell
git log --oneline
```

---

## 24. Phụ lục G: Bài tập thực hành có hướng dẫn

Các bài sau giúp bạn hiểu code qua việc tự sửa. Mỗi bài có đáp án gợi ý đã được chạy thử.

> **Trước khi làm:** sao lưu `main.py` thành `main_backup.py`. Sau mỗi bài, thoát chương trình rồi chạy lại để thấy thay đổi.

### Bài 1: Thêm lệnh `ngay`

**Mục tiêu:** gõ `ngay` để xem ngày hôm nay.

1. Mở `main.py`, tìm hàm `reply()`.
2. Thêm nhánh sau vào **trước** câu trả lời mặc định ("Mình chưa hiểu..."):
```python
    if lower == "ngay":
        return datetime.now().strftime("Hôm nay là ngày %d/%m/%Y.")
```
3. Thêm dòng `"- ngay: xem ngày hôm nay\n"` vào chuỗi của `help`.
4. Lưu, chạy lại, thử `ngay`.

### Bài 2: Thêm lệnh `xoalichsu`

**Mục tiêu:** xóa lịch sử ngay trong chương trình.

1. Thêm hàm mới, đặt gần `show_history()`:
```python
def clear_history():
    with sqlite3.connect(DB_NAME) as db:
        db.execute("DELETE FROM messages")
```
2. Trong `main()`, thêm khối sau **cùng chỗ với khối xử lý `lichsu`** (trước `save_message("user", ...)`):
```python
        if message.lower() == "xoalichsu":
            clear_history()
            print("PyClaw: Đã xóa toàn bộ lịch sử.\n")
            continue
```
3. Thử: chat vài câu, gõ `xoalichsu`, rồi `lichsu`. Kết quả phải là "Chưa có lịch sử trò chuyện."

> **Cẩn thận:** lệnh này xóa vĩnh viễn, không hoàn tác được.

### Bài 3: Cho phép `lichsu 20` để chọn số tin cần xem

1. Sửa dòng khai báo hàm thành `def show_history(limit=10):`.
2. Trong câu lệnh SQL, đổi `LIMIT 10` thành `LIMIT ?` và truyền thêm tham số:
```python
        rows = db.execute(
            """
            SELECT role, content, created_at
            FROM messages ORDER BY id DESC LIMIT ?
            """,
            (limit,),
        ).fetchall()
```
3. Đổi dòng tiêu đề thành `print(f"\n--- {limit} tin nhắn gần nhất ---")`.
4. Trong `main()`, thay khối `if message.lower() == "lichsu":` bằng:
```python
        parts = message.lower().split()
        if parts and parts[0] == "lichsu":
            limit = 10
            if len(parts) > 1 and parts[1].isdigit():
                limit = max(1, min(int(parts[1]), 100))
            show_history(limit)
            continue
```
5. Thử `lichsu`, `lichsu 2`, `lichsu 50`. Con số được giới hạn trong khoảng 1 đến 100.

> **Chú ý:** nếu bạn sửa như vậy, bài kiểm thử `test_history_limit_is_10` vẫn đúng vì giá trị mặc định là 10.

### Bài 4: Hiển thị nghiệm phức khi Delta < 0

1. Thêm `import cmath` ở đầu file, dưới dòng `import ast`.
2. Trong `solve_equation()`, thay dòng `return header + "Delta < 0: ..."` bằng:
```python
            root = cmath.sqrt(delta)
            x1 = (-b - root) / (2 * a)
            x2 = (-b + root) / (2 * a)
            return header + f"Nghiệm phức: x1 = {x1:.4g}, x2 = {x2:.4g}"
```
3. Thử `giai x^2 + x + 1 = 0`. Kết quả:
```
Phương trình bậc 2: 1x² + 1x + 1 = 0
Delta = -3
Nghiệm phức: x1 = -0.5-0.866j, x2 = -0.5+0.866j
```
Python ký hiệu đơn vị ảo là `j` chứ không phải `i`.

> **Chú ý:** nếu thêm bài này, bài kiểm thử `test_quadratic_no_real_root` (kiểm tra chữ "vô nghiệm") sẽ **thất bại** vì nội dung đã đổi. Hãy sửa bài kiểm thử cho khớp hành vi mới, đây là một cách luyện tập kiểm thử rất tốt.

### Bài 5 (nâng cao): Cho phép hàm `sqrt` trong `tinh`

Gợi ý hướng làm, không có đáp án đầy đủ để bạn tự khám phá:

1. Trong `calculate()`, thêm xử lý nút `ast.Call` (lời gọi hàm).
2. Tạo một từ điển whitelist, ví dụ `FUNCTIONS = {"sqrt": math.sqrt}`.
3. Chỉ chấp nhận khi `node.func` là một `ast.Name` có tên nằm trong `FUNCTIONS` và chỉ có **đúng một đối số**.
4. Gọi hàm với giá trị `evaluate(node.args[0])`.
5. Kiểm tra bằng `tinh sqrt(16)` (phải ra `4.0`) và `tinh __import__('os')` (**phải bị từ chối**).

Nguyên tắc vàng: **chỉ cho phép những gì liệt kê rõ ràng**, tuyệt đối không cho gọi hàm tùy ý.

---

## 25. Phụ lục H: Các quyết định thiết kế

| Quyết định | Lý do |
|------------|-------|
| Một file `main.py` duy nhất | Dễ chép, dễ nộp bài, dễ đọc từ trên xuống dưới với dự án nhỏ |
| Dùng luật cố định thay vì AI | Chạy offline, miễn phí, kết quả dự đoán được, phù hợp mục đích học tập |
| Cây `ast` thay cho `eval()` | An toàn: chỉ cho phép đúng các phép toán đã liệt kê |
| SQLite thay cho file văn bản | Có sẵn trong Python, truy vấn được, không cần cài máy chủ |
| Tham số `?` trong SQL | Chống SQL Injection |
| `reply()` không in, không ghi file | Dễ kiểm thử, tách rõ phần "nghĩ" và phần "nói" |
| Đa thức dạng từ điển `{bậc: hệ số}` | Ngắn gọn, dễ cộng, nhân, và dễ mở rộng lên bậc cao hơn |
| Giới hạn số mũ và kích thước kết quả | Tránh treo máy khi người dùng nhập phép tính khổng lồ |
| Lưu cả tin nhắn bot không hiểu | Giữ nguyên vẹn lịch sử, có thể dùng để cải thiện bot sau này |

---

## 26. Phụ lục I: Bảng thuật ngữ

| Thuật ngữ | Giải thích |
|-----------|------------|
| **AST** (Abstract Syntax Tree) | Cây cú pháp trừu tượng: cách biểu diễn một biểu thức dưới dạng cây các nút |
| **Biểu thức chính quy (regex)** | Mẫu mô tả cách khớp chuỗi, dùng để tìm và thay thế văn bản |
| **Delta** | Biệt thức `b² - 4ac` của phương trình bậc 2, quyết định số nghiệm |
| **Đệ quy** | Hàm tự gọi chính nó để xử lý các phần nhỏ hơn |
| **Hàm thuần** | Hàm chỉ phụ thuộc vào đầu vào và không gây tác dụng phụ (không in, không ghi file) |
| **Danh sách trắng (whitelist)** | Danh sách những thứ **được phép**; mọi thứ ngoài danh sách bị từ chối |
| **Dấu phẩy động** | Cách máy tính lưu số thực, có thể sai số rất nhỏ |
| **ISO 8601** | Chuẩn định dạng thời gian, ví dụ `2026-10-28T12:51:55` |
| **SQL Injection** | Tấn công bằng cách chèn mã SQL vào dữ liệu nhập; phòng bằng tham số hóa |
| **SQLite** | Cơ sở dữ liệu nhỏ gọn lưu trong một file, không cần máy chủ |
| **Terminal** | Cửa sổ nhập lệnh bằng chữ |
| **UTF-8** | Bảng mã chữ, hỗ trợ đầy đủ tiếng Việt có dấu |
| **PATH** | Danh sách thư mục hệ điều hành tìm chương trình khi bạn gõ lệnh |
| **PyInstaller** | Công cụ đóng gói chương trình Python thành file `.exe` |
| **Unit test** | Bài kiểm thử tự động cho từng hàm nhỏ |

---

## 27. Giấy phép và đóng góp

- **Giấy phép:** dự án chưa chọn giấy phép. Nếu bạn muốn chia sẻ công khai, hãy chọn một giấy phép (ví dụ MIT) và thêm file `LICENSE` vào thư mục.
- **Đóng góp:** nếu muốn người khác góp ý, nên mô tả rõ cách báo lỗi: nêu phiên bản Python, lệnh đã gõ, kết quả mong đợi và kết quả thực tế.
- **Báo lỗi hiệu quả:** kèm theo thông báo lỗi nguyên văn hoặc ảnh chụp Terminal.

---

*PyClaw Assistant: dự án học tập viết bằng Python.*
