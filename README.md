# 🔇 Active Window Muter 

- A simple, low-overhead Python script to toggle the audio of your currently active window (game, browser, media player, etc).

- The script is optimized for gaming and is anti-cheat safe.

- It features a customizable UI that doesn't steal window focus, even from fullscreen/borderless applications.
  
- Use in conjunction with a keyboard remapping utility to trigger the script (see below)

https://github.com/user-attachments/assets/ab2ba5a7-9629-411a-9a39-7db8a042f298

### 🛡️ Why use this over other options?
This script is intentionally minimal:

- Only 125 lines of code
- No suspicious or costly background process, no keyboard hooks
- Reasonably fast execution (~1s)
- Customizable popup that doesn't interrupt gaming

### Python, AutoHotkey and Anti-Cheat Software
Sensitive game anti-cheats (like Vanguard, EAC, ACE, etc.) may flag processes like Python and AutoHotkey (AHK) as suspicious. This can prevent you from starting up the game or even lead to a temporary ban (happened to me in Delta Force). This is because they are powerful enough to create macros that give gameplay advantages (e.g. recoil prevention), possibly even full-on cheats (e.g. aimbot). 

The danger lies in persistent background scripts that's constantly loaded in memory: especially if they listen for keyboard/mouse inputs. While this *is* a Python script, it doesn't listen for inputs, and it doesn't run in the background: when activated it finds the currently active window, makes changes to the Windows Core Audio API, displays the overlay, then kills its own process, all in a few seconds. 

While I can't guarantee anything, no anti-cheat worth its salt should mark this as suspicious; briefly spinning up the Python executable is something that a significant portion of PCs do.

## 📥 Installation

### Prerequisites
- Python 3.8+ added to PATH.

### Installation steps
   1. Clone or download this repository to a folder (e.g., C:\Users\Username\Scripts\active-window-muter
   2. Run install_requirements.bat
   3. Continue with your chosen trigger method

### Trigger Method A: Microsoft PowerToys (recommended)
- PowerToys is an open-source toolset maintained by Microsoft.
- It's Keyboard Manager module allows you to remap keys with a simple interface. Or like in this case, launch programs using custom shortcuts.

1. Install PowerToys: https://learn.microsoft.com/en-us/windows/powertoys/
2. Open **PowerToys** → **Keyboard Manager** → **Remap a shortcut**
3. Click **Add shortcut remapping**
4. Configure the shortcut using these settings:

| Setting | Value |
|---|---|
| **Shortcut** | `Shift + Alt + M` *(or your preferred shortcut)* |
| **Action** | `Run Program` |
| **App** | `C:\Program Files\Python312\pythonw.exe` *(or wherever Python is installed — no quotes needed)* |
| **Args** | `"C:\Path\To\Your\active-window-muter.pyw"` |
| **Start in directory** | *(Leave blank)* |
| **Elevation** | `Elevated` |
| **If running** | `Start another` |
| **Visibility** | `Normal` |

4. Click **OK**

> Tip: PowerToys includes many other useful utilities, but disabling unused modules can help reduce memory usage.

### Method B: Autohotkey (if you already use it and don't play multiplayer games)
Add this to your .ahk script (or create a new one)

```
# SHIFT+ALT+M=TOGGLE MUTE
^!m::
Run, pythonw.exe "C:\Path\To\Your\active-window-muter.pyw"
return
```

### Manual activation & other methods
- If you want to test the script or activate it manually:
   Open active-window-muter.pyw in a text editor and change ACTIVATION_DELAY_MS = 0 to 1500 (or however long you need to ALT+TAB to an application playing audio).

- Windows has a native way to open programs with a shortcut, but it's notiously unreliable unless you're in File Explorer / Desktop. If you still want to try it:
   Right click active-window-muter.pyw -> Create shortcut. 
   Right click the shortcut -> Properties -> click "Shortcut key" to set shortcut -> OK.

## Customizing the UI
Open active-window-muter.pyw in Notepad (or any text editor). At the top is a CONFIGURATION block where you can edit variables (like WINDOW_POSITION, BG_COLOR, etc.).

### Known Quirks
- The muted application will **not** show as muted in the Volume Mixer.
- Windows does not add an application to the Volume Mixer until that application has already played sound. In that case, you'll see a "No Audio Session" warning. 
