"""Tkinter implementation of the UI presenter."""

import sys
import threading
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
        self._is_capturing_hotkey = False

        self.title("AutoClicker")
        self.geometry("640x320")
        self.minsize(640, 320)
        self._configure_styles()
        self._apply_window_icon()

        self._status_var = tk.StringVar(value="Ready")
        self._speed_var = tk.StringVar(value="1.0")
        self._loop_var = tk.BooleanVar(value=False)
        self._stop_hotkey_var = tk.StringVar(
            value=self._format_hotkey_for_display(
                self._controller.get_stop_record_hotkey()
            )
        )

        self._content = ttk.Frame(self, style="App.TFrame", padding=(16, 14, 16, 12))
        self._content.pack(fill=tk.BOTH, expand=True)

        self._title_label = ttk.Label(
            self._content,
            text="AutoClicker",
            style="Title.TLabel",
        )
        self._title_label.pack(anchor=tk.W, pady=(0, 10))

        self._record_button = ttk.Button(
            self._content,
            text="Start Recording",
            style="Primary.TButton",
            width=22,
            command=self._controller.on_start_record_clicked,
        )
        self._record_button.pack(anchor=tk.W, pady=(0, 10))

        self._stop_row = ttk.Frame(self._content, style="App.TFrame")
        self._stop_row.pack(fill=tk.X, pady=(0, 10))

        self._stop_button = ttk.Button(
            self._stop_row,
            text="Stop Recording",
            style="Primary.TButton",
            width=22,
            command=self._controller.on_stop_record_requested,
        )
        self._stop_button.pack(side=tk.LEFT)

        self._stop_hotkey_frame = ttk.Frame(self._stop_row, style="App.TFrame")
        self._stop_hotkey_frame.pack(side=tk.RIGHT)

        self._stop_hotkey_label = ttk.Label(
            self._stop_hotkey_frame,
            text="Stop hotkey:",
            style="App.TLabel",
        )
        self._stop_hotkey_label.pack(side=tk.LEFT, padx=(0, 8))

        self._stop_hotkey_entry = ttk.Entry(
            self._stop_hotkey_frame,
            textvariable=self._stop_hotkey_var,
            width=18,
            state="readonly",
            justify="center",
        )
        self._stop_hotkey_entry.pack(side=tk.LEFT, padx=(0, 8))

        self._change_hotkey_button = ttk.Button(
            self._stop_hotkey_frame,
            text="Capture",
            style="Primary.TButton",
            command=self._on_change_stop_hotkey_clicked,
        )
        self._change_hotkey_button.pack(side=tk.LEFT)

        self._play_row = ttk.Frame(self._content, style="App.TFrame")
        self._play_row.pack(fill=tk.X, pady=(0, 10))

        self._play_button = ttk.Button(
            self._play_row,
            text="Play Recorded Scenario",
            style="Primary.TButton",
            width=22,
            command=self._on_play_clicked,
        )
        self._play_button.pack(side=tk.LEFT)

        self._playback_options = ttk.Frame(self._play_row, style="App.TFrame")
        self._playback_options.pack(side=tk.RIGHT)

        self._speed_label = ttk.Label(
            self._playback_options,
            text="Speed multiplier:",
            style="App.TLabel",
        )
        self._speed_label.pack(side=tk.LEFT, padx=(0, 8))

        self._speed_entry = ttk.Entry(
            self._playback_options,
            textvariable=self._speed_var,
            width=8,
            justify="center",
        )
        self._speed_entry.pack(side=tk.LEFT, padx=(0, 14))

        self._loop_check = ttk.Checkbutton(
            self._playback_options,
            text="Loop playback",
            variable=self._loop_var,
        )
        self._loop_check.pack(side=tk.LEFT)

        self._status_label = ttk.Label(
            self._content,
            textvariable=self._status_var,
            style="Status.TLabel",
            anchor="w",
        )
        self._status_label.pack(fill=tk.X, pady=(12, 0))

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

    def _on_change_stop_hotkey_clicked(self) -> None:
        if self._is_capturing_hotkey:
            return

        self._is_capturing_hotkey = True
        self._change_hotkey_button.configure(state="disabled", text="Capturing...")
        self.show_status("Press a new stop hotkey combination on keyboard...")

        capture_thread = threading.Thread(
            target=self._capture_stop_hotkey_worker,
            daemon=True,
        )
        capture_thread.start()

    def _capture_stop_hotkey_worker(self) -> None:
        try:
            new_hotkey = self._controller.capture_stop_record_hotkey()
        except Exception as exc:
            self.after(0, lambda: self._finish_stop_hotkey_capture(None, str(exc)))
            return
        self.after(0, lambda: self._finish_stop_hotkey_capture(new_hotkey, None))

    def _finish_stop_hotkey_capture(
        self, new_hotkey: str | None, error_text: str | None
    ) -> None:
        self._is_capturing_hotkey = False
        self._change_hotkey_button.configure(state="normal", text="Capture")

        if error_text:
            self.on_error(error_text)
            return

        if not new_hotkey:
            self.on_error("Failed to capture hotkey")
            return

        if self._controller.on_change_stop_hotkey_requested(new_hotkey):
            self._stop_hotkey_var.set(
                self._format_hotkey_for_display(
                    self._controller.get_stop_record_hotkey()
                )
            )

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

    def _configure_styles(self) -> None:
        style = ttk.Style(self)
        if "clam" in style.theme_names():
            style.theme_use("clam")

        bg = "#f4f6f9"
        text = "#1f2937"
        accent = "#0f6db8"
        accent_active = "#0a568f"
        status_bg = "#e9eef5"

        self.configure(bg=bg)
        style.configure("App.TFrame", background=bg)
        style.configure("App.TLabel", background=bg, foreground=text, font=("Segoe UI", 10))
        style.configure(
            "Title.TLabel",
            background=bg,
            foreground="#0f172a",
            font=("Segoe UI Semibold", 14),
        )
        style.configure(
            "Primary.TButton",
            font=("Segoe UI", 10),
            padding=(10, 6),
            background=accent,
            foreground="#ffffff",
            borderwidth=0,
        )
        style.map(
            "Primary.TButton",
            background=[("active", accent_active), ("pressed", accent_active)],
            foreground=[("disabled", "#dbeafe"), ("!disabled", "#ffffff")],
        )
        style.configure(
            "Status.TLabel",
            background=status_bg,
            foreground="#334155",
            font=("Segoe UI", 10),
            padding=(10, 8),
        )

    @staticmethod
    def _format_hotkey_for_display(hotkey: str) -> str:
        alias = {
            "ctrl": "Ctrl",
            "shift": "Shift",
            "alt": "Alt",
            "windows": "Win",
            "win": "Win",
        }
        parts = [part.strip() for part in hotkey.split("+") if part.strip()]
        pretty_parts = []
        for part in parts:
            lower = part.lower()
            if lower in alias:
                pretty_parts.append(alias[lower])
            elif len(part) == 1 and part.isalpha():
                pretty_parts.append(part.upper())
            else:
                pretty_parts.append(part)
        return " + ".join(pretty_parts)
