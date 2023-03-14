# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['tkinter_main.py'],
    pathex=['/Users/dsa/PycharmProjects/AdobeStockSourceGeneratorV2', '/Users/dsa/PycharmProjects/AdobeStockSourceGeneratorV2/venv/lib/python3.10/site-packages'],
    binaries=[],
    datas=[],
    hiddenimports=['webdriver_manager'],
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
    [],
    exclude_binaries=True,
    name='gen',
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
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='gen',
)
