import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import time
import os
import tempfile
import plotly.express as px

# Hàm để lấy giá vàng từ trang web
def get_gold_prices(date):
    url = f'https://www.24h.com.vn/gia-vang-hom-nay-c425.html?ngaythang={date}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    data = []

    table = soup.find('table', class_='gia-vang-search-data-table')

    if table is None:
        print(f'No data found for {date}. Check the page content.')
        print(response.text) 
        return data

    rows = table.find_all('tr')

    for row in rows:
        name_cell = row.find('td', class_='colorGrey')
        if name_cell and 'SJC' in name_cell.text:
            name = 'SJC'
            selling_price = row.find_all('span', class_='fixW')[0].text.strip().replace(',', '')
            buying_price = row.find_all('span', class_='fixW')[1].text.strip().replace(',', '')
            data.append({
                'Tên loại vàng': name,
                'Giá bán': int(selling_price) if selling_price.isdigit() else None,
                'Giá mua': int(buying_price) if buying_price.isdigit() else None,
                'Nguồn dữ liệu': 'www.24h.com.vn',
                'date': date
            })
    
    return data

# Hàm để tạo danh sách các ngày trong khoảng thời gian, chỉ lấy đến ngày hiện tại
def get_dates_in_range(start_date, end_date):
    delta = timedelta(days=1)
    dates = []
    current_date = start_date
    while current_date <= end_date:
        dates.append(current_date.strftime('%Y-%m-%d'))
        current_date += delta
    return dates

# Hàm để thu thập dữ liệu và lưu vào CSV
def collect_and_save_data(start_date, end_date, progress_callback):
    dates = get_dates_in_range(start_date, end_date)
    all_data = []

    for date in dates:
        progress_callback(f'Đang thu thập dữ liệu cho ngày: {date}')  # Cập nhật log cho giao diện Streamlit
        day_data = get_gold_prices(date)
        seen = set()
        unique_data = []

        for entry in day_data:
            identifier = f"{entry['Tên loại vàng']}_{entry['date']}"
            if identifier not in seen:
                seen.add(identifier)
                unique_data.append(entry)

        all_data.extend(unique_data)
        time.sleep(1)  # Chờ 1 giây giữa các lần yêu cầu

    df = pd.DataFrame(all_data)
    return df

# Streamlit interface
def main():
    st.title("Ứng dụng Lấy Dữ Liệu Giá Vàng")

    # Nhập ngày bắt đầu và ngày kết thúc
    start_date = st.date_input("Ngày bắt đầu", datetime(2025, 7, 1))
    end_date = st.date_input("Ngày kết thúc", datetime.today())

    # Dòng log tiến trình
    log_text = st.empty()

    # Nút để bắt đầu lấy dữ liệu
    if st.button("Lấy Dữ Liệu"):
        with st.spinner('Đang thu thập dữ liệu...'):
            df = collect_and_save_data(start_date, end_date, progress_callback=lambda msg: log_text.text(msg))
        
        if df.empty:
            st.error("Không có dữ liệu cho khoảng thời gian này.")
        else:
            # Hiển thị preview dữ liệu
            st.subheader("Preview Dữ Liệu")
            st.dataframe(df)

            # Vẽ biểu đồ với Plotly
            fig = px.line(df, x='date', y=['Giá bán', 'Giá mua'], 
                          title='Biểu đồ giá vàng theo thời gian',
                          labels={'date': 'Ngày', 'value': 'Giá', 'variable': 'Loại giá'})
            st.plotly_chart(fig)

            # Sử dụng thư mục tạm thời hệ thống để lưu file CSV
            temp_dir = tempfile.gettempdir()  # Lấy thư mục tạm thời hệ thống
            output_path = os.path.join(temp_dir, "gold_prices.csv")
            df.to_csv(output_path, index=False)

            # Cung cấp nút tải file CSV
            with open(output_path, "rb") as f:
                st.download_button(
                    label="Tải file CSV về máy",
                    data=f,
                    file_name="gold_prices.csv",
                    mime="text/csv"
                )

# Chạy ứng dụng Streamlit
if __name__ == "__main__":
    main()
