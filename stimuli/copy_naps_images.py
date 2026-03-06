import os
import shutil
import pandas as pd

# === PATHS ===
csv_path = r"C:\Users\fkamdar\Desktop\repos\cp_nonmotor\stimuli\NAPS_not_in_child_rated.csv"
source_dir = r"C:\Users\fkamdar\Desktop\NAPs downloads\NAPS_H"
dest_dir = r"C:\Users\fkamdar\Desktop\NAPs downloads\naps not in child rated"

# Create destination folder if it doesn't exist
os.makedirs(dest_dir, exist_ok=True)

# Load CSV
df = pd.read_csv(csv_path)

copied = 0
missing = []

for img_id in df["ID"]:
    filename = img_id + ".jpg"
    source_path = os.path.join(source_dir, filename)
    dest_path = os.path.join(dest_dir, filename)

    if os.path.exists(source_path):
        shutil.copy2(source_path, dest_path)
        copied += 1
    else:
        missing.append(filename)

print(f"Copied {copied} images.")
if missing:
    print(f"{len(missing)} files not found:")
    print(missing)