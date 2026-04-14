import requests
from datetime import datetime, timedelta

class WeatherService:
    def __init__(self):
        # 過去データ取得用のベースURL
        self.archive_url = "https://archive-api.open-meteo.com/v1/archive"

    def get_comparison_data(self, lat: float, lon: float, years_back: int):
        # 1. 日付の計算
        past_date = datetime.now() - timedelta(days=365 * years_back)
        date_str = past_date.strftime("%Y-%m-%d")

        # 2. Open-Meteo APIに送るパラメータを設定
        # ここでは「その日の最高気温（temperature_2m_max）」を要求
        params = {
            "latitude": lat,
            "longitude": lon,
            "start_date": date_str,
            "end_date": date_str,
            "daily": [
                "temperature_2m_max",
                "temperature_2m_min",
                "relative_humidity_2m_max",
                "weather_code"
            ],
            "timezone": "GMT"
        }

        # 天気コードのマッピング
        weather_map = {
            0: {"label": "快晴", "icon": "☀️"},
            1: {"label": "晴れ", "icon": "🌤️"},
            2: {"label": "時々曇り", "icon": "⛅"},
            3: {"label": "くもり", "icon": "☁️"},
            45: {"label": "霧", "icon": "🌫️"},
            51: {"label": "小雨", "icon": "🌦️"},
            61: {"label": "雨", "icon": "🌧️"},
            71: {"label": "雪", "icon": "❄️"},
            95: {"label": "雷雨", "icon": "⛈️"},
        }

        # 3. 実際にAPIを叩く
        response = requests.get(self.archive_url, params=params)
        data = response.json()
        daily = data.get("daily", {})

        code = daily.get("weather_code",[0])[0]
        weather_info = weather_map.get(code, {"label": "不明", "icon": "❓"})

        # 4. 結果を整理して返す
        # APIのレスポンス構造に合わせてデータを抽出
        
        return {
            "location": {"lat": lat, "lon": lon},
            "comparison": {
                "years_back": years_back,
                "date": date_str,
                "max_temp": daily.get("temperature_2m_max", [0])[0],
                "min_temp": daily.get("temperature_2m_min", [0])[0],
                "humidity": daily.get("relative_humidity_2m_max", [0])[0],
                "weather_label": weather_info["label"],
                "weather_icon": weather_info["icon"]
            }
        }

