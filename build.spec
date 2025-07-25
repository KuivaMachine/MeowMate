# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main_menu.py'],
    pathex=[],
    binaries=[],
    datas=[

    ('resources/*.qss', 'resources'),
    ('resources/*.ico', 'resources'),
    ('resources/fonts/*.ttf', 'resources/fonts'),
    ('drawable/bongo/bongo/*.png', 'drawable/bongo/bongo'),
    ('drawable/bongo/classic/*.png', 'drawable/bongo/classic'),
    ('drawable/bongo/guitar/*.png', 'drawable/bongo/guitar'),
    ('drawable/bongo/piano/*.png', 'drawable/bongo/piano'),
    ('drawable/bongo/rock/*.png', 'drawable/bongo/rock'),
    ('drawable/bongo/*.svg', 'drawable/bongo'),
    ('drawable/bongo/*.png', 'drawable/bongo'),
    ('drawable/bongo/*.gif', 'drawable/bongo'),
    ('drawable/cat/*.svg', 'drawable/cat'),
    ('drawable/cat/*.png', 'drawable/cat'),
    ('drawable/cat/*.gif', 'drawable/cat'),
    ('drawable/flork/*.svg', 'drawable/flork'),
    ('drawable/flork/*.png', 'drawable/flork'),
    ('drawable/flork/*.gif', 'drawable/flork'),
    ('drawable/ham/*.svg', 'drawable/ham'),
    ('drawable/ham/*.png', 'drawable/ham'),
    ('drawable/ham/*.gif', 'drawable/ham'),
    ('drawable/menu/*.svg', 'drawable/menu'),
    ('drawable/menu/*.png', 'drawable/menu'),
    ('drawable/menu/*.gif', 'drawable/menu'),],
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
    name='MeowMate_v1.0.8',
    strip=False,
    upx=True,
    upx_exclude=[],
)