import os
from pathlib import Path
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List, Dict

from .indexer import scan_music_directory
from .player import state

API_TOKEN = os.getenv("HINOTE_TOKEN")
if not API_TOKEN:
    raise RuntimeError(
        "HINOTE_TOKEN environment variable must be set before starting HiNote"
    )
MUSIC_DIR = os.getenv("MUSIC_DIR", "music")

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"

app = FastAPI(title="HiNote")
app.mount(
    "/static",
    StaticFiles(directory=str(FRONTEND_DIR / "static")),
    name="static",
)
templates = Jinja2Templates(directory=str(FRONTEND_DIR / "templates"))

songs: List[Dict] = scan_music_directory(MUSIC_DIR)


def verify_token(request: Request):
    token = request.headers.get("Authorization")
    if token != f"Bearer {API_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/songs", dependencies=[Depends(verify_token)])
async def get_songs():
    return songs


@app.get("/api/songs/{song_id}", dependencies=[Depends(verify_token)])
async def get_song(song_id: int):
    for song in songs:
        if song["id"] == song_id:
            return song
    raise HTTPException(status_code=404, detail="Song not found")


@app.get("/api/stream/{song_id}", dependencies=[Depends(verify_token)])
async def stream_song(song_id: int):
    for song in songs:
        if song["id"] == song_id:
            return FileResponse(song["path"], media_type="audio/*", filename=os.path.basename(song["path"]))
    raise HTTPException(status_code=404, detail="Song not found")


@app.get("/api/state", dependencies=[Depends(verify_token)])
async def get_state():
    return {
        "playlist": state.playlist,
        "current": state.current_song(),
        "playing": state.playing,
    }


@app.post("/api/play", dependencies=[Depends(verify_token)])
async def play():
    state.playing = True
    return {"status": "playing"}


@app.post("/api/pause", dependencies=[Depends(verify_token)])
async def pause():
    state.playing = False
    return {"status": "paused"}


@app.post("/api/next", dependencies=[Depends(verify_token)])
async def skip():
    state.next()
    return {"current": state.current_song()}


@app.post("/api/queue/{song_id}", dependencies=[Depends(verify_token)])
async def queue(song_id: int):
    state.add_to_playlist(song_id)
    return {"playlist": state.playlist}
