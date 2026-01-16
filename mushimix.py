# MushiMix - Mushi OST Modding Script
# version 2.0.0
#
# Licensed under the MIT License
# Developed by Xeirla (Rur)
# 2025-2026 January 15
#
# PySide6 is Licensed under the LGPL-3.0-only
# Qt is Licensed under the LGPL-3.0-only
#
# -----
# Small script for converting custom WAV files to Mushihimesama BIN format, to play in the Steam Version of the game.
# Now with a Qt GUI and support for other CAVE games on Steam!
#
# As of mushimix 1.1.0, this process can now be done while the game is open even!
# It is recommended you do so while the game is closed, of course, to avoid any potential errors
# (such as trying to replace an music file while its being played)
#
# # !! Remember to backup your game's OST !!
#
# Mushimix will automatically create a "mushimix-bk" folder in the game's install directory on first use of "Remix",
# and make a copy of any files before they are modded, if they don't exist in the directory already,
# along with a small log noting when the last backup occurred and of which files.
# You can use the controls in the program to enable and disable backing up unmodified files as desired.
# To restore a backup, simply move the contents of "steamapps/common/<game>/mushimix-bk/" into the game's install directory.
#
# If things get messy, you can always use "Verify integrity of game files" via Steam to restore the OST back to vanilla.
#
# You can also just reinstall the game entirely, but that shouldn't be necessary!
#
# -----

# Standard Modules
import os
import sys
import shutil
import datetime
import time

# PySide6 (Qt Framework for Python)
from PySide6 import QtCore, QtWidgets, QtGui

# CAVE/KOMODO BIN format documentation
# ----------------------------------------------
# NOTE: The following two dictionaries are just documentation on the file format of the .bin files in the KOMODO published CAVE Steam Ports.
# Both of these instances are not actually used in this script directly, but are here for reference and documentation purposes.
# It is accurate to our research as of: 14 January 2026
#
# This spec is complete:
# _CAVE_HEADER = {
#     "magic":b"",            # int,      x00 - x03 (should always be xC0 09 01 17)
#     "bin_len":b"",          # int,      x04 - x07 (length of bin file)
#     "bin_meta_len":b"",     # int,      x08 - x0B (length of bin metadata including ifd's)
#     "internal_count":b"",   # int,      x0C - x0F (total number of ifd blocks/stored file data)
#     "padding":b"",          # char[20], x10 - x23 (20 bytes null padding before first ifd block)
#     }
#
# This is not a complete spec of the internal file descriptor structure, but enough for determining info for the ones containing WAV data.
# The structure is slightly different for Targa TGA internal files.
# _IFD_HEADER = {
#     "file_index":b"",   # char,    x00
#     "file_type":b"",    # char[3], x01 - x03  (unknown, but always x00 00 02 for wav)
#     "wav_len":b"",      # int,     x04 - x07  (data length for wav, unknown for tga)
#     "unk_meta":b"",     # int,     x08 - x0B  (unused for wav, data length for tga)
#     "data_offset":b"",  # int_ptr, x0C - X0F  (for all known file types, thankfully)
#     "file_name":b"",    # string,  x10 - x114 (internal filename and padding until next index)
#     }
#
# NOTE: For modding Sound Effects:
# Editing sound effects (and textures) in BIN files will change data chunk offsets in the ifd_headers.
# As such, any mods that do so will need to account for this and manually reconstruct the headers to correct the offsets,
# rather than just copy-pasting the entire cave_header and ifd_headers as mushimix currently does.
# The special case for the Main Menu OST gets around this by just hardcoding the known offset of the menu music,
# since it comes last in the ifd files anyways.
# The code wouldnt be too hard to implement but unnecessary for now!
#
# Also probably would want a separate app or advanced/alternate mode for SFX editing,
# since it would have to work on one file at a time, or would make the file list way too long.
# The current UI and design simply can't really accomodate for such a task.
# ----------------------------------------------
# TODO:
# - Add Deathsmiles Support
# - Design mod bundle/package spec for quick modding?
#     Maybe for after texture modding, so others can bundle and share entire audiovisual overhaul mods.
#     Due to added complexity, probably will want to make a separate program to handle sound effects and texture mods respectively.
# ----------------------------------------------

