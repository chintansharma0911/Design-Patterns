# music_system.py
from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum
import random
from typing import List, Dict, Optional


# -----------------------
# Domain Models
# -----------------------
class Song:
    def __init__(self, id: int, title: str, artist: str, path: Optional[str] = None):
        self.id = id
        self.title = title
        self.artist = artist
        self.path = path

    def __repr__(self):
        return f"Song({self.id}, '{self.title}', '{self.artist}')"


class Playlist:
    def __init__(self, name: str):
        self.name = name
        self.songs: List[Song] = []

    def add_song(self, song: Song):
        self.songs.append(song)

    def remove_song(self, song_id: int):
        self.songs = [s for s in self.songs if s.id != song_id]

    def get_songs(self) -> List[Song]:
        return self.songs.copy()

    def __repr__(self):
        return f"Playlist('{self.name}', {len(self.songs)} songs)"


# -----------------------
# Play Strategies (Strategy Pattern)
# -----------------------
class StrategyType(Enum):
    SEQUENTIAL = 1
    RANDOM = 2
    CUSTOM = 3


class PlayStrategy(ABC):
    @abstractmethod
    def set_playlist(self, playlist: Playlist):
        pass

    @abstractmethod
    def has_next(self) -> bool:
        pass

    @abstractmethod
    def next(self) -> Optional[Song]:
        pass

    @abstractmethod
    def previous(self) -> Optional[Song]:
        pass

    @abstractmethod
    def current(self) -> Optional[Song]:
        pass

    @abstractmethod
    def add_to_next(self, song: Song):
        pass


class SequentialPlayStrategy(PlayStrategy):
    def __init__(self):
        self.playlist: Optional[Playlist] = None
        self.index: int = -1

    def set_playlist(self, playlist: Playlist):
        self.playlist = playlist
        self.index = -1

    def has_next(self) -> bool:
        if not self.playlist:
            return False
        return self.index + 1 < len(self.playlist.songs)

    def next(self) -> Optional[Song]:
        if not self.playlist or not self.has_next():
            return None
        self.index += 1
        return self.playlist.songs[self.index]

    def previous(self) -> Optional[Song]:
        if not self.playlist or self.index - 1 < 0:
            return None
        self.index -= 1
        return self.playlist.songs[self.index]

    def current(self) -> Optional[Song]:
        if not self.playlist or self.index < 0 or self.index >= len(self.playlist.songs):
            return None
        return self.playlist.songs[self.index]

    def add_to_next(self, song: Song):
        if self.playlist:
            insert_at = min(self.index + 1, len(self.playlist.songs))
            self.playlist.songs.insert(insert_at, song)


class RandomPlayStrategy(PlayStrategy):
    def __init__(self):
        self.playlist: Optional[Playlist] = None
        self.queue: List[Song] = []
        self.history: List[Song] = []

    def set_playlist(self, playlist: Playlist):
        self.playlist = playlist
        self.queue = playlist.get_songs().copy()
        random.shuffle(self.queue)
        self.history = []

    def has_next(self) -> bool:
        return len(self.queue) > 0

    def next(self) -> Optional[Song]:
        if not self.has_next():
            return None
        song = self.queue.pop(0)
        self.history.append(song)
        return song

    def previous(self) -> Optional[Song]:
        if not self.history:
            return None
        # move last from history to front of queue and return previous item
        last = self.history.pop()
        # previous is now last item in history
        prev = self.history[-1] if self.history else None
        if prev:
            return prev
        return None

    def current(self) -> Optional[Song]:
        return self.history[-1] if self.history else None

    def add_to_next(self, song: Song):
        self.queue.insert(0, song)


class CustomPlayStrategy(PlayStrategy):
    # Custom behavior (for example user-defined order). Here we maintain a custom queue.
    def __init__(self):
        self.custom_queue: List[Song] = []
        self.index = -1

    def set_playlist(self, playlist: Playlist):
        # default custom order is same as playlist, but user can reorder
        self.custom_queue = playlist.get_songs().copy()
        self.index = -1

    def has_next(self) -> bool:
        return self.index + 1 < len(self.custom_queue)

    def next(self) -> Optional[Song]:
        if not self.has_next():
            return None
        self.index += 1
        return self.custom_queue[self.index]

    def previous(self) -> Optional[Song]:
        if self.index - 1 < 0:
            return None
        self.index -= 1
        return self.custom_queue[self.index]

    def current(self) -> Optional[Song]:
        if self.index < 0 or self.index >= len(self.custom_queue):
            return None
        return self.custom_queue[self.index]

    def add_to_next(self, song: Song):
        insert_at = min(self.index + 1, len(self.custom_queue))
        self.custom_queue.insert(insert_at, song)


