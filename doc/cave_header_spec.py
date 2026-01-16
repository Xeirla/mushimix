# This spec is complete
cave_header = {
    "magic":b"",            # int,      x00 - x03 (should always be xC0 09 01 17)
    "bin_len":b"",          # int,      x04 - x07 (length of bin file)
    "bin_meta_len":b"",     # int,      x08 - x0B (length of bin metadata including ifd's)
    "internal_count":b"",   # int,      x0C - x0F (total number of ifd blocks/stored file data)
    "padding":b"",          # char[20], x10 - x23 (20 bytes null padding before first ifd block)
    }

# This is not a complete spec of the internal file descriptor structure, but enough for determining info for the ones containing WAV data.
# The structure is slightly different for Targa TGA internal files.
ifd_header = {
    "file_index":b"",   # char,    x00
    "file_type":b"",    # char[3], x01 - x03  (unknown, but always x00 00 02 for wav)
    "wav_len":b"",      # int,     x04 - x07  (data length for wav, unknown for tga)
    "unk_meta":b"",     # int,     x08 - x0B  (unused for wav, data length for tga)
    "data_offset":b"",  # int_ptr, x0C - X0F  (for all known file types, thankfully)
    "file_name":b"",    # string,  x10 - x114 (internal filename and padding until next index)
    }



