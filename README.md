# AutoClicker

Mouse automation app with scenario recording and playback.

## Architecture

- `autoclicker/domain`: business models (`RecordedEvent`, `MouseEventType`).
- `autoclicker/application`: high-level logic, ports (interfaces), and UI event controller.
- `autoclicker/infrastructure`: adapters for Tkinter, keyboard hotkeys, pynput, pyautogui.
- `autoclicker/composition`: dependency wiring.

## Version

Version is defined in `autoclicker/__init__.py` as `__version__`.

## Run From Source

1. Install Python 3.11+.
2. Open PowerShell in project root.
3. Create virtual env:

```powershell
python -m venv .venv
```

4. Activate virtual env:

```powershell
.\.venv\Scripts\Activate.ps1
```

5. Upgrade pip:

```powershell
python -m pip install -U pip
```

6. Install project and runtime dependencies from `pyproject.toml`:

```powershell
python -m pip install -e .
```

7. Run app:

```powershell
python main.py
```

## Build .exe With pyproject.toml + .spec

1. Keep virtual env activated.
2. Install build tools from optional dependency group:

```powershell
python -m pip install ".[build]"
```

3. Build executable using spec file:

```powershell
pyinstaller --clean --noconfirm AutoClicker.spec
```

4. Output executable:

- `dist\AutoClicker.exe`

## Notes

- Global hotkeys from `keyboard` can require Administrator privileges on Windows.
- If antivirus blocks the app, add your project/build folder to exclusions during local testing.
