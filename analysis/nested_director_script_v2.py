"""
Makes the folder tree for one subject.
Patient first: everything about a subject lives under one folder.
Safe to re-run: it never overwrites anything that already exists.
"""

import os
import stat
from pathlib import Path

# ---- edit these ----
ROOT = Path(r"C:\Users\fkamdar\Desktop\repos\data\cp_nonmotor_data")
SUBJECT = "cpeeg02"
SESSIONS = [
    "01_offstim",
    "02_onstim_dorsal",
    "03_onstim_ventral",
]
# --------------------

TYPES = ["lfp", "eeg", "behavior", "eyetrack"]
STAGES = ["raw", "processed"]
RESULT_TYPES = ["tfr", "psd", "behavior", "stats"]

SESSION_LOG = """Session log
subject: {subject}
session: {session}
date:
who was running:

What happened (breaks, restarts, anything odd):


"""

NOTES_HEADER = "subject,session,date,med_state,stim_state,contact,amplitude,notes\n"


def make_folders():
    for stage in STAGES:
        for session in SESSIONS:
            for dtype in TYPES:
                d = ROOT / SUBJECT / stage / session / dtype
                d.mkdir(parents=True, exist_ok=True)
                print("made", d)

    for sub in RESULT_TYPES:
        d = ROOT / SUBJECT / "results" / sub
        d.mkdir(parents=True, exist_ok=True)
        print("made", d)


def make_notes():
    # one log file per raw session
    for session in SESSIONS:
        f = ROOT / SUBJECT / "raw" / session / "session_log.txt"
        if f.exists():
            print("already there, skipping", f)
            continue
        f.write_text(SESSION_LOG.format(subject=SUBJECT, session=session))
        print("wrote", f)

    # one notes table per subject
    notes = ROOT / SUBJECT / "notes.csv"
    if not notes.exists():
        notes.write_text(NOTES_HEADER)
        print("wrote", notes)

    text = notes.read_text()
    for session in SESSIONS:
        if f"{SUBJECT},{session}," in text:
            continue
        with open(notes, "a") as fh:
            fh.write(f"{SUBJECT},{session},,,,,,\n")
        print("added row for", session)


def lock_raw():
    """Make everything under this subject's raw/ read-only.
    Run only after the raw files are copied in."""
    for path, dirs, files in os.walk(ROOT / SUBJECT / "raw"):
        for name in files:
            f = Path(path) / name
            f.chmod(f.stat().st_mode & ~stat.S_IWRITE & ~stat.S_IWGRP & ~stat.S_IWOTH)
            print("locked", f)


if __name__ == "__main__":
    make_folders()
    make_notes()
    # lock_raw()