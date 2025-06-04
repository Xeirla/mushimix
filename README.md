# MushiMix - Mushi OST Converter
version 1.1.0

Developed by Xeirla (Rur)
Licensed under the MIT License
2025 June 03

-----

Small script for converting custom WAV files to Mushihimesama BIN format, to play in the Steam Version of the game.

As of mushimix 1.1.0, this process can now be done while the game is open even!
It is recommended you do so while the game is closed, of course, to avoid any potential errors
(such as trying to replace an music file while its being played)

# !! Remember to backup your game's OST !!
If things get messy, you can always use "Verify integrity of game files" via Steam to restore the OST back to vanilla.
You can also reinstall the game entirely, but that shouldn't be necessary!
 
If you are changing the music often, it is also a good idea to restore all backups of the OST first 
before running the script again. Otherwise it may make a backup of the modded files instead!

-----

# Usage
*If you want, you can clone this repository to skip part of the setup steps. If so, skip to step 3 below.*

1. Place this script into a folder, and create 2 subfolders:
      "in" and "out"
2. Create 'mushimix.config' in the same directory as this script if it does not exist.
3. In the config, copy-paste the path to the game's OST
    By default, this should be something like:
       - Windows --- C:\Program Files\Steam\SteamApps\common\common\Mushihimesama\res\DISKDATA\B\
       
       - Linux   --- $HOME/.steam/debian-installation/steamapps/common/Mushihimesama/res/DISKDATA/B/
            (On Linux, replace '$HOME' with your home directory, as usual)

       Make sure you include a '/' or '\' at the end of the path!

4. Put your .wav files into "custom"
      Rename your .wav files to the filenames of the OST you want to replace.
      For example:
      "ma05.wav" will be used to replace "ma05.bin" in game (Stage 1 Arrange)

      Most WAV files should just work, but if they don't, try converting them
      from a lossless format using `ffmpeg`
      Converter websites may not always result in a clean file.

5. Once all setup is done, run this script from a terminal:
      python mushimix.py

The script will create backup files in the "out" directory,
and overwrite the designated tracks in the game's directory.

Enjoy custom soundtrack in game!

Note that there is no guarantee a track will sound good if it loops early.
Also no guarantee the game won't just crash unexpectedly for no reason!
It _shouldn't_, but this has not been tested that thoroughly.
Use at your own risk!

