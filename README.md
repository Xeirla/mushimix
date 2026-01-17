# MushiMix - Mushi OST Converter
version 2.0.0

Licensed under the MIT License

Developed by Xeirla (Rur)

2025-2026 January 15


PySide6 is Licensed under the LGPL-3.0-only

Qt is Licensed under the LGPL-3.0-only

-----

Small script for converting custom WAV files to Mushihimesama BIN format, to play in the Steam Version of the game.
Now with a Qt GUI and support for other CAVE games on Steam!

As of mushimix 1.1.0, this process can now be done while the game is open even!
It is recommended you do so while the game is closed, of course, to avoid any potential errors
(such as trying to replace an music file while its being played)

# !! Remember to backup your game's OST !!

Mushimix will automatically create a "mushimix-bk" folder in the game's install directory on first use of "Remix",
and make a copy of any files before they are modded, if they don't exist in the directory already,
along with a small log noting when the last backup occurred and of which files.
You can use the controls in the program to enable and disable backing up unmodified files as desired.
To restore a backup, simply move the contents of "steamapps/common/<game>/mushimix-bk/" into the game's install directory.

If things get messy, you can also use "Verify integrity of game files" via Steam to restore the OST back to vanilla.

You can also just reinstall the game entirely, but that shouldn't be necessary!


-----

# Installing
Prerequisites:
- Python 3.13 
- PySide6

1. Install Python 3
2. Install PySide6: `pip install pyside6`
3. Clone the repository or download a release package

For Linux, depending on your distro it may be easier to create a virtual environment before 
installing PySide6, in the case your package manager doesn't include it or you want to keep
the system python installation clean.
```
cd path/to/mushimix_folder
python -m venv venv
source venv/bin/activate
pip install pyside6
```

# Usage
From command line: `python mushimix.py` 
Though you should be able to launch it without a terminal as well!

How to Use:
1. Select the path to the game's install directory.
2. Select the path to your music files.
    (only WAV supported)
3. Use the list to choose which files to swap.
4. Click "Remix!"

Notes:
- Changing a directory will clear file list!
- Use Manual Mode to save to "out" folder instead

Currently supported CAVE games (Steam Ver.)
- ✅ Mushihimesama
- ✅ DoDonPachi Ressurrection
- 𐄂  Deathsmiles

By default the script will create backups of files in the "/mushimix/bk" directory, 
found in the game's install location. 
This is enabled by default for more convenient and quick modding of the game,
but can be disabled via the checkbox controls.

Manual mode can be useful for troubleshooting as it the program will save
modded files to the "./out" directory rather than overwriting the game files directly. 
With it enabled you will have to manually swap the files in the filesystem instead. 
As such, it is disabled by default.

Note that there is no guarantee a track will sound good if it loops early. 
You may want to consider extended versions of any tracks you intend to add.

Enjoy custom soundtrack in game!

# Building
If you want to build an executeable file, you will need the following
- Python 3.13
- PySide6
- pyside6-deploy

```
pyside6-deploy mushimix.py
```
Configure the generated default pyside-deploy.spec or command line options,
if you would like to additionally change the icon to "img/mushimix-icon.png". 

For more information, see: https://doc.qt.io/qtforpython-6/deployment/deployment-pyside6-deploy.html
For building Qt for Python from source, see: https://doc.qt.io/qtforpython-6/building_from_source/index.html 


Note about pre-built binaries: 
Cross-compiling a PySide6 project is difficult, and we only have Linux host systems to build and test with.
Also, this is a relatively small Python script. Python and Qt are both cross-platform regardless.
Given the easiest method is to use pyside6-deploy, which comes with an installation of pyside6, as well as 
the above points, its not very compelling to build a single executeable for Linux, Windows, and Mac. 

As such, pre-built binaries have not been made to correspond with the release of Mushimix 2.0.0.
You are more than welcome to build the project yourself if you would like! It can be convenient in 
certain situations, such as if you have a dedicated machine to play these games, separate from your main PC.

# License
MushiMix is Licensed under the MIT License

PySide6 is Licensed under the LGPL-3.0-only

Qt is Licensed under the LGPL-3.0-only

More information can be found in "LICENSE.md"
