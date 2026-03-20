const layout = document.querySelector('.game-layout');
const dragX = document.getElementById('drag-x');
const dragY = document.getElementById('drag-y');

// --- 横方向の（左右）のリサイズ ---
if (dragX) {
    dragX.addEventListener('mousedown', function(e) {
        e.preventDefault();
        document.addEventListener('mousemove', resizeX);
        document.addEventListener('mouseup', stopResize);
    });
}


function resizeX(e) {
    if (!layout) return;
    // 右端からの距離でサイドバーの幅を計算
    const sidebarWidth = window.innerWidth - e.clientX;
    // 最小幅と最大幅を制限（任意）
    if (sidebarWidth > 150 && sidebarWidth < 600) {
        layout.style.gridTemplateColumns = `1fr 6px ${sidebarWidth}px`;
    }
}

// --- 縦方向（上下）のリサイズ ---
if (dragY) {
    dragY.addEventListener('mousedown', function(e) {
        e.preventDefault();
        document.addEventListener('mousemove', resizeY);
        document.addEventListener('mouseup', stopResize);
    });
}

function resizeY(e) {
    if (!layout) return;
    // 下端から距離でログエリアの高さを計算
    const footerHeight = window.innerHeight - e.clientY; 
    if (footerHeight > 50 && footerHeight < 500) {
        layout.style.gridTemplateRows = `1fr 6px ${footerHeight}px`;
    }
}

function stopResize() {
    document.removeEventListener('mousemove', resizeX);
    document.removeEventListener('mousemove', resizeY);
}