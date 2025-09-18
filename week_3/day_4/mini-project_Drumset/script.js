function playSound(keyCode) {
    const audio = document.querySelector(`audio[data-key="${keyCode}"]`);
    const drum = document.querySelector(`.drum[data-key="${keyCode}"]`);
    if (!audio || !drum) return;
        audio.currentTime = 0;
        audio.play();
        drum.classList.add('playing');
        setTimeout(() => drum.classList.remove('playing'), 100);
}
window.addEventListener('keydown', (e) => playSound(e.keyCode));
document.querySelectorAll('.drum').forEach(drum => {
    drum.addEventListener('click', () => {
        playSound(drum.getAttribute('data-key'));
    });
});