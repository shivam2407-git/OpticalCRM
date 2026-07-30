# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_all

# Collect everything required by Streamlit
streamlit_datas, streamlit_binaries, streamlit_hiddenimports = collect_all("streamlit")

# Project files
project_datas = [
    ("app.py", "."),
    ("pdf_generator.py", "."),
    ("optical_store.db", "."),
    ("logo.ico", "."),
]

a = Analysis(
    ["launcher.py"],
    pathex=[],
    binaries=streamlit_binaries,
    datas=project_datas + streamlit_datas,
    hiddenimports=streamlit_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="OpticalCRM",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,
    icon="logo.ico",
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    name="OpticalCRM",
)