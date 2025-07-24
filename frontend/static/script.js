let token = localStorage.getItem('token');
const loginOverlay = document.getElementById('login');
const appDiv = document.getElementById('app');
const player = document.getElementById('player');
const songList = document.getElementById('song-list');
const current = document.getElementById('current');

function login() {
    token = document.getElementById('token').value;
    localStorage.setItem('token', token);
    init();
}

async function api(path, options = {}) {
    options.headers = options.headers || {};
    options.headers['Authorization'] = 'Bearer ' + token;
    const res = await fetch(path, options);
    if (res.status === 401) {
        loginOverlay.style.display = 'flex';
        appDiv.style.display = 'none';
        throw new Error('Unauthorized');
    }
    return res.json();
}

async function init() {
    if (!token) {
        loginOverlay.style.display = 'flex';
        return;
    }
    try {
        const songs = await api('/api/songs');
        songList.innerHTML = '';
        songs.forEach(song => {
            const li = document.createElement('li');
            li.textContent = song.title + ' - ' + song.artist;
            li.onclick = () => playSong(song.id, song.title);
            songList.appendChild(li);
        });
        loginOverlay.style.display = 'none';
        appDiv.style.display = 'block';
    } catch (e) {
        console.error(e);
    }
}

function playSong(id, title) {
    player.src = '/api/stream/' + id;
    player.play();
    current.textContent = title;
    api('/api/queue/' + id, {method:'POST'});
}

init();
