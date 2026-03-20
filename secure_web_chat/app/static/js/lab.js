// ログ画面にメッセージを表示する関数
export function appendLog(message, type = 'info') {
    const logWindow = document.getElementById('log-window');
    if (!logWindow) return;

    const entry = document.createElement('div');
    
    // 時刻を取得
    const now = new Date();
    const timeStr = `[${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}]`;

    // タイプによって色を変える
    if (type === 'danger') entry.style.color = '#ff4d4d';
    if (type === 'success') entry.style.color = '#2ecc71';

    entry.textContent = `${timeStr} ${message}`;
    logWindow.appendChild(entry);

    // 常に最新のログが見えるように自動スクロール
    logWindow.scrollTop = logWindow.scrollHeight;
}

// サーバーセキュリティモードを切り替える関数
export async function toggleSecurity(mode) {
    try {
        // Python側の @router.post("/toggle_security") を呼び出す
        const response = await fetch('/auth/toggle_security', { method: 'POST'});
        const data = await response.json();
        
        // サーバーから返ってきた「今の状態」をそのままログに出す
        if (data.status === 'VULNERABLE') {
            appendLog("------------------------------------------------------");
            appendLog("[WARNING] セキュリティレベル：LOW", "danger");
            appendLog("[SYSTEM] SQLインジェクションが有効になりました。", "danger");
        } else {
            appendLog("------------------------------------------------------");
            appendLog("[WARNING] セキュリティレベル：HIGH", "success");
            appendLog("プリペアドステートメントが有効です。", "success");
        }
    } catch (error) {
        appendLog("[ERROR] サーバーとの通信に失敗しました。", "dander");
    }
}

export async function checkInitialStatus() {
    const response = await fetch('/auth/security_status');
    const data = await response.json();
    
    // ログイン直後の「初期状態ログ」として1回だけ出す
    const modeText = data.status === 'VULNERABLE' ? "脆弱性モード (ACTIVE)" : "セキュアモード (SAFE)";
    const modeColor = data.status === 'VULNERABLE' ? "danger" : "success";
    appendLog(`[DEBUG] システム監視開始：${modeText}`, modeColor);
}

// ページ読み込み時に実行
window.addEventListener('load', () => {
    // 1. 状態チェックを先に動かす（ログイン画面がある画面（チャット画面）の時だけ初期チェックを行う）
    if (document.getElementById('log-window')) {
        checkInitialStatus();

        // 2. ハッキング演出 (Hackerという名前が含まれる場合のみ)
        const userInfo = document.querySelector('.user-info');
        if (userInfo && userInfo.textContent.includes('Hacker')) {
            appendLog("====================================", "danger");
            appendLog("[SYSTEM] 警告：不正な認証を検知しました", "danger");
            appendLog("[SYSTEM] ログインユーザー：UNKNOWN (SQL Injection)", "danger");
            appendLog("[SYSTEM] データベースの権限が奪取されました。", "danger");
            appendLog("------------------------------------", "success");
            appendLog("ハッキング成功：システムを掌握しました。", "success");
            appendLog("====================================", "success");
        }
    }
});

    


