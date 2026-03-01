"""pynput implementation for click recording."""

import threading
import time
from typing import List

from pynput import mouse

from autoclicker.application.ports import MouseClickRecorderPort
from autoclicker.domain import MouseEventType, RecordedEvent, Scenario


class PynputClickRecorder(MouseClickRecorderPort):
    def __init__(self) -> None:
        self._events: List[RecordedEvent] = []
        self._recording = False
        self._listener: mouse.Listener | None = None
        self._lock = threading.Lock()

    def start_recording(self) -> None:
        with self._lock:
            self._events = []
            self._recording = True

        self._listener = mouse.Listener(on_click=self._on_click)
        self._listener.start()

    def stop_recording(self) -> None:
        with self._lock:
            self._recording = False

        if self._listener is not None:
            self._listener.stop()
            self._listener.join()
            self._listener = None

    def get_events(self) -> Scenario:
        with self._lock:
            return list(self._events)

    def _on_click(self, x: int, y: int, button, pressed: bool) -> None:
        if not pressed:
            return
        if button != mouse.Button.left:
            return
        if not self._is_recording():
            return

        event = RecordedEvent(
            event_type=MouseEventType.LEFT_CLICK,
            timestamp=time.perf_counter(),
            x=x,
            y=y,
        )
        with self._lock:
            self._events.append(event)

    def _is_recording(self) -> bool:
        with self._lock:
            return self._recording
