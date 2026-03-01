"""Tkinter implementation of the UI presenter."""

import sys
import tkinter as tk
from pathlib import Path
from tkinter import ttk

from autoclicker.application import AppController, UiPresenterPort

_ICON_ICO_REL = Path("autoclicker") / "share" / "icons" / "icon.ico"
_ICON_PNG_REL = Path("autoclicker") / "share" / "icons" / "icon.png"


class TkinterMainWindow(tk.Tk, UiPresenterPort):
    def __init__(self, controller: AppController) -> None:
        super().__init__()
        self._controller = controller
        self._window_icon_image = None

        self.title("AutoClicker")
        self.geometry("360x270")
        self._apply_window_icon()

        self._status_var = tk.StringVar(value="Ready")
        self._speed_var = tk.StringVar(value="1.0")
        self._loop_var = tk.BooleanVar(value=False)

        self._record_button = ttk.Button(
            self,
            text="Start Recording",
            command=self._controller.on_start_record_clicked,
        )
        self._record_button.pack(pady=10)

        self._stop_button = ttk.Button(
            self,
            text="Stop Recording",
            command=self._controller.on_stop_record_requested,
        )
        self._stop_button.pack(pady=10)

        self._play_button = ttk.Button(
            self,
            text="Play Recorded Scenario",
            command=self._on_play_clicked,
        )
        self._play_button.pack(pady=10)

        self._speed_frame = ttk.Frame(self)
        self._speed_frame.pack(pady=4)

        self._speed_label = ttk.Label(self._speed_frame, text="Speed multiplier:")
        self._speed_label.pack(side=tk.LEFT, padx=(0, 8))

        self._speed_entry = ttk.Entry(self._speed_frame, textvariable=self._speed_var, width=8)
        self._speed_entry.pack(side=tk.LEFT)

        self._loop_check = ttk.Checkbutton(
            self,
            text="Loop playback",
            variable=self._loop_var,
        )
        self._loop_check.pack(pady=4)

        self._status_label = ttk.Label(self, textvariable=self._status_var)
        self._status_label.pack(pady=14)

        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def run(self) -> None:
        self.mainloop()

    def show_status(self, text: str) -> None:
        self.after(0, lambda: self._status_var.set(text))

    def on_recording_started(self) -> None:
        self.after(0, self.iconify)

    def on_recording_stopped(self) -> None:
        self.after(0, self.deiconify)

    def on_playback_started(self) -> None:
        self.after(0, self.iconify)

    def on_playback_finished(self) -> None:
        self.after(0, self.deiconify)

    def on_error(self, text: str) -> None:
        self.show_status(f"Error: {text}")

    def _on_play_clicked(self) -> None:
        try:
            speed_multiplier = float(self._speed_var.get().strip())
        except ValueError:
            self.on_error("Speed multiplier must be a number")
            return
        self._controller.on_play_clicked(speed_multiplier, self._loop_var.get())

    def _on_close(self) -> None:
        self._controller.on_stop_record_requested()
        self.destroy()

    def _apply_window_icon(self) -> None:
        ico_path = self._resolve_resource_path(_ICON_ICO_REL)
        png_path = self._resolve_resource_path(_ICON_PNG_REL)

        try:
            if ico_path.exists():
                self.iconbitmap(default=str(ico_path))
                return
        except tk.TclError:
            pass

        try:
            if png_path.exists():
                self._window_icon_image = tk.PhotoImage(file=str(png_path))
                self.iconphoto(True, self._window_icon_image)
        except tk.TclError:
            pass

    @staticmethod
    def _resolve_resource_path(relative_path: Path) -> Path:
        if getattr(sys, "frozen", False):
            base = Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent))
        else:
            base = Path(__file__).resolve().parents[3]
        return base / relative_path
