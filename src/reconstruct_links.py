import glob
from utils import extract_filename

files = glob.glob("ignored_data/with_exceptions/*.xml")
for file in files:
    name = extract_filename(file)
    prefix, idx = name.split("_")
    idx = int(idx)

    print(f"https://bugs.eclipse.org/bugs/show_bug.cgi?id={idx}")