# CaveData - Hardcoded dictionaries of the in-game OST files. Modding Sound Effects is currently unsupported.
class CaveData:
    def __init__(self):
        self.mushi_files = {
            "Main Menu": "mme.bin",
            # "Sound Effects": "ms.bin"
            # "Voice Lines": "mv.bin"

            "Shot Select":"m01.bin",
            "Stage 1":"m05.bin",
            "Stage 2":"m06.bin",
            "Stage 3":"m09.bin",
            "Stage 4":"m10.bin",
            "Stage 5":"m11.bin",
            "Stage Clear":"m02.bin",
            "Boss 1":"m07.bin",
            "Boss 2":"m12.bin",
            "TLB Final":"m13.bin",
            "Ending":"m08.bin",
            "Name Entry":"m04.bin",
            "Game Over":"m03.bin",

            "(1.5) Shot Select":"mu01.bin",
            "(1.5) Stage 1":"mu05.bin",
            "(1.5) Stage 2":"mu06.bin",
            "(1.5) Stage 3":"mu09.bin",
            "(1.5) Stage 4":"mu10.bin",
            "(1.5) Stage 5":"mu11.bin",
            "(1.5) Stage Clear":"mu02.bin",
            "(1.5) Boss 1":"mu07.bin",
            "(1.5) Boss 2":"mu12.bin",
            "(1.5) TLB Final":"mu13.bin",
            "(1.5) Ending":"mu08.bin",
            "(1.5) Name Entry":"mu04.bin",
            "(1.5) Game Over":"mu03.bin",

            "(Arrange) Shot Select":"ma01.bin",
            "(Arrange) Stage 1":"ma05.bin",
            "(Arrange) Stage 2":"ma06.bin",
            "(Arrange) Stage 3":"ma09.bin",
            "(Arrange) Stage 4":"ma10.bin",
            "(Arrange) Stage 5":"ma11.bin",
            "(Arrange) Stage Clear":"ma02.bin",
            "(Arrange) Boss 1":"ma07.bin",
            "(Arrange) Boss 2":"ma12.bin",
            "(Arrange) TLB Final":"ma13.bin",
            "(Arrange) Ending":"ma08.bin",
            "(Arrange) Name Entry":"ma04.bin",
            "(Arrange) Game Over":"ma03.bin",
            }

        self.dfk_files = {
            "Main Menu": "mm.bin",
            # "Sound Effects": "msoe.bin"
            # "Voice Lines": "msv.bin"

            "Shot Select":"m01.bin",
            "Stage 1":"m02.bin",
            "Stage 2-A":"m07a.bin",
            "Stage 2-B":"m07b.bin",
            "Stage 3-A":"m08a.bin",
            "Stage 3-B":"m08b.bin",
            "Stage 4-A":"m09a.bin",
            "Stage 4-B":"m09b.bin",
            "Stage 5":"m10.bin",
            "Stage Clear":"m04.bin",
            "Boss 1":"m03.bin",
            "Boss 2":"m06.bin",
            "EX Boss":"m11.bin",
            "TLB Hibachi":"m12.bin",
            "Ending":"m13.bin",
            "Name Entry":"m05.bin",

            "(BL) Shot Select":"mb01.bin",
            "(BL) Stage 1":"mb02.bin",
            "(BL) Stage 2-A":"mb07a.bin",
            "(BL) Stage 2-B":"mb07b.bin",
            "(BL) Stage 3-A":"mb08a.bin",
            "(BL) Stage 3-B":"mb08b.bin",
            "(BL) Stage 4-A":"mb09a.bin",
            "(BL) Stage 4-B":"mb09b.bin",
            "(BL) Stage 5":"mb10.bin",
            "(BL) Stage Clear":"mb04.bin",
            "(BL) Boss 1":"mb03.bin",
            "(BL) Boss 2":"mb06.bin",
            "(BL) EX Boss":"mb11.bin",
            "(BL) TLB Hibachi":"mb12.bin",
            "(BL) Secret Zatsuza":"mb14.bin",
            "(BL) Ending":"mb13.bin",
            "(BL) Name Entry":"mb05.bin",

            "(BL Arrange) Shot Select":"mk01.bin",
            "(BL Arrange) Stage 1":"mk02.bin",
            "(BL Arrange) Stage 2-A":"mk07a.bin",
            "(BL Arrange) Stage 2-B":"mk07b.bin",
            "(BL Arrange) Stage 3-A":"mk08a.bin",
            "(BL Arrange) Stage 3-B":"mk08b.bin",
            "(BL Arrange) Stage 4-A":"mk09a.bin",
            "(BL Arrange) Stage 4-B":"mk09b.bin",
            "(BL Arrange) Stage 5":"mk10.bin",
            "(BL Arrange) Stage Clear":"mk04.bin",
            "(BL Arrange) Boss 1":"mk03.bin",
            "(BL Arrange) Boss 2":"mk06.bin",
            "(BL Arrange) EX Boss":"mk11.bin",
            "(BL Arrange) TLB Hivac":"mk12.bin",
            "(BL Arrange) Secret":"mk14.bin",
            "(BL Arrange) Ending":"mb13.bin",
            "(BL Arrange) Name Entry":"mk05.bin",
            }

