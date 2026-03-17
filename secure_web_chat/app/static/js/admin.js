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
                document.getElementById(`slot-${i}`).innerHTML = `<p>MONITORING: ${user}</p>`;
                break;
            }
        }
    }
}