import csv
import json
from datetime import datetime
import requests


def fetch_weather_data():
    # 範例：抓取中央氣象署的開放資料（或是任何公開 API）
    # 這裡以抓取公共 API 的 JSON 資料為例
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 25.0375,  # 台北市緯度
        "longitude": 121.5637,  # 台北市經度
        "current_weather": True,
        "timezone": "Asia/Taipei",
    }

    print("正向 API 發送請求中...")
    try:
        response = requests.get(url, params=params, timeout=10)
    except requests.RequestException as e:
        print(f"請求失敗：{e}")
        return None

    # 修正：使用 status_code 屬性
    if response.status_code == 200:  # 確保請求成功
        data = response.json()
        current = data.get("current_weather", {})

        # 整理要儲存的數據格式
        result = {
            "fetch_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "temperature": current.get("temperature"),
            "windspeed": current.get("windspeed"),
            "weathercode": current.get("weathercode"),
        }
        return result
    else:
        print(f"抓取失敗，HTTP 狀態碼: {response.status_code}")
        return None


def save_to_json(data, filename="weather_data.json"):
    # 讀取舊資料並累加新數據
    existing_data = []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            existing_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        pass  # 檔案不存在或是空檔案時忽略

    existing_data.append(data)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)
    print(f"已更新資料至 {filename}")


def save_to_csv(data, filename="weather_data.csv"):
    file_exists = False
    try:
        with open(filename, "r", encoding="utf-8"):
            file_exists = True
    except FileNotFoundError:
        pass

    fieldnames = ["fetch_time", "temperature", "windspeed", "weathercode"]

    # 開啟檔案並寫入（以 append 模式）
    with open(filename, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()  # 若檔案不存在則寫入標題
        writer.writerow(data)
    print(f"已更新資料至 {filename}")


if __name__ == "__main__":
    weather_info = fetch_weather_data()
    if weather_info:
        save_to_json(weather_info)
        save_to_csv(weather_info)
        print("爬蟲執行完成，資料寫入成功！")
