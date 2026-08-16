# -*- mode: python ; coding: utf-8 -*-

import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# 필요 시 PySide6 및 추가 모듈 hiddenimport 지정
hidden_imports = [
    'PySide6.QtCore',
    'PySide6.QtWidgets',
    'PySide6.QtGui',
    'openpyxl',
    'supabase',
    'postgrest',
    'gotrue',
    'realtime',
    'storage3',
    'my_package.repositories.excel_receipt_repository'
]

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=[],  # resources는 외부에 둘 것이므로 datas에서 제외합니다.
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['__pycache__', '.venv', '.vscode'],
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
    exclude_binaries=True, # --onedir 모드 설정
    name='AcademyPOS',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True, # GUI 프로그램이므로 콘솔 창 비활성화 (테스트 시에는 True로 변경 가능)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # icon='resources/images/app_icon.ico' # 필요 시 실행 파일 아이콘 지정
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='AcademyPOS',
)