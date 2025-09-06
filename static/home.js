document.addEventListener("DOMContentLoaded", () => {
    const neonCursor = document.createElement('div');
    neonCursor.classList.add('neon-cursor');
    document.body.appendChild(neonCursor);

    document.addEventListener('mousemove', (e) => {
        neonCursor.style.left = `${e.clientX}px`;
        neonCursor.style.top = `${e.clientY}px`;

        const dot = document.createElement('div');
        dot.classList.add('neon-trail-dot');
        dot.style.left = `${e.clientX}px`;
        dot.style.top = `${e.clientY}px`;
        document.body.appendChild(dot);

        setTimeout(() => {
            dot.remove();
        }, 800);
    });
});
