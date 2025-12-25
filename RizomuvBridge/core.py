import os
from .settings import RizomUVBridgeSettings
from .max_ops import RizomUVBridgeMaxOps
from .rizom_client import RizomClient

class RizomUVBridgeCore:
    def __init__(self):
        self.settings = RizomUVBridgeSettings()
        self.max_ops = RizomUVBridgeMaxOps()
        self.client = RizomClient(self.settings)

    # Exposed for UI
    def get_ini_setting(self, section, key, default=""):
        return self.settings.get_ini_setting(section, key, default)

    def set_ini_setting(self, section, key, value):
        self.settings.set_ini_setting(section, key, value)
        
    def get_rizom_path(self):
        return self.settings.get_rizom_path()
        
    def get_scripts_folder(self):
        return self.settings.get_scripts_folder()
        
    def set_scripts_folder(self, path):
        self.settings.set_scripts_folder(path)
        
    def get_available_scripts(self):
        return self.settings.get_available_scripts()

    def get_exchange_folder(self):
        return self.settings.get_exchange_folder()

    def start_rizom(self):
        return self.client.connect()
        
    def close_rizom(self, force=False):
        self.client.close(force)
        
    def is_rizom_running(self):
        return self.client.is_running()
        
    # Helpers needed by UI
    @property
    def link(self):
        return self.client.link
        
    def send_mesh(self, fbx_path):
        # 1. Start Rizom (Load Mesh handles connect, but good to ensure)
        if not self.client.connect():
             return False
             
        # 2. Rizom Load
        return self.client.load_mesh(fbx_path)

    def get_mesh(self, fbx_path):
        return self.client.save_mesh(fbx_path)

    def run_script(self, script_path):
        return self.client.run_script(script_path)
        

    def unfold(self):
        return self.client.unfold()
        
    def pack(self):
        return self.client.pack()
        
    def cut(self):
        return self.client.cut()

    def optimize(self):
        return self.client.optimize()

    def weld_all(self):
        return self.client.weld_all()
        
    def weld_selected(self):
        return self.client.weld_selected()

    def set_element_mode(self, mode):
        return self.client.set_element_mode(mode)
        
    def set_element_mode(self, mode):
        return self.client.set_element_mode(mode)

    def sync_selection(self):
        # 1. Get Selection from Max
        mode, ids = self.max_ops.get_selection()
        
        if mode == -1:
             # Could be object mode or invalid
             return False
             
        # 2. Set Mode
        if not self.client.set_element_mode(mode):
            return False
        
        # 3. Select Components
        # Even if ids is empty, we might want to clear selection?
        # Select command with empty IDs and ResetBefore=True will clear.
        return self.client.select(mode, ids)

    # expose max ops
    def prepare_temp_objects(self, objects):
        return self.max_ops.prepare_temp_objects(objects)
        
    def cleanup_object(self, obj):
        self.max_ops.cleanup_object(obj)
        
    def export_fbx(self, path, selected=True):
        ver = self.settings.get_ini_setting("FileFormat", "FBX_Version_sys")
        self.max_ops.export_fbx(path, fbx_version=ver, selected=selected)
        
    def import_fbx(self, path):
        self.max_ops.import_fbx(path)
        
    def transfer_uvs_from_imported(self, objects):
        self.max_ops.transfer_uvs_from_imported(objects)

