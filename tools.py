import os

def scan_folder(folder):
    files = []
    for root, _, filenames in os.walk(folder):
        for f in filenames:
            if f.endswith(".py") or f.endswith(".js"):
                files.append(os.path.join(root, f))
    return files


def read_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return "Error reading file"


def get_pc_spec():
    return os.popen("systeminfo").read()