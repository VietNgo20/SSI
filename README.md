# SSI

## 29/5: Done
    - API cho phép pgười dùng nhập các ngày nghỉ lễ trong năm, hệ thống xử lý và lưu trữ lại vào database.
    - API trả danh sách ngày nghỉ lễ + cuối tuần(T7 & CN) trong năm.

## 30/5: Done
    - API cho phép người dùng nhập mã chứng khoán/ danh sách mã chứng khoán (https://iboard.ssi.com.vn/):
        + thực hiện crawl dữ liệu hồ sơ công ty.
        + thực hiện crawl dữ liệu cổ đông của mã chứng khoán đó (50 cổ đông lớn nhất).
        + thực hiện crawl dữ liệu lịch sử giá của mã chứng khoán đó (50 ngày gần nhất).

## 31/5: Done
    - API trả ra toàn bộ thông tin về mã chứng khoán và danh sách cổ đông của mã chứng khoán đó.
    - API trả ra lịch sử giao dịch của 1 mã chứng khoán
    - API trả danh sách mã chứng khoán phái sinh theo ngày mà người dùng nhập, mỗi mã phái sinh sẽ có những thông tin:
        {
            "symbol": "VN30F2306",
            "code": "VN30F1M",
            "expired_date": "15/06/2023"
        }

## 1/6: Plan
    - Containerize app bằng Docker
