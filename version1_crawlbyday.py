import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import time

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

def get_dates_in_july(year):
    today = datetime.today().date()
    start_date = datetime(year, 7, 1).date()
    end_date = datetime(year, 7, 31).date()
    if today < end_date:
        end_date = today

    delta = timedelta(days=1)
    dates = []
    current_date = start_date
    while current_date <= end_date:
        dates.append(current_date.strftime('%Y-%m-%d'))
        current_date += delta
    return dates
def collect_and_save_data(year):
    dates = get_dates_in_july(year)
    all_data = []

    for date in dates:
        print(f'Collecting data for {date}...')
        day_data = get_gold_prices(date)
        seen = set()
        unique_data = []

        for entry in day_data:
            identifier = f"{entry['name']}_{entry['date']}"
            if identifier not in seen:
                seen.add(identifier)
                unique_data.append(entry)

        all_data.extend(unique_data)
        time.sleep(1) 
    df = pd.DataFrame(all_data)
    output_path = f'gold_prices_{year}_07_sjc.csv'
    df.to_csv(output_path, index=False)
    print(f'Data saved to {output_path}')
if __name__ == '__main__':
    collect_and_save_data(2025)  
