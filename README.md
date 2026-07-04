# 🛠️ File Processor (ZSTD & AES)

Một công cụ Python nhỏ gọn hỗ trợ nén, giải nén dữ liệu bằng **ZSTD** và mã hóa, giải mã bảo mật bằng **AES**. 

---

## 🚀 Tính năng chính

* ⚡ **Nén & Giải nén tốc độ cao:** Sử dụng thuật toán `ZSTD`.
* 🔒 **Bảo mật dữ liệu:** Mã hóa và giải mã với chuẩn mã hóa nâng cao `AES`.
* 🎨 **Giao diện dòng lệnh trực quan:** Hỗ trợ hiển thị màu sắc (ANSI escape codes) giúp dễ dàng theo dõi.

---

## 🛠️ Hướng dẫn Sử dụng

Để xem hướng dẫn nhanh trong terminal, bạn có thể gọi hàm `help()` có sẵn trong công cụ.

### 1. Chế độ Tự động (Auto Mode)
Tự động phát hiện và xử lý file dựa trên định dạng hoặc cấu trúc sẵn có.
```python
auto(file_path)
```

### 2. Chế độ Thủ công (Mode)
Xử lý file theo chế độ đã chọn

| Tùy chọn Mode | Loại tác vụ | Mô tả chi tiết |
| :--- | :--- | :--- |
| **`COM_ZSTD`** | `Compression` | Nén tệp tin đích bằng thuật toán ZSTD để giảm dung lượng. |
| **`DEC_ZSTD`** | `Decompression` | Giải nén tệp tin đã nén bằng ZSTD về trạng thái gốc ban đầu. |
| **`ENC_AES`** | `Encryption` | Mã hóa bảo mật tệp tin bằng thuật toán mã hóa AES. |
| **`DEC_AES`** | `Decryption` | Giải mã tệp tin đã được mã hóa bằng AES trở lại bình thường. |

```python
mode(file_path, mode)
```