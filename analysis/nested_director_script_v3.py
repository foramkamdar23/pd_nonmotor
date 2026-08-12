"""
Makes the folder tree for one or more subjects.
Patient first: everything about a subject lives under one folder.
Safe to re-run: it never overwrites anything that already exists.
"""

import os
import stat
from pathlib import Path

# ---- edit this ----
ROOT = Path(r"C:\Users\fkamdar\Desktop\repos\data\pd_nonmotor_data")
# 01_offmed_offstim
# 03_offmed_onstimventral


# 01_offmed_offstim
# 02_offmed_onstimdorsal

# 06_onmed_onstimventral

# subject: list of (session name, date)
# leave the date as "" if you don't know it yet
SUBJECTS = {
    "pdnm_064": [
        ("01_onmed_onstimdorsal",   "2026-03-26"),
        ("02_onmed_onstimventral",  "2026-04-07"),
        ("03_offmed_onstimdorsal",  "2026-04-21"),
        ("04_offmed_onstimventral", "2026-05-06"),
        ("05_onmed_offstim", "2026-06-18"),

    ],
    "pdnm_091": [
        ("01_onmed_onstimdorsal",   "2026-04-13"),
        ("02_offmed_onstimdorsal",  "2026-04-27"),
        ("03_offmed_onstimventral", "2026-05-11"),
        ("04_onmed_offstim", "2026-07-09"),
    ],
}
# -------------------

TYPES = ["lfp", "eeg", "behavior", "eyetrack"]
STAGES = ["raw", "processed"]
RESULT_TYPES = ["tfr", "psd", "behavior", "stats"]

SESSION_LOG = """Session log
subject: {subject}
session: {session}
date: {date}
who was running:

What happened (breaks, restarts, anything odd):


"""

NOTES_HEADER = "subject,session,date,med_state,stim_state,contact_leftbrain,amplitude_leftbrain,pulsewidth_leftbrain,frequency_leftbrain,contact_rightbrain,amplitude_rightbrain,pulsewidth_rightbrain,frequency_rightbrain,notes\n"


def make_folders(subject, sessions):
    for stage in STAGES:
        for session, date in sessions:
            for dtype in TYPES:
                d = ROOT / subject / stage / session / dtype
                d.mkdir(parents=True, exist_ok=True)
                print("made", d)

    for sub in RESULT_TYPES:
        d = ROOT / subject / "results" / sub
        d.mkdir(parents=True, exist_ok=True)
        print("made", d)


def make_notes(subject, sessions):
    # one log file per raw session
    for session, date in sessions:
        f = ROOT / subject / "raw" / session / "session_log.txt"
        if f.exists():
            print("already there, skipping", f)
            continue
        f.write_text(SESSION_LOG.format(subject=subject, session=session, date=date))
        print("wrote", f)

    # one notes table per subject
    notes = ROOT / subject / "notes.csv"
    if not notes.exists():
        notes.write_text(NOTES_HEADER)
        print("wrote", notes)

    text = notes.read_text()
    for session, date in sessions:
        if f"{subject},{session}," in text:
            continue
        with open(notes, "a") as fh:
            fh.write(f"{subject},{session},{date},,,,,\n")
        print("added row for", session)


def lock_raw(subject):
    """Make everything under this subject's raw/ read-only.
    Run only after the raw files are copied in."""
    for path, dirs, files in os.walk(ROOT / subject / "raw"):
        for name in files:
            f = Path(path) / name
            f.chmod(f.stat().st_mode & ~stat.S_IWRITE & ~stat.S_IWGRP & ~stat.S_IWOTH)
            print("locked", f)


if __name__ == "__main__":
    for subject in SUBJECTS:
        sessions = SUBJECTS[subject]
        print("\n===", subject, "===")
        make_folders(subject, sessions)
        make_notes(subject, sessions)
        # lock_raw(subject)