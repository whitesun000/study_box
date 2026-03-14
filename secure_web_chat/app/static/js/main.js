import { sendSocketMessage } from './network.js';

export function displayChatMessage(user, messageText) {
    const chatBox = document.getElementById('chat-box');
    const entry = document.createElement('div');
    entry.className = 'message';
    entry.textContent = `${user}: ${messageText}`;
    chatBox.appendChild(entry);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// 画面上のログを消去する
export function clearChatLog() {
    const chatBox = document.getElementById('chat-box');
    if (chatBox) {
        chatBox.innerHTML = "";
    }
}

// サーバーへリセット命令を送る
export function requestChatReset() {
    sendSocketMessage({ type: "reset_request" });
}

// メッセージ送信関数 (JSON形式で送るように修正)
export function sendMessage() {
    const input = document.getElementById("messageText");
    if (input.value) {
        sendSocketMessage({
            // 文字列ではなくオブジェクトを送る
            type: "chat",
            message: input.value
        });
        input.value = "";
    }
}