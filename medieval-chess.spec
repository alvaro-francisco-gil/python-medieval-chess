# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['medieval-chess.py'],
    pathex=[],
    binaries=[],
    datas=[('images', 'images')],  # Include the images directory
    hiddenimports=['medieval_chess'],  # Include the medieval_chess module
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='medieval-chess',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to False for a windowed application
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # You can add an icon file here if you have one
) 