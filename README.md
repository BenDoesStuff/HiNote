# HiNote

HiNote is a lightweight local music streaming server and web-based player. It indexes your music library and lets you play tracks from a mobile browser on your local network.

## Features

- FastAPI backend that scans `MUSIC_DIR` (default `music/`) for FLAC, WAV, ALAC, and MP3 files.
- Token-based authentication for API access.
- REST API to list songs, stream tracks, queue items, and control playback state.
- Minimal mobile-friendly web UI.

## Usage

1. Install dependencies and install HiNote locally (so the `hinote` module is available anywhere):

```bash
pip install -r requirements.txt
pip install -e .
```

2. Place your music files under the `music/` directory or set the `MUSIC_DIR` environment variable.

3. Start the server:

```bash
HINOTE_TOKEN=yourtoken python -m hinote
```

4. On your mobile device, navigate to `http://<server-ip>:8000`, enter the token, and start playing your music.

## Notes

This is a minimal reference implementation. Advanced features like persistent state, output device selection, or casting are left as future improvements.
