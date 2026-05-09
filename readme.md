# 🔇 Active Window Muter 

A simple, low-overhead utility to toggle the audio of your currently active window (game, browser, media player, etc). 

The script is optimized for gaming and is anti-cheat safe (when used per my recommendations below).

It features a customizable popup UI that doesn't steal window focus, even from fullscreen/borderless applications. 

*Note: This is not a standalone app; you need to set up a trigger method (even with the .exe version).*

### 🛡️ Why use this over other options?
Most alternatives I've combed through are unneccessarily complex & performance heavy, aren't anti-cheat safe, and don't offer a configurable UI.

This script is intentionally minimal:

- No suspicious or costly background process
- Reasonably fast execution (~1s)
- Customizable popup UI that doesn't interrupt gaming

### Python, AutoHotkey and Anti-Cheat Software
Sensitive game anti-cheats (like Vanguard, EAC, ACE, etc.) may flag processes like Python and AutoHotkey (AHK) as suspicious. This can prevent you from starting up the game or even lead to a temporary ban (happened to me in Delta Force). This is because they are powerful enough to create macros that give gameplay advantages (e.g. recoil prevention), possibly even full-on cheats (e.g. aimbot). 

The danger lies in persistent background scripts that's constantly loaded in memory: especially if they listen for keyboard/mouse inputs. While this *is* a Python script, it doesn't listen for inputs, and it doesn't run in the background: when activated it finds the currently active window, makes changes to the Windows Core Audio API, displays the overlay, then kills its own process, all in a few seconds. 

While I can't guarantee anything, no anti-cheat worth its salt should mark this as suspicious; briefly spinning up the Python executable is something that a significant portion of PCs do every once in a while.


## 📥 Installation

*Note: Running this as a Python script is the recommended method, but if you don't want to install it, I did include an executable version: scroll down to the end for details*

### Prerequisites
- Python 3.8+ added to PATH.

### Installation steps
   1. Clone or download this repository to a folder (e.g., C:\Users\Username\Scripts\active-window-muter
   2. Run install_requirements.bat
   3. Continue with your chosen trigger method

### Method A: Microsoft PowerToys (recommended)
PowerToys is an open-source toolset maintained by Microsoft. ts Keyboard Manager module allows you to remap keys with a simple interface. Or like in this case, launch programs using custom shortcuts much more reliably than the vanilla shortcut

1. Open PowerToys -> **Keyboard Manager** -> **Remap a shortcut**.
2. Click **Add shortcut remapping**.
3. Use the following settings:
   * **Shortcut:** `Shift` + `Alt` + `M` 
         *(or your preference)*
   * **Action:** `Run Program`
   * **App:** `C:\Program Files\Python312\pythonw.exe` 
         *(or wherever you have Python installed, no "" needed)*
   * **Args:** C:\Path\To\Your\active-window-muter.pyw"
         *Enclosed in ""*
   * **Start in directory:** *(Leave blank)*
   * **Elevation:** `Elevated`
   * **If running:** `Start another`
   * **Visibility:** `Normal`
4. Click **OK**. The 
5. Check out the other PowerToys Utilities! Some are quite useful, but only activate those you might want to use to save memory.

### Method B: Autohotkey
Add this to your .ahk script (or create a new one)

# SHIFT+ALT+M=TOGGLE MUTE
^!m::
Run, pythonw.exe "C:\Path\To\Your\active-window-muter.pyw"
return

### Method C: Manual activation & other methods
- If you want to activate the script manually (e.g. to test it before implementing a trigger method):
   Open active-window-muter.pyw in a text editor and change ACTIVATION_DELAY_MS = 0 to 1500 (or however long you need to ALT+TAB to an application playing audio)

- Windows has a native way to open programs with a shortcut, but it's notiously unreliable unless you're in File Explorer / Desktop. If you still want to try it:
   Right click active-window-muter.pyw -> Create shortcut. 
   Right click the shortcut -> Properties -> click "Shortcut key" to set shortcut -> OK.

## Customizing the UI
Open active-window-muter.pyw in Notepad (or any text editor). At the top is a CONFIGURATION block where you can edit variables (like WINDOW_POSITION, BG_COLOR, etc.).

### Known Quirks
- The muted application will **not** show as muted in the Volume Mixer.
- Windows does not add an application to the Volume Mixer until that application has already played sound. In that case, you'll see a "No Audio Session" warning. 

### EXECUTABLE VERSION
- The pre-compiled version should be considered experimental. If you run into issues, try the Python method before asking for help.
- It is located in the /executable folder. 
- It takes an extra ~0.5s to toggle mute.
- You can configure the design parameters by editing config.json in the same folder.