# -----------------------
# Strategy Manager (Singleton)
# -----------------------
class StrategyManager:
    _instance = None

    def __init__(self):
        self._strategies: Dict[StrategyType, PlayStrategy] = {
            StrategyType.SEQUENTIAL: SequentialPlayStrategy(),
            StrategyType.RANDOM: RandomPlayStrategy(),
            StrategyType.CUSTOM: CustomPlayStrategy(),
        }

    @classmethod
    def instance(cls) -> StrategyManager:
        if cls._instance is None:
            cls._instance = StrategyManager()
        return cls._instance

    def get_strategy(self, stype: StrategyType) -> PlayStrategy:
        # Return a fresh instance or a reusable one depending on needs.
        return self._strategies[stype]


# -----------------------
# Playlist Manager (Singleton)
# -----------------------
class PlaylistManager:
    _instance = None

    def __init__(self):
        self.playlists: Dict[str, Playlist] = {}

    @classmethod
    def instance(cls) -> PlaylistManager:
        if cls._instance is None:
            cls._instance = PlaylistManager()
        return cls._instance

    def create_playlist(self, name: str) -> Playlist:
        pl = Playlist(name)
        self.playlists[name] = pl
        return pl

    def get_playlist(self, name: str) -> Optional[Playlist]:
        return self.playlists.get(name)


# -----------------------
# Audio Output Device Abstraction & Adapters
# -----------------------
class IAudioOutputDevice(ABC):
    @abstractmethod
    def play_audio(self, song: Song):
        pass

    @abstractmethod
    def stop(self):
        pass


class BluetoothSpeakerAPI:
    # Pretend external API with its own signature
    def play_sound_via_bluetooth(self, data: str):
        print(f"[Bluetooth API] playing: {data}")


class WiredSpeakerAPI:
    def play_sound_via_cable(self, data: str):
        print(f"[Wired Speaker API] playing: {data}")


class HeadphoneAPI:
    def play_sound_in_headphones(self, data: str):
        print(f"[Headphones API] playing: {data}")


class BluetoothSpeakerAdapter(IAudioOutputDevice):
    def __init__(self):
        self.api = BluetoothSpeakerAPI()

    def play_audio(self, song: Song):
        payload = f"{song.title} - {song.artist}"
        self.api.play_sound_via_bluetooth(payload)

    def stop(self):
        print("[BluetoothSpeakerAdapter] stop")


class WiredSpeakerAdapter(IAudioOutputDevice):
    def __init__(self):
        self.api = WiredSpeakerAPI()

    def play_audio(self, song: Song):
        payload = f"{song.title} - {song.artist}"
        self.api.play_sound_via_cable(payload)

    def stop(self):
        print("[WiredSpeakerAdapter] stop")


class HeadphonesAdapter(IAudioOutputDevice):
    def __init__(self):
        self.api = HeadphoneAPI()

    def play_audio(self, song: Song):
        payload = f"{song.title} - {song.artist}"
        self.api.play_sound_in_headphones(payload)

    def stop(self):
        print("[HeadphonesAdapter] stop")


# -----------------------
# Device Factory & Manager (Singleton)
# -----------------------
class DeviceType(Enum):
    BLUETOOTH = 1
    WIRED = 2
    HEADPHONES = 3


class DeviceFactory:
    @staticmethod
    def create_device(dtype: DeviceType) -> IAudioOutputDevice:
        if dtype == DeviceType.BLUETOOTH:
            return BluetoothSpeakerAdapter()
        elif dtype == DeviceType.WIRED:
            return WiredSpeakerAdapter()
        elif dtype == DeviceType.HEADPHONES:
            return HeadphonesAdapter()
        else:
            raise ValueError("Unknown device type")


class DeviceManager:
    _instance = None

    def __init__(self):
        self.connected_device: Optional[IAudioOutputDevice] = None

    @classmethod
    def instance(cls) -> DeviceManager:
        if cls._instance is None:
            cls._instance = DeviceManager()
        return cls._instance

    def connect(self, dtype: DeviceType):
        self.connected_device = DeviceFactory.create_device(dtype)
        print(f"[DeviceManager] Connected device: {dtype.name}")

    def get_device(self) -> Optional[IAudioOutputDevice]:
        return self.connected_device

    def disconnect(self):
        if self.connected_device:
            self.connected_device.stop()
        self.connected_device = None
        print("[DeviceManager] Disconnected device")


# -----------------------
# Audio Engine
# -----------------------
class AudioEngine:
    def __init__(self):
        self.device_manager = DeviceManager.instance()

    def play(self, song: Song):
        device = self.device_manager.get_device()
        if not device:
            print("[AudioEngine] No device connected. Cannot play.")
            return
        device.play_audio(song)

    def stop(self):
        device = self.device_manager.get_device()
        if device:
            device.stop()


