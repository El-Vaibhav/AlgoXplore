# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['GUI\\1.py'],
    pathex=[],
    binaries=[],
    datas=[('GUI\\*', '.'), ('GUI\\GraphAlgos', 'GraphAlgos'), ('GUI\\Sorting_Algos', 'Sorting_Algos'), ('GUI\\scheduling_algos', 'scheduling_algos'), ('GUI\\Codes', 'Codes'), ('GUI\\Time_Complexity', 'Time_Complexity')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['pkg_resources'],
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
    name='Algoxplore',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
