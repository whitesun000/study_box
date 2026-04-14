from typing import Optional
from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.services.weather_service import WeatherService

app = FastAPI()

# 1. HTMLと静的ファイル（画像など）を使うための準備
# app/static フォルダがなくても動くように念のため static は設定しておきます
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

service = WeatherService()

# 2. トップページ（"/"）にアクセスしたときの処理
@app.get("/", response_class=HTMLResponse)
async def read_root(
    request: Request,
    lat: float = 35.6895,
    lon: float = 139.6917,
    years: Optional[str] = Query(None)
):
    try:
        if years is not None and years.strip() != "":
            safe_years = int(years)
        else:
            safe_years = 10
    except ValueError:
        safe_years = 10

    # サービスからデータ取得
    weather_data = service.get_comparison_data(lat, lon, safe_years)

    print(f"DEBUG DATA: {weather_data}")

    # templates/index.html を使って画面を表示する
    return templates.TemplateResponse(
        request = request,
        name = "index.html",
        context = {"data": weather_data}
    )

# 3.データだけを返す窓口
@app.get("/compare")
def compare_weather(lat: float, lon: float, years: int = 10):
    # yearsパラメータがない場合はデフォルトで10年前を計算
    data = service.get_comparison_data(lat, lon, years)
    return data