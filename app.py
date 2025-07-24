import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import time
import os
import tempfile
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor
import numpy as np

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

# Hàm dự đoán giá bán kỳ vọng bằng RandomForest
def predict_gold_price(df, expected_price):
    # Chuyển đổi ngày thành số (để sử dụng trong mô hình học máy)
    df['date'] = pd.to_datetime(df['date'])
    df['days_since'] = (df['date'] - df['date'].min()).dt.days

    X = df[['days_since', 'Giá mua', 'Giá bán']]  
    y = df['Giá bán']  

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    future_days = np.array([df['days_since'].max() + i for i in range(1, 31)]).reshape(-1, 1)
    future_buying_prices = np.full((30, 1), df['Giá mua'].iloc[-1])  
    future_selling_prices = np.full((30, 1), df['Giá bán'].iloc[-1]) 

    future_data = np.hstack((future_days, future_buying_prices, future_selling_prices))

    future_prices = model.predict(future_data)

    predicted_dates = pd.date_range(df['date'].max() + timedelta(days=1), periods=30, freq='D')

    predicted_df = pd.DataFrame({
        'Ngày dự đoán': predicted_dates,
        'Giá bán dự đoán': future_prices
    })

    closest_date = predicted_df.iloc[(predicted_df['Giá bán dự đoán'] - expected_price).abs().argmin()]

    accuracy = 100 - abs((closest_date['Giá bán dự đoán'] - expected_price) / expected_price) * 100
    return closest_date, accuracy

def main():
    st.title("Ứng dụng Lấy Dữ Liệu Giá Vàng và Dự Đoán")

    today = datetime.today().date()
    start_date = st.date_input("Ngày bắt đầu", datetime(2025, 7, 1), max_value=today)
    end_date = st.date_input("Ngày kết thúc", today, max_value=today)

    if start_date > end_date:
        st.error("Ngày kết thúc không thể trước ngày bắt đầu!")
        return

    expected_price = st.number_input("Nhập giá bán kỳ vọng", min_value=0)

    log_text = st.empty()

    if st.button("Lấy Dữ Liệu"):
        with st.spinner('Đang thu thập dữ liệu...'):
            df = collect_and_save_data(start_date, end_date, progress_callback=lambda msg: log_text.text(msg))
        
        if df.empty:
            st.error("Không có dữ liệu cho khoảng thời gian này.")
        else:
            st.subheader("Preview Dữ Liệu")
            st.dataframe(df)

            fig = px.line(df, x='date', y=['Giá bán', 'Giá mua'], 
                          title='Biểu đồ giá vàng theo thời gian',
                          labels={'date': 'Ngày', 'value': 'Giá', 'variable': 'Loại giá'})
            st.plotly_chart(fig)

            if expected_price > 0:
                predicted_date, accuracy = predict_gold_price(df, expected_price)
                st.subheader(f"Ngày vàng đạt giá bán {expected_price}: {predicted_date['Ngày dự đoán'].strftime('%Y-%m-%d')}")
                # st.write(f"Tỷ lệ chính xác: {accuracy:.2f}%")

            temp_dir = tempfile.gettempdir()  
            output_path = os.path.join(temp_dir, "gold_prices.csv")
            df.to_csv(output_path, index=False)

            with open(output_path, "rb") as f:
                st.download_button(
                    label="Tải file CSV về máy",
                    data=f,
                    file_name="gold_prices.csv",
                    mime="text/csv"
                )

if __name__ == "__main__":
    main()
