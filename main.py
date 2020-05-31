import wx.adv
import wx
from plyer import notification
import sys

import warzonerep
import proccheck
import config
from bindata import resource_path
from updater import download_release, have2update, restart


TRAY_TOOLTIP = 'WarZone FIX'
TRAY_ICON = 'icon.ico'
PROCESS_NAME = 'ModernWarfare.exe'
VERSION = '0.1'
REPO = 'cproff/wzfix'


def notify(text, timeout=5, force=False):
    if not config.SETTINGS['silence'] or force:
        notification.notify(
            title='WarZone Fix',
            message=text,
            app_icon=resource_path(TRAY_ICON),
            timeout=timeout)

def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.Append(item)
    return item

class TaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self, frame):
        self.frame = frame
        self.dirname = config.SETTINGS['wzfolder']
        self.status = None
        self.renamer = warzonerep.WarzoneReanamer(self.dirname)
        super().__init__()
        self.set_icon(TRAY_ICON)
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_config)

        self.onGo = False
        self.warzoneState = None
        if warzonerep.WarzoneReanamer.check_dir(self.dirname):
            wx.CallLater(1000, self.start_switch, 0)
        else:
            self.dirname = ''
            config.set_param('wzfolder', '')
            config.save()

    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, 'Config folder', self.on_config)
        menu.AppendSeparator()
        create_menu_item(menu, f'Status: {"ON" if self.onGo else "OFF"}', self.start_switch)
        create_menu_item(menu, f'Silence: {"ON" if config.SETTINGS["silence"] else "OFF"}', self.silence_switch)
        menu.AppendSeparator()
        create_menu_item(menu, 'Repair WarZone', self.on_repair)
        menu.AppendSeparator()
        create_menu_item(menu, 'Exit', self.on_exit)
        return menu

    def start_switch(self, e):
        if self.dirname != '':
            self.onGo = not self.onGo
            if self.onGo:
                wx.CallLater(1000, self.on_timer)
        else:
            wx.MessageBox('You have to setup WarZone installation folder firstly.', 'Warning!', wx.OK | wx.ICON_WARNING)

    def silence_switch(self, e):
        config.set_param('silence', not config.SETTINGS["silence"])

    def set_icon(self, path):
        icon = wx.Icon(resource_path(path))
        self.SetIcon(icon, TRAY_TOOLTIP)

    def on_repair(self, e):
        if self.dirname != '':
            self.renamer.load_backup()
            wx.MessageBox('WarZone was repaired.', 'Done.', wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox('You have to setup WarZone installation folder firstly.', 'Warning!', wx.OK | wx.ICON_WARNING)

    def change_dirname(self, path):
        self.dirname = path
        self.renamer = warzonerep.WarzoneReanamer(self.dirname)
        config.set_param('wzfolder', self.dirname)
        if self.dirname != '' and not self.onGo:
            self.onGo = True
            self.on_timer()

    def on_config(self,e):
        dlg = wx.DirDialog(self.frame, "Choose WarZone installation folder", self.dirname, wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            if warzonerep.WarzoneReanamer.check_dir(dlg.GetPath()):
                self.change_dirname(dlg.GetPath())
            else:
                wx.MessageBox('Bad folder.\nChoose another one which contains "ModernWarfare.exe".', 'Warning!',
                    wx.OK | wx.ICON_WARNING)
        dlg.Destroy()

    def on_timer(self):
        newState = proccheck.process_exists(PROCESS_NAME)
        if self.warzoneState != newState and self.warzoneState is not None:
            if newState:
                self.renamer.fix()
                notify('WarZone was fixed')
            else:
                self.renamer.load_backup()
                notify('WarZone executable was loaded from backup')
        self.warzoneState = newState
        if self.onGo:
            wx.CallLater(1000, self.on_timer)

    def show_folder(self, event):
        wx.MessageBox(f'Current WarZone path: "{self.dirname}"', 'Help', wx.OK | wx.ICON_INFORMATION)

    def on_exit(self, event):
        wx.CallAfter(self.Destroy)

class App(wx.App):
    def update_dialog(self):
        v = (self.dialog.GetValue()+10)%100
        self.dialog.Update(v)
        if not self.isLoaded:
            wx.CallLater(500, self.update_dialog)
        else:
            self.dialog.Update(100)
            self.dialog.Destroy()
    def OnInit(self):
        if have2update(VERSION):
            self.isLoaded = False
            self.dialog = wx.ProgressDialog("WarZone Fix updater", "Updating...")
            self.update_dialog()
            updated, cmdline = download_release(REPO, VERSION)
            self.isLoaded = True
            if updated:
                os.system(cmdline)
                sys.exit(0)
        config.load()
        TaskBarIcon(None)
        return True

def main():
    app = App(False)
    app.MainLoop()


if __name__ == '__main__':
    main()