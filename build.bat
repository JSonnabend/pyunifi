@rem pyinstaller -F --paths="E:\pyRoon\pyRoonLibrary\pyroon-master\roonapi" --paths="E:\pyRoon\pyRoonLibrary\Lib\site-packages" --hidden-import=http,roonapi RoonEventghost.py
@rem "D:\Program Files\Python 3.11\python.exe" -m
pyinstaller -D -y ^
	--add-data "sampleconfig.conf;." ^
	unificli.py
xcopy .\dist\unificls\*.* "d:\program files\unifi command line\" /E /Y

@rem