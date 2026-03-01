"""Dependency composition root."""

from autoclicker.application import (
    AppController,
    PlayScenarioUseCase,
    RecordingSessionState,
    StartRecordingUseCase,
    StopRecordingUseCase,
)
from autoclicker.infrastructure.hotkeys import KeyboardHotkeyManager
from autoclicker.infrastructure.mouse import (
    PyAutoGuiMoveRecorder,
    PyAutoGuiScenarioPlayer,
    PynputClickRecorder,
)
from autoclicker.infrastructure.ui import TkinterMainWindow


def build_app() -> TkinterMainWindow:
    state = RecordingSessionState()

    move_recorder = PyAutoGuiMoveRecorder(sample_interval=0.05)
    click_recorder = PynputClickRecorder()
    hotkeys = KeyboardHotkeyManager()

    start_recording = StartRecordingUseCase(
        move_recorder=move_recorder,
        click_recorder=click_recorder,
        hotkeys=hotkeys,
        state=state,
        stop_hotkey="ctrl+p",
    )
    stop_recording = StopRecordingUseCase(
        move_recorder=move_recorder,
        click_recorder=click_recorder,
        hotkeys=hotkeys,
        state=state,
    )
    play_scenario = PlayScenarioUseCase(
        player_factory=lambda speed_multiplier, loop_playback: PyAutoGuiScenarioPlayer(
            speed_multiplier=speed_multiplier,
            loop_playback=loop_playback,
        )
    )

    controller = AppController(
        start_recording_use_case=start_recording,
        stop_recording_use_case=stop_recording,
        play_scenario_use_case=play_scenario,
        session_state=state,
    )

    window = TkinterMainWindow(controller)
    controller.set_presenter(window)
    return window
