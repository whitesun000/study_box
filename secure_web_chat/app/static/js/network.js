let socket;

/**
 * WebSocketの初期化と受信データの仕分けを担当
 * @param {Function} onChat - チャットメッセージを受け取る関数
 * @param {Function} onAlert - AI警告を受け取る関数
 * @param {Function} onReset - リセット命令を受け取る関数
 * @param {Function} onInfra - インフラ情報を受け取る関数
 */
export function initNetwork(onChat, onAlert, onReset, onInfra) {
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
            if (data.type === "chat") {
                onChat(data.user, data.message);
            }
            else if (data.type === "ai_alert") {
                onAlert(data.level, data.message);
            }
            else if (data.type === "reset_command") {
                onReset();
            }
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