class MushiMix:
    def __init__(self):
        print(" --- MushiMix 2.0.0 ---")
        self.app = QtWidgets.QApplication([])
        self.containers = {}
        self.widgets = {}
        self.cave_data = CaveData()


        self.current_game = ""
        self.current_game_file_dict = {}

        self.music_file_list = []
        self.file_dict = {}
        self.path_dict = {
            "out": "./out",
            "backup": ""
            }

        self.safe_mode = False # Renamed to Manual Mode for clarity. Disabled by default for direct game modding
        self.backup_mode = True # For simple file version backups

        self.backup_status = " "
        self.progress = "🟥 Select a supported game first!"
        print("[INFO]", ": Initialization Complete!")


    @QtCore.Slot()
    def setPathHelper(self, path, key, label, dir_type):
        path[key] = self.setPath()
        label.setText(path[key])
        self.path_dict[dir_type] = path[key]
        self.updateFileList(path, key, dir_type)

    def setPath(self):
        dialog = QtWidgets.QFileDialog()
        dialog.setFileMode(QtWidgets.QFileDialog.FileMode.Directory)

        path = []
        try:
            if dialog.exec():
                path = dialog.selectedFiles()

                print("[INFO]", "setPath() : ", path[0])
            return path[0]
        except Exception:
            return ""


    def updateFileList(self, path, key, dir_type):
        # Clear exiting file list
        for entry in self.file_dict.keys():
            self.file_dict[entry].clear()
            self.file_dict[entry].addItem("--")

        # Update game list
        if (dir_type == "game"):
            if self.filelist_container.layout() != None:
                layout = self.filelist_container.layout()

                # MUST iterate in reverse order as deleting an item shifts the index for every item
                # Special thanks to eyllanesc on stackoverflow.com for this because
                # it is practically undocumented. The method given for safely deleting widgets of a layout in the official Qt Documentation is _wrong_
                # and will cause a runtime error or crash.
                for index in reversed(range(layout.count())):
                    layout.itemAt(index).widget().setParent(None)

            self.current_game = ""
            self.current_game_file_dict = {}
            self.file_dict = {}
            self.filelist_container.show()

            game = path[key]
            if (os.path.isdir(self.path_dict["game"] + "/res/DISKDATA")):
                if game[-13:] == "Mushihimesama" or (game[-4:] == "虫姫さま"):
                    self.current_game = "mushi"
                    self.current_game_file_dict = self.cave_data.mushi_files

                elif (game[-23:] == "DoDonPachi Resurrection") or (game[-8:] == "怒首領蜂 大復活"):
                    self.current_game = "dfk"
                    self.current_game_file_dict = self.cave_data.dfk_files

            # Add dropdowns
            for entry in self.current_game_file_dict.keys():
                self.file_dict[entry] = QtWidgets.QComboBox(parent=self.filelist_container)
                self.file_dict[entry].addItem("--")

                # Populate wth music if any
                if self.music_file_list != None:
                    self.file_dict[entry].addItems(self.music_file_list)

        if dir_type == "music":
            # Clear exiting file list
            for entry in self.file_dict.keys():
                self.file_dict[entry].clear()
                self.file_dict[entry].addItem("--")

            # Read Music directory
            self.music_file_list = []
            if path[key]:
                for i in os.listdir(path[key]):
                    if i[-4:] == ".wav": # Should read magic as well to verify but 99% of cases this will work fine.
                        self.music_file_list.append(i)
                    self.music_file_list.sort()

            # Populate any dropdowns
            if self.filelist_container.layout() != None:
                layout = self.filelist_container.layout()
                for k in self.file_dict.keys():
                    for track in self.music_file_list:
                        self.file_dict[k].addItem(track)

        # Update layout
        layout = self.filelist_container.layout()
        if layout == None:
            layout = QtWidgets.QGridLayout(self.filelist_container)

        i = 0
        for label, widget in self.file_dict.items():
            layout.addWidget(QtWidgets.QLabel(label, parent=self.filelist_container), 0 + i, 0)
            layout.addWidget(widget,0 + i, 1)
            i += 1

            self.filelist_container.show()

        # Ready Check
        if self.file_dict.items() != None:
            self.path_dict["backup"] = self.path_dict["game"] + "/mushimix-bk"
            if os.path.isdir(self.path_dict["backup"]):
                self.backup_status = "🟢 Backup folder exists!"
                self.info_backup.setText(self.backup_status)
                print("[INFO]", ": Backup Dir Exists")
            else:
                self.backup_status = "🟡 Backup folder missing!\nWill be created unless explicitly disabled"
                self.info_backup.setText(self.backup_status)

            if self.backup_mode == False:
                self.backup_status = "🟥 Backups Disabled!"
                self.info_backup.setText(self.backup_status)


            self.progress = "🟡 Ready!"
            self.info_progress.setText(self.progress)


    # Window
    def createWindow(self):
        self.window = QtWidgets.QWidget()
        self.window.resize(600,600)
        self.window.setObjectName("MainWindow")
        self.window.setStyleSheet("QWidget#MainWindow { border-image: url(./img/mushimix-bg.png) }")
        self.win_layout = QtWidgets.QGridLayout(self.window)
        self.window.show()

    # Top Widget
    def createTopWidget(self):
        top_container = QtWidgets.QWidget(parent=self.window)

        # Title
        title = QtWidgets.QLabel(parent=top_container)
        img = QtGui.QPixmap("./img/mushimix-title.png")
        scaled = img.scaled(QtCore.QSize(240, 240), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        title.setPixmap(scaled)
        # title.setMinimumHeight(120)

        # Credits
        credits = QtWidgets.QLabel("version 2.0.0\nMusic Modding Script for Mushihimesama \n(Steam Ver.)\nDeveloped by Xeirla (c) 2026\nLicensed under the MIT License\nMade with Qt/PySide6 (LGPL-3.0-only)\n", parent=top_container)

        # # Dialogs
        dir_container = QtWidgets.QGroupBox(parent=top_container)
        directories = {
            "game_path":"...",
            "music_path":"..."
            }
        dir_game_label = QtWidgets.QLabel(directories["game_path"], parent=dir_container)
        dir_game_label.setWordWrap(True)
        dir_game_button =  QtWidgets.QPushButton("Set Path to Game", parent=dir_container)
        dir_game_button.clicked.connect(lambda checked: self.setPathHelper(directories, "game_path", dir_game_label, "game"))

        dir_mus_label = QtWidgets.QLabel(directories["game_path"], parent=dir_container)
        dir_mus_label.setWordWrap(True)
        dir_mus_button =  QtWidgets.QPushButton("Set Path to Custom WAVs", parent=dir_container)
        dir_mus_button.clicked.connect(lambda checked: self.setPathHelper(directories, "music_path", dir_mus_label, "music"))

        # Diag Layout 2x3 grid
        dialog_layout = QtWidgets.QGridLayout(dir_container)
        dialog_layout.addWidget(dir_game_button, 0, 0 ,1, 1)
        dialog_layout.addWidget(dir_game_label, 0, 1, 1, 3)

        dialog_layout.addWidget(dir_mus_button, 1, 0 ,1, 1)
        dialog_layout.addWidget(dir_mus_label, 1, 1, 1, 3)

        # Image
        image = QtWidgets.QLabel(parent=top_container)
        img = QtGui.QPixmap("./img/mushimix-logo.png")
        scaled = img.scaled(QtCore.QSize(200, 200), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        image.setPixmap(scaled)

        # Layout 2x5 grid
        layout = QtWidgets.QGridLayout(top_container)
        layout.addWidget(title,0,0,1,2)
        layout.addWidget(credits,0,3,1,1)

        layout.addWidget(dir_container,1,0,1,4)
        layout.addWidget(image,0,4,2,2)


        top_container.show()

        # References
        self.containers["top_container"] = top_container
        self.widgets["title_label"] = title

    # Bottom Widget
    def createBottomWidget(self):
        bot_container = QtWidgets.QWidget(parent=self.window)

        # List
        self.filelist_container = QtWidgets.QGroupBox(parent=bot_container)
        scrollArea = QtWidgets.QScrollArea()
        scrollArea.setWidget(self.filelist_container)
        scrollArea.setWidgetResizable(True)

        # Manual Mode - Safe Mode Check
        check_container = QtWidgets.QWidget(parent=bot_container)

        safe_checkbox = QtWidgets.QCheckBox("Manual Mode", parent=bot_container)
        safe_checkbox.stateChanged.connect(lambda checked: self.safeModeChange())
        safe_checkbox.setStyleSheet("QCheckBox { font:bold; font-size : 16px } QCheckBox::indicator { width: 24px; height: 24px;} ")
        safe_checkbox.setToolTip("When enabled, will write output to the \"./out\" directory \ninstead of modifying the game files directly.")

        # Backup Checkbox
        backup_checkbox = QtWidgets.QCheckBox("Enable Backups", parent=bot_container)
        backup_checkbox.setChecked(True)
        backup_checkbox.stateChanged.connect(lambda checked: self.backupModeChange())
        backup_checkbox.setStyleSheet("QCheckBox { font:bold; font-size : 16px } QCheckBox::indicator { width: 24px; height: 24px;} ")
        backup_checkbox.setToolTip("When enabled, will copy vanilla files \ninto \"<game_path>/mushimix-bk/\" before modifying.")

        # Info and Game Selector
        info_text = QtWidgets.QLabel("""\
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
    ✅ Mushihimesama
    ✅ DoDonPachi Ressurrection
    𐄂  Deathsmiles
"""\
        , parent=bot_container)
        info_text.setWordWrap(True)
        info_text.setIndent(12)

        # Backup Info
        self.info_backup = QtWidgets.QLabel(self.backup_status, parent=bot_container)

        # Progress info
        self.info_progress = QtWidgets.QLabel(self.progress, parent=bot_container)

        # Mix Button
        mix_button =  QtWidgets.QPushButton("Remix!", parent=bot_container)
        mix_button.setMaximumHeight(100)
        mix_button.setStyleSheet("QPushButton { font : bold; font-size: 30px; }")  #height: 48px; }")
        mix_button.clicked.connect(lambda checked: self.mixButton())

        # Layout 1x2 grid for checkboxes
        layout = QtWidgets.QGridLayout(check_container)
        layout.addWidget(safe_checkbox, 0, 0, 1, 1)
        layout.addWidget(backup_checkbox, 0, 1, 1, 1)

        # Layout 3x5 grid
        layout = QtWidgets.QGridLayout(bot_container)
        layout.addWidget(scrollArea, 0, 0, 6, 3)
        layout.addWidget(check_container, 0, 3, 1, 1)
        layout.addWidget(info_text, 1, 3, 1, 1)
        layout.addWidget(self.info_backup, 2, 3, 1, 1)
        layout.addWidget(self.info_progress, 3, 3, 1, 1)
        layout.addWidget(mix_button, 4, 3, 2, 1)

        bot_container.show()

        # References
        self.containers["bot_container"] = bot_container

    # Manual Mode - Safe Mode
    @QtCore.Slot()
    def safeModeChange(self):
        if self.safe_mode == False:
            self.safe_mode = True
            print("[INFO]",": Safe Mode Enabled")
        else:
            self.safe_mode = False
            print("[INFO]",": Safe Mode Disabled")


    # Backup Mode
    @QtCore.Slot()
    def backupModeChange(self):
        if self.backup_mode == False:
            self.backup_mode = True
            try:
                if self.path_dict["game"] != None:
                    if os.path.isdir(self.path_dict["game"] + "/mushimix-bk"):
                        self.backup_status = "🟢 Backup folder exists!"
                        self.info_backup.setText(self.backup_status)
                        print("[INFO]", ": Backup Dir Exists")
                    else:
                        self.backup_status = "🟡 Backup folder missing!\nWill be created unless explicitly disabled"
                        self.info_backup.setText(self.backup_status)

            except KeyError as e:
                self.backup_status = " "
                self.info_backup.setText(self.backup_status)

            print("[INFO]",": Backups Enabled")
        else:
            self.backup_mode = False
            self.backup_status = "🟥 Backups Disabled!"
            self.info_backup.setText(self.backup_status)
            print("[INFO]",": Backups Disabled")


    # Mix Button
    @QtCore.Slot()
    def mixButton(self):
        # Ready Check
        if self.file_dict:
            print("[INFO]",": Mixing!")
            start_time = datetime.datetime.now()
            dfk_paths = {
                "1.5":  "/res/DISKDATA/F/",
                "BL":   "/res_BL/DISKDATA/F/",
                }
            mushi_path = "/res/DISKDATA/B/"

            if self.safe_mode == True:
                if not os.path.isdir(self.path_dict["out"]):
                    os.makedirs(self.path_dict["out"])
                    print("[INFO]", ": Created Manual Mode Directory")

            if self.backup_mode == True:
                if not os.path.isdir(self.path_dict["backup"]):
                    os.makedirs(self.path_dict["backup"])
                    print("[INFO]:", "Created Backup Directory.")
                backup_list = []

            for entry in self.file_dict.keys():
                try:
                    if self.file_dict[entry].currentText() != "--": # check if combo box has something:

                        # Check Game
                        if self.current_game == "mushi":
                            diskdata_path = mushi_path
                        if self.current_game == "dfk":
                            if entry[:3] == "(BL":
                                diskdata_path = dfk_paths["BL"]
                            else:
                                diskdata_path = dfk_paths["1.5"]

                        # Backup the file if needed
                        if self.backup_mode == True:
                            src = self.path_dict["game"] + diskdata_path + self.current_game_file_dict[entry]
                            dst = self.path_dict["backup"] + diskdata_path
                            if not os.path.isfile(dst + self.current_game_file_dict[entry]):
                                if not os.path.isdir(dst):
                                    os.makedirs(dst)
                                shutil.copy2(src, dst, follow_symlinks=True)
                                backup_list.append(diskdata_path + self.current_game_file_dict[entry])

                        # Get the mushi_header and custom WAV file data:
                        with open(self.path_dict["game"] + diskdata_path + self.current_game_file_dict[entry], 'rb') as f:
                            if entry == "Main Menu": # Main Menu special case
                                header = f.read(0x474)
                                # Preserve all menu Sound Effects data
                                # NOTE: Editing sound effects in the future will change data chunk offsets.
                                if self.current_game == "mushi":
                                    mm_se_data = f.read(0x139EE)
                                    header = header + mm_se_data
                                if self.current_game == "dfk":
                                    mm_se_data = f.read(0x355B6)
                                    header = header + mm_se_data
                            else:
                                header = f.read(0x138)
                            f.close() # Make sure this is closed before overwriting

                        with open(self.path_dict["music"] + "/" + self.file_dict[entry].currentText(), 'rb') as f:
                            data = f.read()

                        # Write file with game header + filename
                        out = header + data
                        outpath = self.path_dict["game"] + diskdata_path + self.current_game_file_dict[entry]
                        if self.safe_mode == True:
                            outpath = self.path_dict["out"] + "/" + self.current_game_file_dict[entry]

                        with open(outpath, 'wb') as f:
                            f.write(out)
                except Exception as e:
                    print("[ERRUR]", e, ": in mixButton()")


            if self.backup_mode == True:
                with open(self.path_dict["backup"] + "/backup.log", "a+") as f:
                    if backup_list:
                        f.write("---\n")
                        f.write("Backup @ " + str(start_time).split(".")[0] + "\n")
                        for i in backup_list:
                            f.write(i + "\n")

                    f.close()
                self.backup_status = "🟢 Backup versioning complete!"
                self.info_backup.setText(self.backup_status)

            end_time = datetime.datetime.now()
            elapsed_time = end_time - start_time
            self.progress = "🟢 Done! @ " + str(end_time).split(".")[0] + " in " + str(elapsed_time) + "s"
            self.info_progress.setText(self.progress)
            print("[INFO]",": 🟢 Done! @ " + str(end_time).split(".")[0] + " in " + str(elapsed_time) + "s")

        else:
            print("[WARNING]", "Nothing to mix! Did you set a Game Directory yet?")


    # Layout
    def updateWindowLayout(self):
        self.win_layout.addWidget(self.containers["top_container"], 0, 0, 1, 1)
        self.win_layout.addWidget(self.containers["bot_container"], 1, 0, 3, 1)


    def run(self):
        self.createWindow()
        self.createTopWidget()
        self.createBottomWidget()
        self.updateWindowLayout()

        self.app.exec()


if __name__ == "__main__":
    mushimix = MushiMix()
    mushimix.run()
    print("[INFO]", ": Program Exited")
    print("--------------------------")
    sys.exit()

''''
MIT License
Copyright (c) 2026 Xeirla

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''
