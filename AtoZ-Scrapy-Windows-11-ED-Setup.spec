# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['scrapy\\gui\\installer_gui.py'],
    pathex=[],
    binaries=[],
    datas=[('scrapy', 'scrapy'), ('_tcl_data', '_tcl_data'), ('_tk_data', '_tk_data')],
    hiddenimports=['scrapy.gui.installer_gui', 'scrapy.gui.main_gui', 'scrapy.gui.version', 'scrapy.gui.updater', 'scrapy.pipelines.gui_pipeline'],
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
    name='AtoZ-Scrapy-Windows-11-ED-Setup',
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
    version='version_info.txt',
)
