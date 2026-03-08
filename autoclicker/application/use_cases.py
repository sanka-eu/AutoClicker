"""Use cases for recording and playback orchestration."""

from dataclasses import dataclass, field
from typing import Callable, Optional

from autoclicker.application.ports import (
    HotkeyManagerPort,
    MouseClickRecorderPort,
    MouseMoveRecorderPort,
    ScenarioPlayerPort,
)
from autoclicker.domain import Scenario


@dataclass
class RecordingSessionState:
    is_recording: bool = False
    stop_hotkey_id: Optional[object] = None
    last_scenario: Scenario = field(default_factory=list)


class StartRecordingUseCase:
    def __init__(
        self,
        move_recorder: MouseMoveRecorderPort,
        click_recorder: MouseClickRecorderPort,
        hotkeys: HotkeyManagerPort,
        state: RecordingSessionState,
        stop_hotkey: str = "ctrl+p",
    ) -> None:
        self._move_recorder = move_recorder
        self._click_recorder = click_recorder
        self._hotkeys = hotkeys
        self._state = state
        self._stop_hotkey = stop_hotkey

    def execute(self, stop_callback: Callable[[], None]) -> None:
        if self._state.is_recording:
            return

        self._move_recorder.start_recording()
        self._click_recorder.start_recording()
        hotkey_id = self._hotkeys.register(self._stop_hotkey, stop_callback)

        self._state.is_recording = True
        self._state.stop_hotkey_id = hotkey_id

    def get_stop_hotkey(self) -> str:
        return self._stop_hotkey

    def set_stop_hotkey(self, hotkey: str) -> None:
        normalized = hotkey.strip().lower()
        if not normalized:
            raise ValueError("Stop hotkey cannot be empty")
        self._stop_hotkey = normalized

    def capture_hotkey(self) -> str:
        return self._hotkeys.capture_hotkey()


class StopRecordingUseCase:
    def __init__(
        self,
        move_recorder: MouseMoveRecorderPort,
        click_recorder: MouseClickRecorderPort,
        hotkeys: HotkeyManagerPort,
        state: RecordingSessionState,
    ) -> None:
        self._move_recorder = move_recorder
        self._click_recorder = click_recorder
        self._hotkeys = hotkeys
        self._state = state

    def execute(self) -> Scenario:
        if not self._state.is_recording:
            return list(self._state.last_scenario)

        self._move_recorder.stop_recording()
        self._click_recorder.stop_recording()

        if self._state.stop_hotkey_id is not None:
            self._hotkeys.unregister(self._state.stop_hotkey_id)

        scenario = self._move_recorder.get_events() + self._click_recorder.get_events()
        scenario.sort(key=lambda event: event.timestamp)

        self._state.is_recording = False
        self._state.stop_hotkey_id = None
        self._state.last_scenario = scenario
        return list(scenario)


class PlayScenarioUseCase:
    def __init__(self, player_factory: Callable[[float, bool], ScenarioPlayerPort]) -> None:
        self._player_factory = player_factory

    def execute(
        self,
        scenario: Scenario,
        speed_multiplier: float,
        loop_playback: bool,
        should_stop: Callable[[], bool] | None = None,
    ) -> None:
        player = self._player_factory(speed_multiplier, loop_playback)
        player.play(scenario, should_stop=should_stop)
