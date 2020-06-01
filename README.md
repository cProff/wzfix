# WarZone FIX

This app is a fix for Call of Duty Warzone bug of non-loading shaders. This bug let the game crashes every time it tries to install shaders. [Here](https://www.reddit.com/r/CODWarzone/comments/fhqt1t/pc_crash_investigation_warzone/) you can find thread searching for the solution. This thread is kind an old one but this bug is still here. And this is a solution.

#### Installation

This app doesn't need any installation, just download last release from the [releases page](https://github.com/cProff/wzfix/releases) and save it in some folder. On first execution it'll create file "param.ini" and that's all. Now you can play CoD Warzone. 

###### Windows startup

It is on your own, but starting this app every time computer starts is a little lazily. You can add it to the Windows startup and **WarZoneFIX** will runs with Windows. To do it you need make following steps:

1. Press WIN+R,  write "shell:startup" and press ENTER
2. Create Windows link for **WarZoneFIX** in opened folder:
   - Mouse right-click on executable, "create link"
   - Copy created link to the folder

Now **WarZoneFIX** is added to the Windows startup list. 

#### Usage

Usage is pretty simple. First of all setup the CoD Warzone installation folder. It can be done by mouse left-click on tray icon of **WarZoneFIX** or by choosing *config folder* in tray dropdown menu. Now **WarZoneFIX** is ready to work.

If you don't want **WarZoneFIX** to send you notification every time it save your chair from your ass-fire, you can set *silence* parameter to OFF. 

If you close an app while playing Warzone and now it cannot start try to use *Repair WarZone* button.

#### How it works

This app just changes ModernWarfare.exe title to  ModernWarfare.exe_backup every tine WarZone starts. And change name back on WarZone close.