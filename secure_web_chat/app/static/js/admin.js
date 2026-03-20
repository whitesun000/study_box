// スロット管理（誰がどの枠を使っているか）
let monitoredUsers = {};

export function updateAdminInterface(connections, blocked, userList) {
    // 統計の更新
    document.getElementById('connection-count').textContent = connections;
    document.getElementById('blocked-count').textContent = blocked;

    // ユーザーリストの更新
    const listEl = document.getElementById('admin-user-list');
    listEl.innerHTML = '';
    userList.forEach(user => {
        const li = document.createElement('li');
        const isChecked = monitoredUsers[user] ? 'checked' : '';
        li.innerHTML = `
            <label>
                <input type="checkbox" ${isChecked} onchange="toggleMonitor('${user}')" />
                ${user}
            </label>
        `;
        listEl.appendChild(li);
    });
}


// 映像を更新する関数
export function handleScreenUpdate(userDate) {
    const { user, image } = userDate;

    // そのユーザーが今、監視対象（スロットに割り当て済み）かチェック
    if (monitoredUsers[user]) {
        const slotNum = monitoredUsers[user];
        const slotEl = document.getElementById(`slot-${slotNum}`);
        
        // スロット内に img タグがあるか確認。なければ作る。
        let img = slotEl.querySelector('img');
        if (!img) {
            slotEl.innerHTML = `<span class="user-label">LIVE: ${user}</span>`
            img = document.createElement('img');
            img.className = 'monitor-stream';
            Object.assign(img.style, { width: '100%', height: '100%', objectFit: 'contain' })
            slotEl.appendChild(img);
        }

        // 画像を更新 (Base64データを直接srcに入れる)
        img.src = image;
    }
}


// チェックボックス操作時の処理
window.toggleMonitor = function(user) {
    if (monitoredUsers[user]) {
        const slotId = `slot-${monitoredUsers[user]}`;
        document.getElementById(slotId).innerHTML = `<p>NO SIGNAL</p>`;
        delete monitoredUsers[user];
    } else {
        for (let i = 1; i <= 4; i++) {
            if (!Object.values(monitoredUsers).includes(i)) {
                monitoredUsers[user] = i;
                document.getElementById(`slot-${i}`).innerHTML = `<p>CONNECTING: ${user}...</p>`;
                break;
            }
        }
    }
};