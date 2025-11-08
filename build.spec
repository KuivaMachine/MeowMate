# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main_menu.py'],
    pathex=[],
    binaries=[],
    datas=[

    ('resources/*', 'resources'),
    ('resources/.env', 'resources'),
    ('resources/fonts/*', 'resources/fonts'),
    ('drawable/bongo/bongo/*', 'drawable/bongo/bongo'),
    ('drawable/bongo/classic/*', 'drawable/bongo/classic'),
    ('drawable/bongo/guitar/*', 'drawable/bongo/guitar'),
    ('drawable/bongo/piano/*', 'drawable/bongo/piano'),
    ('drawable/bongo/rock/*', 'drawable/bongo/rock'),
    ('drawable/bongo/*', 'drawable/bongo'),
    ('drawable/cat/*', 'drawable/cat'),
    ('drawable/flork/*', 'drawable/flork'),
    ('drawable/ham/*', 'drawable/ham'),
    ('drawable/menu/*', 'drawable/menu'),],
    hiddenimports=[],
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
    [],
    exclude_binaries=True,
    name='MeowMate',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='resources/icon.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    name='MeowMate_v1.0.9',
    strip=False,
    upx=True,
    upx_exclude=[],
)