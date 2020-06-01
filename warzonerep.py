import os.path

FILE_NAME = '/ModernWarfare.exe'
BACKUP_NAME = '/ModernWarfare.exe_backup'


class WarzoneReanamer():
    def __init__(self, path):
        self.p = path

    def fix(self):
        if os.path.isfile(self.p+FILE_NAME):
            os.rename(self.p+FILE_NAME, self.p+BACKUP_NAME)
            return True
        else:
            return False

    def load_backup(self):
        if os.path.isfile(self.p+BACKUP_NAME):
            os.rename(self.p+BACKUP_NAME, self.p+FILE_NAME)
            return True
        else:
            return False

    @classmethod
    def check_dir(cls, path):
        return os.path.isfile(path+FILE_NAME) or os.path.isfile(path+BACKUP_NAME)
