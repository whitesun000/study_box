import os
from pathlib import Path

def is_text_file(file_path):
    text_extensions = {'.py', '.txt', '.html', '.css', '.md', '.json', '.js', '.php'}
    return Path(file_path).suffix in text_extensions

def export_project_structure(root_dir, log_file, export_content=True):
    # 不要なディレクトリを除外(適宜変更)
    exclude_dirs = {'.git', '__pycache__', '.venv', '.idea', '.vscode'}

    # ログファイルの親ディレクトリが存在しない場合は作成
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    with open(log_file, 'w', encoding='utf-8') as f:
        f.write("PROJECT STRUCTURE & CONTENT LOG\n")
        f.write("="*50 + "\n\n")

        for root, dirs, files in os.walk(root_dir):
            # ディレクトリの階層深さを計算
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            level = root.replace(root_dir, '').count(os.sep)
            indent = ' ' * 4 * level
            f.write(f'{indent}📁 {os.path.basename(root)}/\n')

            # ファイル名と中身を記録
            sub_indent = ' ' * 4 * (level + 1)
            for file in files:
                file_path = os.path.join(root, file)
                f.write(f'{sub_indent}📄{file}\n')

                # export_content が True の場合のみ中身を書き込む
                if export_content and is_text_file(file_path):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as code_f:
                            content = code_f.read()
                            f.write(f"{sub_indent}--- CONTENT START: {file} ---\n")
                            for line in content.splitlines():
                                f.write(f"{sub_indent}  {line}\n")
                            f.write(f"{sub_indent}--- CONTENT END ---\n\n")
                    except Exception as e:
                        f.write(f"{sub_indent}[Error: {e}\n\n]")