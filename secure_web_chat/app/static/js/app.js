// 各ファイルをモジュールとして読み込む
// ※jsファイル側でも関数の前に 'export' を付ける必要があります
import { appendLog, toggleSecurity } from './lab.js';
import { clearChatLog, displayChatMessage, requestChatReset, sendMessage } from './main.js';
import { initMonitor } from './monitor.js';
import { initNetwork } from './network.js';
import './resizer.js';

// --- HTMLの onclick から呼べるようにグローバルに公開する ---
window.sendMessage = sendMessage;
window.toggleSecurity = toggleSecurity;
window.requestChatReset = requestChatReset;

// --- ページ読み込み時の初期化処理 ---
window.addEventListener('load', () => {
    console.log("[SYSTEM] アプリケーションを初期化中...");

    // ネットワーク (WebSocket) の開始
    // main.js などの関数を渡して、受信時の挙動をセットする
    if (typeof initNetwork === 'function') {
        initNetwork(
            // 1. チャット受信
            (user, message) => {
                displayChatMessage(user, message);
            },
            // 2. AI警告受信
            (level, alertMessage) => {
                const type = level === "CRITICAL" ? "danger" : "info";
                appendLog(`[AI-DETECTOR] ${alertMessage}`, type);
            },
            // 3. リセット命令受信時の動作
            () => {
                clearChatLog();
                appendLog("[SYSTEM] 管理者によりチャット履歴が消去されました。", "success");
            }
        )
    }

    // 監視機能の初期化
    initMonitor();
});