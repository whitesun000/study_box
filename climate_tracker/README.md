# Climate Tracker 🌍

過去の気象データを分析し、現在と比較するためのWebアプリケーションです。
FastAPI(Python)とOpen-Meteo APIを活用し、特定の場所の数年前の天気を可視化します。

## 🛠 機能
- **過去データ検索**: 緯度・経度を指定して、指定年数の過去の天気を即座に取得。
- **インタラクティブ・マップ**: Leaflet.jsを使用し、分析対象地点を地図上で視覚的に確認。
- **詳細分析**: 最高/最低気温、湿度、天気アイコンを美しく表示。
- **モダンなUI**: Tailwind CSSを使用した、ダークモード基調のレスポンシブデザイン。

## 📂 ディレクトリ構成
リファクタリングを意識し、関心の分離（SoC）を適用したディレクトリ構造を採用しています。

```text
climate_tracker/
├── app/
│   ├── main.py          # FastAPIエントリーポイント（ルーティング・マウント）
│   ├── services/        # ビジネスロジック（天気データの取得・計算）
│   ├── static/          # 静的ファイル（CSS, JS, 画像）
│   │   └── js/
│   │       └── map.js   # 地図制御ロジック（分離済み）
│   └── templates/       # Jinja2テンプレート（HTML）
├── data/                # ローカルデータ保管用（予定）
├── .gitignore           # Git管理除外設定
└── README.md            # 本ファイル
```

## 🚀使い方
#### 1. 環境構築(Docker推奨)
```
docker -compose up-d
```
#### 2. アプリへのアクセス
ブラウザで ```http://localhost:8000``` を開きます。

#### 3. 操作方法
1. 左側のパネルに調べたい場所の「緯度」「経度」を入力します。
2. 「比較する年数」を入力します。
3. 「データ更新」ボタンを押すと、右側のパネルに過去のデータと地図が表示されます。

## 🧬技術スタック
- **Backend**: Python 3.12/FastAPI
- **Frontend**: HTML5/JavaScript(IIFE pattern)/TailwindCSS
- **Maps**: Leaflet.js/OpneStreetMap
- **Data Source**: Open-Meteo API
