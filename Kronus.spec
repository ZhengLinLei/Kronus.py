# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['src\\__main__.py'],
             pathex=['C:\\Users\\34688\\Desktop\\Python\\py\\chatbot'],
             binaries=[],
             datas=[('./src/email.setting.json', '.'), ('./src/tkinter.setting.json', '.'), ('./build/ico.ico', 'data')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Kronus',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False , icon='build\\ico.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='Kronus')
