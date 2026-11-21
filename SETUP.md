# Setup guide (Windows and macOS) - please do this BEFORE the workshop (about 15 minutes)

You need three things: **Python 3.8+**, **Antigravity**, and **this folder**. No cloud account, no cost, no API keys for the labs.

## 1. Python

### Windows
1. Check first: open **PowerShell** and run `python --version`. If it prints 3.8 or higher, skip to step 2.
   (If it opens the Microsoft Store or says "not found", continue.) Also try `py --version`.
2. Download the installer from https://www.python.org/downloads/ and run it.
3. **Tick "Add python.exe to PATH"** on the first screen, then Install.
4. Close and reopen PowerShell, then run `python --version` (or `py --version`).

### macOS
1. Check first: open **Terminal** and run `python3 --version`. If it prints 3.8 or higher, skip to step 2.
   (macOS may offer to install developer tools. That is fine, accept it.)
2. Install from https://www.python.org/downloads/ (macOS installer), or with Homebrew: `brew install python`.
3. Reopen Terminal and run `python3 --version`.

Command name: on Windows use `python` (or `py`). On macOS use `python3`. The rest of this guide writes `python`, so swap in yours.

## 2. Antigravity
1. Download from https://antigravity.google/download (the facilitator will tell you which Antigravity product to use: the **standalone IDE** is what the workshop was tested with, unless told otherwise).
2. Requirements listed on that page: macOS 12 (Monterey) or later, or Windows 10 (64-bit) or later.
3. Install, open it, and sign in when prompted.
4. Make sure you can chat with the agent (send "hello"). If you hit a sign-in or quota message, tell the facilitator before the session. You can pair with someone.

## 3. The workshop folder
1. Unzip `cost-safeguards-participant.zip` somewhere easy (for example Desktop or Documents).
2. In Antigravity: **File > Open Folder**, and choose the unzipped `cost-safeguards-participant` folder (the one that contains `.agent`, `fixtures` and `tests`).
3. Open a terminal in that folder (Antigravity has one built in, or use PowerShell / Terminal and `cd` to the folder).

## 4. Pre-check (2 minutes, please do it)
Run these three steps in the folder's terminal:

1. `python tests/precheck.py`
   Expect every line to say `OK` and the last line `ALL GOOD`.
2. `python tests/run_fixtures.py`
   Expect `1/5 fixtures correct`. **That is correct.** The rules are blank until Lab 1.
3. In Antigravity's agent chat, ask: `What skills do you have available?`
   Expect `cloud-cost-safeguards` to appear. If it does not, tell the facilitator.

Optional, but useful for Lab 3: `git init`, `git add -A`, `git commit -m start` lets you undo changes later with `git checkout .`. Skip it if you don't have git.

If anything fails, send the facilitator a screenshot of the terminal. Don't spend more than 15 minutes on it, because pairing up on the day is fine.

## Troubleshooting
| Problem | Fix |
|---|---|
| `python` not found (Windows) | Try `py`, or reinstall and tick "Add python.exe to PATH" |
| `python` opens the Microsoft Store (Windows) | Install from python.org, or turn off the "App execution aliases" for python in Windows Settings |
| `python` is Python 2 or missing (macOS) | Use `python3` |
| precheck says files are missing | You opened the wrong folder level. Open the folder that directly contains `.agent`, `fixtures` and `tests` |
| `.agent` folder is not visible | It is a hidden folder. Turn on hidden files (Finder: Cmd+Shift+. ; Explorer: View > Show > Hidden items). Antigravity's file tree should still show it |
| Skill does not appear in the agent | Reopen the folder as the workspace, start a new chat, then tell the facilitator |
| Antigravity quota or sign-in problems | Tell the facilitator, you can pair with a neighbour |
| Security warning when installing | Only download from the official links above |
