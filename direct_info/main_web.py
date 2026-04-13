import uvicorn

if __name__ == "__main__":
    # webフォルダ内のapp.pyにある「app」を読み込んで起動する
    uvicorn.run("web.app:app", host="0.0.0.0", port=8000, reload=True)