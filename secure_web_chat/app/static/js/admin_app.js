import { handleScreenUpdate, updateAdminInterface } from './admin.js';
import { initNetwork } from './network.js';

window.addEventListener('load', () => {
    console.log("[ADMIN] 監視パネルを初期化中...");

    initNetwork(
        // チャット受信（管理画面でも一応表示する場合）
        (user, message) => { console.log(`Chat: ${user}: ${message}`); },
        // AI警告受信
        (level, alert) => { console.warn(`[AI] ${level}: ${alert}`); },
        // リセット命令
        () => { console.log("Reset received"); },
        // インフラステータス受信
        (data) => { 
            updateAdminInterface(data.connections, data.blocked, data.user_list);
        },
        (data) => {
            handleScreenUpdate(data);
        }
    );
});