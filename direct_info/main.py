import os
from utils.file_processor import export_project_structure

def main():
    # ユーザーに入力を促す
    print("=== Project Content Extractor ===")
    user_input = input("スキャンしたいフォルダのパスを入力してください（空欄で現在のフォルダ）: ").strip()

    # 1. スキャン対象
    # ※入力が空欄ならカレントディレクトリ（.）、入力があればそのパスを使用
    target = user_input if user_input else "."

    # 入力されたパスが存在するかチェック
    if not os.path.exists(target):
        print(f"エラー: 指定されたパス '{target}' は存在しません。")
        return

    # 2. 保存先フォルダとファイル名の設定
    log_dir = "logs"
    log_filename = "project_content.log"

    # 3. ログフォルダが存在しない場合に自動で作る
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        print(f"フォルダを作成しました: {log_dir}")

    # 4. フルパス生成（例: logs/project_content.log）
    log_path = os.path.join(log_dir, log_filename)

    print(f"スキャンを開始します: {os.path.abspath(target)}")
    export_project_structure(target, log_path)
    print(f"完了しました！保存先: {os.path.abspath(log_path)}")

if __name__ == "__main__":
    main()
