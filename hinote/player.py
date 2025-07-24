from typing import List, Optional
from dataclasses import dataclass, field

@dataclass
class PlayerState:
    playlist: List[int] = field(default_factory=list)
    current_index: int = 0
    playing: bool = False

    def current_song(self) -> Optional[int]:
        if self.playlist and 0 <= self.current_index < len(self.playlist):
            return self.playlist[self.current_index]
        return None

    def next(self):
        if self.playlist:
            self.current_index = (self.current_index + 1) % len(self.playlist)

    def add_to_playlist(self, song_id: int):
        self.playlist.append(song_id)

state = PlayerState()
