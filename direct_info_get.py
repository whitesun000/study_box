import os

def export_project_structure(root_dir, log_file):
    with open(log_file, 'w', encoding='utf-8') as f:
        for root, dirs, files in os.walk(root_dir):
            # 不要なディレクトリを除外(適宜変更)
            dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', '.venv', '.idea']]

            # ディレクトリの階層深さを計算
            level = root.replace(root_dir, '').count(os.sep)
            indent = ' ' * 4 * level
            f.write(f'{indent}{os.path.basename(root)}/\n')

            print(f"DEBUG: Scanning {root_dir} and saving to {log_file}")

            # ファイル名と中身を記録
            sub_indent = ' ' * 4 * (level + 1)
            for file in files:
                f.write(f'{sub_indent}{file}\n')

if __name__ == "__main__":
    target_directory = "."      # 今いるフォルダを対象にする
    output_filename = "project_log.log"

    export_project_structure(target_directory, output_filename)
    print("完了しました！")