## Building Binary of our Application

First, install necessary tools for build.

```bash
pip3 install photocrypt[gui]
pip3 install PyInstaller
```

Then go to bin directory.

```bash
cd bin
```

Inside bin directory, run following command to build our application.

```bash
pyinstaller --onefile src/app.py
```

Then the executable file will be generated inside bin/dist directory.

If you are in windows, you can run application by

```bash
dist/app.exe
```

If you are in linux distros, you can run application by
```bash
dist/app
```