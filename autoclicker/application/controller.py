"""High-level controller handling UI events."""

import threading

from autoclicker.application.ports import UiPresenterPort
from autoclicker.application.use_cases import (
    PlayScenarioUseCase,
    RecordingSessionState,
    StartRecordingUseCase,
    StopRecordingUseCase,
)


class NullPresenter(UiPresenterPort):
    def show_status(self, text: str) -> None:
        return

    def on_recording_started(self) -> None:
        return

    def on_recording_stopped(self) -> None:
        return

    def on_playback_started(self) -> None:
        return

    def on_playback_finished(self) -> None:
        return

    def on_error(self, text: str) -> None:
        return


class AppController:
    def __init__(
        self,
        start_recording_use_case: StartRecordingUseCase,
        stop_recording_use_case: StopRecordingUseCase,
        play_scenario_use_case: PlayScenarioUseCase,
        session_state: RecordingSessionState,
        presenter: UiPresenterPort | None = None,
    ) -> None:
        self._start_recording_use_case = start_recording_use_case
        self._stop_recording_use_case = stop_recording_use_case
        self._play_scenario_use_case = play_scenario_use_case
        self._session_state = session_state
        self._presenter: UiPresenterPort = presenter or NullPresenter()
        self._lock = threading.Lock()
        self._playback_thread: threading.Thread | None = None
        self._playback_stop_event = threading.Event()

    def set_presenter(self, presenter: UiPresenterPort) -> None:
        self._presenter = presenter

    def get_stop_record_hotkey(self) -> str:
        return self._start_recording_use_case.get_stop_hotkey()

    def capture_stop_record_hotkey(self) -> str:
        with self._lock:
            if self._session_state.is_recording:
                raise RuntimeError("Cannot capture hotkey while recording")
        return self._start_recording_use_case.capture_hotkey()

    def on_change_stop_hotkey_requested(self, new_hotkey: str) -> bool:
        with self._lock:
            if self._session_state.is_recording:
                self._presenter.on_error("Cannot change hotkey while recording")
                return False

            try:
                self._start_recording_use_case.set_stop_hotkey(new_hotkey)
            except ValueError as exc:
                self._presenter.on_error(str(exc))
                return False

            hotkey = self._start_recording_use_case.get_stop_hotkey()
            self._presenter.show_status(f"Stop hotkey set to: {hotkey}")
            return True

    def on_start_record_clicked(self) -> None:
        with self._lock:
            if self._session_state.is_recording:
                self._presenter.show_status("Recording is already running")
                return

            hotkey = self._start_recording_use_case.get_stop_hotkey()
            try:
                self._start_recording_use_case.execute(self.on_stop_record_requested)
            except Exception as exc:  # pragma: no cover
                self._presenter.on_error(f"Failed to start recording: {exc}")
                return
            self._presenter.on_recording_started()
            self._presenter.show_status(f"Recording started. Press {hotkey} to stop")

    def on_stop_record_requested(self) -> None:
        with self._lock:
            if self._session_state.is_recording:
                scenario = self._stop_recording_use_case.execute()
                self._presenter.on_recording_stopped()
                self._presenter.show_status(f"Recording stopped. Events: {len(scenario)}")
                return

            if self._playback_thread and self._playback_thread.is_alive():
                self._playback_stop_event.set()
                self._presenter.show_status("Stopping playback...")
                return

            self._presenter.show_status("Nothing to stop")

    def on_play_clicked(self, speed_multiplier: float, loop_playback: bool) -> None:
        with self._lock:
            if self._session_state.is_recording:
                self._presenter.on_error("Stop recording before playback")
                return

            if not self._session_state.last_scenario:
                self._presenter.on_error("No recorded scenario")
                return

            if self._playback_thread and self._playback_thread.is_alive():
                self._presenter.show_status("Playback is already running")
                return

            if speed_multiplier <= 0:
                self._presenter.on_error("Speed multiplier must be > 0")
                return

            scenario = list(self._session_state.last_scenario)
            self._playback_stop_event.clear()
            self._playback_thread = threading.Thread(
                target=self._playback_worker,
                args=(scenario, speed_multiplier, loop_playback),
                daemon=True,
            )
            self._playback_thread.start()

    def _playback_worker(
        self, scenario, speed_multiplier: float, loop_playback: bool
    ) -> None:
        self._presenter.on_playback_started()
        mode = "loop" if loop_playback else "single"
        self._presenter.show_status(f"Playback started (x{speed_multiplier:g}, {mode})")
        try:
            self._play_scenario_use_case.execute(
                scenario=scenario,
                speed_multiplier=speed_multiplier,
                loop_playback=loop_playback,
                should_stop=self._playback_stop_event.is_set,
            )
            if self._playback_stop_event.is_set():
                self._presenter.show_status("Playback stopped")
            else:
                self._presenter.show_status("Playback finished")
        except Exception as exc:  # pragma: no cover
            self._presenter.on_error(f"Playback failed: {exc}")
        finally:
            self._presenter.on_playback_finished()
