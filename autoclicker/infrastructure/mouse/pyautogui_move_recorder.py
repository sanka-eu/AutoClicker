"""PyAutoGUI + background thread implementation for move recording."""

import threading
import time
from typing import List

import pyautogui

from autoclicker.application.ports import MouseMoveRecorderPort
from autoclicker.domain import MouseEventType, RecordedEvent, Scenario


class PyAutoGuiMoveRecorder(MouseMoveRecorderPort):
    def __init__(self, sample_interval: float = 0.05) -> None:
        self._sample_interval = sample_interval
        self._events: List[RecordedEvent] = []
        self._recording = False
        self._thread: threading.Thread | None = None
        self._lock = threading.Lock()

    def start_recording(self) -> None:
        with self._lock:
            self._events = []
            self._recording = True

        self._thread = threading.Thread(target=self._worker, daemon=True)
        self._thread.start()

    def stop_recording(self) -> None:
        with self._lock:
            self._recording = False

        if self._thread is not None:
            self._thread.join()
            self._thread = None

    def get_events(self) -> Scenario:
        with self._lock:
            return list(self._events)

    def _worker(self) -> None:
        while self._is_recording():
            point = pyautogui.position()
            event = RecordedEvent(
                event_type=MouseEventType.MOVE,
                timestamp=time.perf_counter(),
                x=point.x,
                y=point.y,
            )
            with self._lock:
                self._events.append(event)
            time.sleep(self._sample_interval)

    def _is_recording(self) -> bool:
        with self._lock:
            return self._recording
