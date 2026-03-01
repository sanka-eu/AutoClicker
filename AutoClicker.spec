# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path

from PyInstaller.utils.hooks import collect_submodules

ROOT = Path(SPECPATH)
ICON_DIR = ROOT / "autoclicker" / "share" / "icons"
ICON_PATH = ICON_DIR / "icon.ico"

if not ICON_PATH.exists():
    raise FileNotFoundError(f"Icon file not found: {ICON_PATH}")

DATAS = []
for file_name in ("icon.ico", "icon.png"):
    candidate = ICON_DIR / file_name
    if candidate.exists():
        DATAS.append((str(candidate), "autoclicker/share/icons"))

hiddenimports = collect_submodules("pynput") + [
    "pyautogui",
    "pyscreeze",
    "mouseinfo",
]


a = Analysis(
    ["main.py"],
    pathex=[str(ROOT)],
    binaries=[],
    datas=DATAS,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="AutoClicker",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(ICON_PATH),
)
