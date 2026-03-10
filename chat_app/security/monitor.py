import time
from collections import defaultdict

class SecurityMonitor:
    def __init__(self, threshold=100):
        # IPごとのスコア
        self.scores = defaultdict(int)
        # IPごとの最終操作時間
        self.last_action_time = {}
        # ブラックリスト（遮断済みのIP）
        self.blacklist = set()
        # ブロックしきい値
        self.threshold = threshold
    
    def id_blocked(self, ip):
        """ 対象のIPが既にブラックリストに入っているかチェック """
        return ip in self.blacklist

    def add_score(self, ip, points, reason):
        """ スコアを加算し、しきい値を超えたらブラックリストに登録 """
        if self.is_blocked(ip):
            return True
        
        self.scores[ip] += points
        print(f"[!] 警告: {ip} に {points}点加算。理由: {reason} (現在: {self.scores[ip]}点)")

        # 100点を超えたらブラックリスト入り
        if self.scores[ip] >= 100:
            print(f"[!!!] 遮断: {ip} をブラックリストに登録しました。")
            self.blacklist.add(ip)
            return True # ブロック対象
        return False
    
    def check_speed(self, ip):
        """ 送信スピードが速すぎないかチェック (0.2秒以内はTrueを返す) """
        now = time.time()
        if ip in self.last_action_time:
            interval = now - self.last_action_time[ip]
            if interval < 0.2:  # 0.2秒以内の連続送信
                return True
        
        # 最終操作時間を更新
        self.last_action_time[ip] = now
        return False

        
    
