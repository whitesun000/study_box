import os

from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from utils.file_processor import export_project_structure

app = FastAPI()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    default_target = os.getcwd()
    default_log = os.path.join(default_target, "logs", "project_content.log")

    return templates.TemplateResponse(
        request = request,
        name = "index.html",
        context = {
            "result": None,
            "target_path": default_target,
            "output_path": default_log
        }
    )

@app.post("/scan", response_class=HTMLResponse)
async def run_scan(
    request: Request, 
    target_path: str = Form(...),
    output_path: str = Form(...),
    include_content: bool = Form(False)
):
    if not target_path or not os.path.exists(target_path):
        result_message = "エラー：有効なスキャン対象フォルダを入力してください。"
    else:
        try:
            # logsフォルダがない場合に備えて親ディレクトリを作成
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # 既存のロジックを実行
            export_project_structure(target_path, output_path, export_content=include_content)
            result_message = f"完了！ログを保存しました：{output_path}"
        except Exception as e:
            result_message = f"エラーが発生しました: {e}"

        return templates.TemplateResponse(
            request = request,
            name = "index.html",
            context = {
                "result": result_message,
                "target_path": target_path,
                "output_path": output_path
            }
        )