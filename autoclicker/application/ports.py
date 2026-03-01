"""Application ports (interfaces) used by high-level logic."""

from abc import ABC, abstractmethod
from typing import Callable

from autoclicker.domain import Scenario


class MouseMoveRecorderPort(ABC):
    @abstractmethod
    def start_recording(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def stop_recording(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_events(self) -> Scenario:
        raise NotImplementedError


class MouseClickRecorderPort(ABC):
    @abstractmethod
    def start_recording(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def stop_recording(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_events(self) -> Scenario:
        raise NotImplementedError


class ScenarioPlayerPort(ABC):
    @abstractmethod
    def play(self, scenario: Scenario, should_stop: Callable[[], bool] | None = None) -> None:
        raise NotImplementedError


class HotkeyManagerPort(ABC):
    @abstractmethod
    def register(self, combination: str, callback: Callable[[], None]) -> object:
        raise NotImplementedError

    @abstractmethod
    def unregister(self, hotkey_id: object) -> None:
        raise NotImplementedError


class UiPresenterPort(ABC):
    @abstractmethod
    def show_status(self, text: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_recording_started(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_recording_stopped(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_playback_started(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_playback_finished(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_error(self, text: str) -> None:
        raise NotImplementedError
