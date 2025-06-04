# # MushiMix - Mushi OST Converter
# version 1.1.0
#
# Developed by Xeirla (Rur)
# Licensed under the MIT License
# 2025 June 03
#
# -----
#
# Small script for converting custom WAV files to Mushihimesama BIN format, to play in the Steam Version of the game.
#
# As of mushimix 1.1.0, this process can now be done while the game is open even!
# It is recommended you do so while the game is closed, of course, to avoid any potential errors
# (such as trying to replace an music file while its being played)
#
# # !! Remember to backup your game's OST !!
# If things get messy, you can always use "Verify integrity of game files" via Steam to restore the OST back to vanilla.
# You can also reinstall the game entirely, but that shouldn't be necessary!
#
# If you are changing the music often, it is also a good idea to restore all backups of the OST first
# before running the script again. Otherwise it may make a backup of the modded files instead!
#
# -----
#
# # Usage
# *If you want, you can clone this repository to skip part of the setup steps. If so, skip to step 3 below.*
#
# 1. Place this script into a folder, and create 2 subfolders:
#       "in" and "out"
# 2. Create 'mushimix.config' in the same directory as this script if it does not exist.
# 3. In the config, copy-paste the path to the game's OST
#     By default, this should be something like:
#        - Windows --- C:\Program Files\Steam\SteamApps\common\common\Mushihimesama\res\DISKDATA\B\
#
#        - Linux   --- $HOME/.steam/debian-installation/steamapps/common/Mushihimesama/res/DISKDATA/B/
#             (On Linux, replace '$HOME' with your home directory, as usual)
#
#        Make sure you include a '/' or '\' at the end of the path!
#
# 4. Put your .wav files into "custom"
#       Rename your .wav files to the filenames of the OST you want to replace.
#       For example:
#       "ma05.wav" will be used to replace "ma05.bin" in game (Stage 1 Arrange)
#
#       Most WAV files should just work, but if they don't, try converting them
#       from a lossless format using `ffmpeg`
#       Converter websites may not always result in a clean file.
#
# 5. Once all setup is done, run this script from a terminal:
#       python mushimix.py
#
# The script will create backup files in the "out" directory,
# and overwrite the designated tracks in the game's directory.
#
# Enjoy custom soundtrack in game!
#
# Note that there is no guarantee a track will sound good if it loops early.
# Also no guarantee the game won't just crash unexpectedly for no reason!
# It _shouldn't_, but this has not been tested that thoroughly.
# Use at your own risk!
#
# -----

import os
import sys

GAMEDIR = getGameDir()
WAVDIR = os.getcwd() + '/in/'
OUTDIR = os.getcwd() + '/out/'

#Set Game Directory from config file
def getGameDir():
    try:
        with open(os.getcwd() + '/mushimix.config', 'r') as f:
            gamedir = f.read().splitlines()[0]
            if (gamedir[0] == '#') or (gamedir == ''):
                raise Exception('NoPath')
            f.close()
        return str(gamedir)
    except Exception as e:
        if e == 'NoPath':
            print("ERRUR: No path set in 'mushimix.config'.")
        else:
            print("ERRUR: Failed to open 'mushimix.config'.")
        print("Make sure the file is in the same folder as this script, and contains the path to the game's OST on the first line of the file.")
        print("For example: ")
        print("Windows --- 'C:\\Program Files\\Steam\\SteamApps\\common\\common\\Mushihimesama\\res\\DISKDATA\\B\\'")
        print("Linux   --- '$HOME/.steam/debian-installation/steamapps/common/Mushihimesama/res/DISKDATA/B/'")
        sys.exit()


# Custom WAV to Mushi
def wavToMushi():
    print("Using the following directories:")
    print('GAME OST:  \t' + GAMEDIR)
    print('CUSTOM WAV:\t' + WAVDIR)
    print('OUTPUT:    \t' + OUTDIR)
    print('')
    if (GAMEDIR[-15:] != 'res/DISKDATA/B/') and (GAMEDIR[-15:] != 'res\\DISKDATA\\B\\'):
        print("WARNING: Game OST directory is different from expected.")
        print("The script will try to continue, but may fail or overwrite the wrong files!")
        print("Double check the path in `mushimix.config` matches the expected value")
    print("Processing Files...")
    try:
        for track in os.listdir(WAVDIR):
            # Open OST bin
            print(track)
            with open(GAMEDIR + track[:-4] + '.bin', 'rb') as bin_file:
                indata = bin_file.read()
                bin_file.close()

                # Strip header bytes
                prefix = indata[:0x138]

                # Make Backup files
                with open(OUTDIR + track[:-4] + '.bin' + '.backup', 'wb') as backup_file:
                    backup_file.write(indata)
                    backup_file.close()

                with open(GAMEDIR + track[:-4] + '.bin' + '.backup', 'wb') as backup_file:
                    backup_file.write(indata)
                    backup_file.close()

            # Get custom input WAV data
            with open(WAVDIR + track[:-4] + '.wav', 'rb') as in_file:
                data = in_file.read()
                in_file.close()

            # Overwrite OST in GAMEDIR with new WAV data
            with open(GAMEDIR + track[:-4] + '.bin', 'wb') as bin_file:
                bin_file.write(prefix)
                bin_file.write(data)
                bin_file.close()

    except Exception as e:
        print(e)
        print("ERRUR: Is an input file missing or named wrong?")

if __name__ == '__main__':
    print(":: mushimix.py ::\n")
    wavToMushi()
    print("Done!")
    print("Backup files of the OST tracks that were changed have been written to:")
    print('\t' + OUTDIR)
    print('\t' + GAMEDIR)
    print("To restore, delete the modded files, and then remove '.backup' from the backup filenames")
    print("If things get messy, you can always use 'Verify integrity of game files' via Steam to restore the OST back to vanilla.")
    print("You can also reinstall the game entirely, but that shouldn't be necessary!")


''''
MIT License
Copyright (c) 2025 Xeirla

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''
