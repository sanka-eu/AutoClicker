Architecture layers:

- `autoclicker/domain`: business models (`RecordedEvent`, `MouseEventType`).
- `autoclicker/application`: high-level logic, ports (interfaces), and UI event controller.
- `autoclicker/infrastructure`: adapters for Tkinter, keyboard hotkeys, pynput, pyautogui.
- `autoclicker/composition`: dependency wiring.

## Run

From project root:

```powershell
python main.py
```

