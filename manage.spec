# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['manage.py'],
             pathex=['/Users/rapple2018/Documents/Professional/Entrepreneur/Bill More Tech/bmt-saas-doc_search/ediscovery',
                     '/Users/rapple2018/Documents/Professional/Entrepreneur/Bill More Tech/bmt-saas-dependencies'],
             binaries=[('/Users/rapple2018/Documents/Professional/Entrepreneur/Bill More Tech/bmt-saas-dependencies/windows/tesseract/tesseract-ocr-w64-setup-v5.0.0-alpha.20210506.exe', '.')],
             datas=[],
             hiddenimports=[
                    'search',
                    'django.contrib.admin',
                    'django.contrib.auth',
                    'django.contrib.contenttypes',
                    'django.contrib.sessions',
                    'django.contrib.messages',
                    'django.contrib.staticfiles',
                    'django_elasticsearch_dsl',
                    'django.middleware.security.SecurityMiddleware',
                    'django.contrib.sessions.middleware.SessionMiddleware',
                    'django.middleware.common.CommonMiddleware',
                    'django.middleware.csrf.CsrfViewMiddleware',
                    'django.contrib.auth.middleware.AuthenticationMiddleware',
                    'django.contrib.messages.middleware.MessageMiddleware',
                    'django.middleware.clickjacking.XFrameOptionsMiddleware',
             ],
             hookspath=[],
             hooksconfig={},
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
          a.binaries, 
          Tree('../bmt-saas-dependencies/windows'),
          [],
          exclude_binaries=False,
          name='manage',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='manage')
