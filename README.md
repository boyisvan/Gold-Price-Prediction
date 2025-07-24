# Ứng dụng Dự Đoán Giá Vàng

## Tổng quan
Đây là ứng dụng web sử dụng Streamlit để thu thập dữ liệu giá vàng SJC từ trang web www.24h.com.vn, trực quan hóa dữ liệu và dự đoán giá bán vàng trong tương lai bằng mô hình Random Forest. Người dùng có thể chọn khoảng thời gian, nhập giá bán kỳ vọng và tải dữ liệu về dưới dạng CSV.

## Tính năng
- Thu thập dữ liệu giá vàng SJC theo ngày từ www.24h.com.vn
- Hiển thị bảng dữ liệu và biểu đồ giá vàng theo thời gian
- Dự đoán ngày giá bán vàng đạt mức kỳ vọng bằng Random Forest
- Cho phép tải dữ liệu về dưới dạng file CSV

## Công nghệ sử dụng
- Python 3
- [Streamlit](https://streamlit.io/) (giao diện web)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) (thu thập dữ liệu web)
- [Pandas](https://pandas.pydata.org/) (xử lý dữ liệu)
- [Plotly](https://plotly.com/python/) (vẽ biểu đồ)
- [scikit-learn](https://scikit-learn.org/) (Random Forest)

## Hướng dẫn cài đặt
1. **Clone dự án về máy:**
   ```bash
   git clone <https://github.com/boyisvan/Gold-Price-Prediction>
   cd giavang
   ```
2. **Cài đặt các thư viện cần thiết:**
   
   Nếu dùng pip:
   ```bash
   pip install streamlit requests beautifulsoup4 pandas plotly scikit-learn numpy
   ```

3. **Chạy ứng dụng:**
   ```bash
   streamlit run app.py
   ```

4. **Sử dụng:**
   - Truy cập địa chỉ hiển thị trên terminal (thường là http://localhost:8501)
   - Chọn ngày bắt đầu, ngày kết thúc, nhập giá bán kỳ vọng (nếu muốn dự đoán)
   - Nhấn "Lấy Dữ Liệu" để xem bảng, biểu đồ và tải file CSV

## Ghi chú
- Ứng dụng chỉ thu thập dữ liệu giá vàng SJC.
- Nếu không có dữ liệu cho ngày chọn, kiểm tra lại kết nối mạng hoặc thử lại sau.
- Dữ liệu được lưu tạm thời và có thể tải về dưới dạng CSV.
## Demo sản phẩm
<div style="display:flex; justify-content:center;">
  <img width="407" height="824" alt="image" src="https://github.com/user-attachments/assets/43d7107f-db0f-4bf8-b3b2-8201500c42f4" />
</div>
<img width="1100" height="550" alt="image" src="https://github.com/user-attachments/assets/80d5692e-b995-4eda-bf1e-014cf1fed221" />

## Liên hệ
- boyisvan (Ducvancoder-0587282880)
- Email: protector01rem@gmail.com
