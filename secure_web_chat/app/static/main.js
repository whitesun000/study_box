// WebSocketのインスタンス用変数
let ws;

// ページ読み込み時にWebSocketを接続
window.onload = function() {
    // 現在のホスト名に基づいたWebSocket URLを生成 (ws://127.0.0.1:8000/ws)
    const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws:';
    ws = new WebSocket(`${protocol}//${window.location.host}/ws`);

    // メッセージを受信時の処理
    ws.onmessage = function(event) {
        const chatBox = document.getElementById('chat-box');
        const message = document.createElement('div');
        message.className = 'message';
        message.textContent = event.data;
        chatBox.appendChild(message);

        // 常に最新のメッセージが見えるようにスクロール
        chatBox.scrollTop = chatBox.scrollHeight;
    };

    ws.onclose = function() {
        console.log("WebSocket接続が終了しました。");
    };
};

// メッセージ送信関数
function sendMessage() {
    const input = document.getElementById("messageText");
    if (ws && input.value) {
        ws.send(input.value);   // サーバーへ送信
        input.value = "";
    }
}