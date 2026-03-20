let socket;

/**
 * WebSocketの初期化と受信データの仕分けを担当
 * @param {Function} onChat - チャットメッセージを受け取る関数
 * @param {Function} onAlert - AI警告を受け取る関数
 * @param {Function} onReset - リセット命令を受け取る関数
 * @param {Function} onInfra - インフラ情報を受け取る関数
 * @param {Function} onScreenUpdate - 画面キャプチャデータを受け取る関数
 */
export function initNetwork(onChat, onAlert, onReset, onInfra, onScreenUpdate) {
    // 1. プロトコルの決定（ws か wss か）
    const isHttps = window.location.protocol === 'https:'
    const protocol = isHttps ? 'wss:' : 'ws:';
    
    // 2. 正確なURLの組み立て
    const wsUrl = `${protocol}//${window.location.host}/ws`;

    console.log("[DEBUG] Connecting to:", wsUrl);
    socket = new WebSocket(wsUrl);

    socket.onmessage = function(event) {
        try {
            const data = JSON.parse(event.data);

            // データのタイプに応じてコールバック関数を呼び出す（仕分け）

            // 1. 通常のチャットメッセージ
            if (data.type === "chat") {
                onChat(data.user, data.message);
            }

            // 2. 🛡️ 重要：画面キャプチャデータの転送（監視用）
            // Python側の type: "screen_data" と完全に一致させる
            else if (data.type === "screen_data") {
                if (onScreenUpdate) {
                    onScreenUpdate(data);
                }
            }

            // 3. AIによる攻撃検知アラート
            else if (data.type === "ai_alert") {
                onAlert(data.level, data.message);
            }

            // 4. 管理者からの全消去命令
            else if (data.type === "reset_command") {
                onReset();
            }

            // 5. インフラの稼働状況（接続数など）
            else if (data.type == "infra_status") {
                if (onInfra) {
                    onInfra(data);
                }
            }

        } catch (e) {
            console.error("JSONの解析に失敗しました:", event.data)
        }
    };

    socket.onclose = function() {
        console.log("WebSocket接続が終了しました。");
    };

    socket.onerror = function() {
        console.log("WebSocketでエラーが発生しました:", error);
    };
}

/**
 * サーバーへオブジェクトをJSON化して送信
 */
export function sendSocketMessage(dataObject) {
    if (socket && socket.readyState === WebSocket.OPEN) {
        const jsonString = JSON.stringify(dataObject);
        socket.send(jsonString);
    }
}