# -----------------------
# MusicPlayerFacade (Singleton)
# -----------------------
class MusicPlayerFacade:
    _instance = None

    def __init__(self):
        self.playlist_manager = PlaylistManager.instance()
        self.strategy_manager = StrategyManager.instance()
        self.device_manager = DeviceManager.instance()
        self.audio_engine = AudioEngine()
        self.current_strategy: Optional[PlayStrategy] = None
        self.current_playlist: Optional[Playlist] = None
        self.is_playing = False

    @classmethod
    def instance(cls) -> MusicPlayerFacade:
        if cls._instance is None:
            cls._instance = MusicPlayerFacade()
        return cls._instance

    # Playlist operations
    def create_playlist(self, name: str) -> Playlist:
        return self.playlist_manager.create_playlist(name)

    def add_song_to_playlist(self, playlist_name: str, song: Song):
        pl = self.playlist_manager.get_playlist(playlist_name)
        if not pl:
            raise ValueError("Playlist not found")
        pl.add_song(song)
        print(f"[Facade] Added {song} to playlist '{playlist_name}'")

    # Strategy operations
    def set_play_strategy(self, stype: StrategyType, playlist_name: str):
        pl = self.playlist_manager.get_playlist(playlist_name)
        if not pl:
            raise ValueError("Playlist not found")
        strat = self.strategy_manager.get_strategy(stype)
        # NOTE: we clone or reinitialize strategy instance if needed; here we just reuse
        strat.set_playlist(pl)
        self.current_strategy = strat
        self.current_playlist = pl
        print(f"[Facade] Strategy set to {stype.name} for playlist '{playlist_name}'")

    # Device operations
    def connect_device(self, dtype: DeviceType):
        self.device_manager.connect(dtype)

    def disconnect_device(self):
        self.device_manager.disconnect()

    # Playback operations
    def play(self):
        if not self.current_strategy:
            print("[Facade] No strategy/playlist set. Cannot play.")
            return
        next_song = self.current_strategy.next()
        if not next_song:
            print("[Facade] Nothing to play.")
            return
        self.audio_engine.play(next_song)
        self.is_playing = True
        print(f"[Facade] Playing: {next_song}")

    def pause(self):
        if self.is_playing:
            self.audio_engine.stop()
            self.is_playing = False
            print("[Facade] Paused")

    def next(self):
        if not self.current_strategy:
            print("[Facade] No strategy set.")
            return
        next_song = self.current_strategy.next()
        if next_song:
            self.audio_engine.play(next_song)
            print(f"[Facade] Next: {next_song}")
        else:
            print("[Facade] No next song.")

    def previous(self):
        if not self.current_strategy:
            print("[Facade] No strategy set.")
            return
        prev_song = self.current_strategy.previous()
        if prev_song:
            self.audio_engine.play(prev_song)
            print(f"[Facade] Previous: {prev_song}")
        else:
            print("[Facade] No previous song.")

    def add_to_next(self, song: Song):
        if not self.current_strategy:
            print("[Facade] No strategy set.")
            return
        self.current_strategy.add_to_next(song)
        print(f"[Facade] Added to next: {song}")


# -----------------------
# Demo / Usage
# -----------------------
if __name__ == "__main__":
    facade = MusicPlayerFacade.instance()

    # Create playlist and songs
    pl = facade.create_playlist("Favorites")
    s1 = Song(1, "Take Five", "Dave Brubeck")
    s2 = Song(2, "Imagine", "John Lennon")
    s3 = Song(3, "Bohemian Rhapsody", "Queen")
    s4 = Song(4, "Billie Jean", "Michael Jackson")

    facade.add_song_to_playlist("Favorites", s1)
    facade.add_song_to_playlist("Favorites", s2)
    facade.add_song_to_playlist("Favorites", s3)
    facade.add_song_to_playlist("Favorites", s4)

    # Connect a device
    facade.connect_device(DeviceType.BLUETOOTH)

    # Set play strategy and play
    facade.set_play_strategy(StrategyType.SEQUENTIAL, "Favorites")
    facade.play()        # plays first
    facade.next()        # plays second
    facade.add_to_next(Song(99, "New Song", "New Artist"))
    facade.next()        # plays the added song (if inserted)
    facade.previous()    # goes back
    facade.pause()       # pause

    # Switch to random strategy
    facade.set_play_strategy(StrategyType.RANDOM, "Favorites")
    facade.play()
    facade.next()
    facade.disconnect_device()
