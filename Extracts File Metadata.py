###Extracts file metadata, including size, create (ctime), last modified (mtime), and last accessed (atime).  Windows/Mac/Linux

import os
import sys

def extract_metadata(filename):
    filename = filename.strip().strip('"').strip("'")
    filename = os.path.expanduser(filename)  
    filename = os.path.abspath(filename)

    if not os.path.exists(filename):
        raise FileNotFoundError(f"File not found: {filename}")

    stat_info = os.stat(filename)
    metadata = {
        'size': stat_info.st_size,
        'last_modified': stat_info.st_mtime,
        'last_accessed': stat_info.st_atime,
        'created': stat_info.st_ctime
    }
    return metadata

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = " ".join(sys.argv[1:])
    else:
        file_path = "{{ .FULL_FILE_PATH }}"

    print(extract_metadata(file_path))
