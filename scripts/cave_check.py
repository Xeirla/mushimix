import os
import sys

# This spec is complete
cave_header = {
    "magic":b"",            # int,      x00 - x03 (should always be xC0 09 01 17)
    "bin_len":b"",          # int,      x04 - x07 (length of bin file)
    "bin_meta_len":b"",     # int,      x08 - x0B (length of bin metadata including ifd's)
    "internal_count":b"",   # int,      x0C - x0F (total number of ifd blocks/stored file data)
    "padding":b"",          # char[20], x10 - x23 (20 bytes null padding before first ifd block)
    }

# This is not a complete spec of the structure, but enough for determining internal files and location,
ifd_header = {
    "file_index":b"",   # char,    x00
    "file_type":b"",    # char[3], x01 - x03  (unknown, but always x00 00 02 for wav)
    "wav_len":b"",      # int,     x04 - x07  (data length for wav, unknown for tga)
    "unk_meta":b"",     # int,     x08 - x0B  (unused for wav, data length for tga)
    "data_offset":b"",  # int_ptr, x0C - X0F  (for all known file types, thankfully)
    "file_name":b"",    # string,  x10 - x114 (internal filename and padding until next index)
    }

def run():
    # The script should be placed in the game's install location for all operations to work
    cwd = os.getcwd()
    for path in os.listdir(cwd):
        if path[:3] == "res": # Check if path is a resource folder
            res = cwd + "/" + path + "/DISKDATA"
            print("Resource Path: ", res)
            for disk_alpha in (sorted(os.listdir(res))): # Get DISKDATA folders and contents
                alpha = res + "/" + disk_alpha
                file_list = sorted(os.listdir(alpha))
                print(disk_alpha, "Files:", file_list)
                print("---------\n")

                for bin_file in file_list: # Parse header metadata of each file
                    # Read cave_header
                    bin_file_path = alpha + "/" + bin_file

                    print("File :", bin_file_path)
                    with open(bin_file_path, "rb") as f:
                        header = cave_header
                        header["magic"] = f.read(0x4)
                        header["bin_len"] = f.read(0x4)
                        header["bin_meta_len"] = f.read(0x4)
                        header["internal_count"] = f.read(0x4)
                        header["padding"] = f.read(20)
                        # for k,v in header.items():
                        #     print(k, ":", "0x" + str(v.hex()).upper())
                        # print("---------\n")

                        # Read all ifd_headers
                        file_ifds = []
                        i = 0
                        while i < int.from_bytes(header["internal_count"]):
                            file_ifds.append({})
                            file_ifds[i]["file_index"] = f.read(0x1)
                            file_ifds[i]["file_type"] = f.read(0x3)
                            file_ifds[i]["wav_len"] = f.read(0x4)
                            file_ifds[i]["unk_meta"] = f.read(0x4)
                            file_ifds[i]["data_offset"] = f.read(0x4)
                            file_ifds[i]["file_name"] = f.read(0x104)
                            # file_ifds.append(current_ifd)
                    #         print ("FILE IFDS:", file_ifds)
                    #         for k,v in file_ifds[i].items():
                    #             print(k, ":", "0x" + str(v.hex()).upper())
                    #         print("---")
                            i += 1
                    # print("---------\n")
                    # Write info to log
                    # sys.exit()
                    f.close()

                    with open("CAVE_CHECK.log", "a+") as f:
                        f.write("File :" + bin_file_path + "\n")
                        for k,v in header.items():
                            f.write(k + ":" + "0x" + str(v.hex()).upper() + "\n")
                        f.write("--------\n")
                        f.write(bin_file_path + "\n")
                        for ind in file_ifds:
                            # print(ind)
                            f.write("IFD_FILE: " + str(ind["file_name"]).split("\\x00")[0] + "\n")
                            f.write("index: " + str((ind["file_index"]).hex()).upper() + "  ")

                            header_offset = (0x23 + (int.from_bytes(ind["file_index"], byteorder='big') * 0x114))
                            f.write("header_offset: " + str(hex(header_offset)).upper() + "  ")

                            f.write("data_offset:" + str((ind["data_offset"]).hex()) + "\n")
                            f.write("---\n")
                        f.write("-----------------------------\n")
                    # sys.exit()



if __name__ == "__main__":
    run()
    print("done")
