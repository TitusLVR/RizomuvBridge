import os
from pymxs import runtime as rt

class RizomUVBridgeSettings:
    def __init__(self):
        self.user_scripts_dir = rt.getDir(rt.Name("userscripts"))
        self.base_dir = os.path.join(self.user_scripts_dir, "RizomuvBridge")
        self.ini_file = os.path.join(self.base_dir, "RizomuvBridge_settings.ini")
        
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

    def get_ini_setting(self, section, key, default=""):
        try:
            val = rt.getINISetting(self.ini_file, section, key)
            if not val and default:
                return default
            return val
        except:
            return default

    def set_ini_setting(self, section, key, value):
        rt.setINISetting(self.ini_file, section, key, str(value))

    def get_port(self):
        try:
            val = self.get_ini_setting("Connection", "Port")
            return int(val) if val else None
        except:
            return None

    def set_port(self, port):
        self.set_ini_setting("Connection", "Port", str(port))

    def get_rizom_path(self):
        path = self.get_ini_setting("Path", "rizomuv")
        if path and os.path.exists(path):
            return path
        return None

    def get_scripts_folder(self):
        default = os.path.join(self.base_dir, "LUA")
        saved = self.get_ini_setting("Scripts", "Folder", default)
        if os.path.exists(saved):
             return saved
        if os.path.exists(default):
             return default
        return self.base_dir

    def set_scripts_folder(self, path):
        self.set_ini_setting("Scripts", "Folder", path)

    def get_available_scripts(self):
        folder = self.get_scripts_folder()
        if not os.path.exists(folder):
            return []
        return [f for f in os.listdir(folder) if f.lower().endswith(".lua")]

    def get_exchange_folder(self):
        folder = self.get_ini_setting("ExchangeFolder", "Folder")
        if not folder or str(folder) == "false":
             temp_dir = os.path.join(rt.sysInfo.tempdir, "RizomuvBridge")
             if not os.path.exists(temp_dir):
                 os.makedirs(temp_dir)
             return temp_dir + "\\" 
        return folder
