import re

class AIDetector:
    def __init__(self):
        # 1. 致命的な攻撃パターン（正規表現）
        # (?i) は大文字小文字を無視するフラグ
        self.danger_patterns = [
            r"(?i)SELECT\s+.*\s+FROM",                      # SELECT ...FROM の構造
            r"(?i)UNION\s+SELECT",                          # UNION 攻撃
            r"(?i)DROP\s+TABLE",                            # テーブル削除
            r"(?i)SLEEP\s*\(\d+\)",                         # 時間差攻撃
            r"(?i)OR\s+['\"].*['\"]=.*['\"]",               # ' OR '1'='1 などの恒等式
            r"--",                                          # コメントアウト
            r"/\*.*\*/",                                    # インラインコメント
        ]

        # 2. 不審な単語 (正規表現)
        self.suspicious_patterns = [
            r"攻撃", r"ハック", r"脆弱性", r"侵入", r"ハッカー"
        ]
    
    def analyze_message(self, message: str, username: str):
        """
        メッセージを正規表現でスキャンして判定結果を返す
        """
        
        # 検証で失敗した　"SEL/ + ECT" のような難読化対策：
        # 記号を除去した「正規化テキスト」もチェック対象にする
        normalized_text = re.sub(r"[^a-zA-Z0-9]", "", message)
        normalized_text_jp = re.sub(r"[^a-zA-Z0-9あ-んア-ンー-龠]", "", message)

        # 1. 強力な攻撃コードの検知
        for pattern in self.danger_patterns:
            if (re.search(pattern, message) or 
                re.search(pattern, normalized_text) or 
                re.search(pattern, normalized_text_jp)):

                return {
                    "level": "CRITICAL",
                    "alert": f"[AI] 致命的な攻撃パターン検知: シグネチャ一致",
                }
        
        # 2. 不審な単語の検知
        for pattern in self.suspicious_patterns:
            if re.search(pattern, message):
                return {
                    "level": "WARNING",
                    "alert": f"[AI] 不穏な言動を検知: パターン一致",
                }
        
        # 3. 特定ユーザー (Hacker) への重点監視
        if username == "Hacker":
            return {
                "level": "MONITORING",
                "alert": "[AI] 監視対象ユーザーによる通信を記録中...",
            }
        
        return None

detector = AIDetector()
