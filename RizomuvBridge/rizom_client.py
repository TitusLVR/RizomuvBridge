import os
import sys
import time
import subprocess
from pymxs import runtime as rt

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

# We assume RizomUVLink path is already in sys.path via __init__ or logic in this file
# To be safe, let's ensure it is hooked up.
try:
    # Attempt import
    from RizomUVLink import CRizomUVLink
except ImportError:
    # Try to find it relative to this file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    _rizom_link_path = os.path.join(current_dir, "RizomUVLink")
    
    if _rizom_link_path not in sys.path:
        sys.path.append(_rizom_link_path)
    
    try:
        from RizomUVLink import CRizomUVLink
    except ImportError as e:
        # Fallback to standard install location just in case
        try:
             _userscripts = rt.getDir(rt.Name("userscripts"))
             _rizom_link_path_std = os.path.join(_userscripts, "RizomuvBridge", "RizomUVLink")
             if _rizom_link_path_std not in sys.path and os.path.exists(_rizom_link_path_std):
                sys.path.append(_rizom_link_path_std)
             from RizomUVLink import CRizomUVLink
        except:
             print(f"Failed to import RizomUVLink: {e}")
             CRizomUVLink = None

class RizomClient:
    def __init__(self, settings):
        self.settings = settings
        self.link = None
        self.port = None

    def is_running(self):
        # 1. Reliable: Check active connection if port is known
        if self.link and self.port:
            try:
                if self.link.TCPPortIsOpen(self.port):
                    return True
            except:
                pass
                
        
        exe_name = self.settings.get_ini_setting("ProccessName", "exeName", "rizomuv.exe")
        if not exe_name:
            exe_name = "rizomuv.exe"
            
        proc_name = exe_name.lower().replace(".exe", "")
        
        if PSUTIL_AVAILABLE:
            for proc in psutil.process_iter(['name']):
                try:
                    if proc.info['name'].lower().startswith(proc_name):
                        return True
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
            return False
        else:
            try:
                out = subprocess.check_output(['tasklist', '/FI', f'IMAGENAME eq {exe_name}'], shell=True).decode()
                if exe_name.lower() in out.lower():
                    return True
            except:
                pass
            return False

    def connect(self):
        if CRizomUVLink is None:
            raise Exception("RizomUVLink module not loaded.")
        
        if self.link is None:
            self.link = CRizomUVLink()
            
        # 1. Try to reuse existing connection if already active
        if self.port and self.link.TCPPortIsOpen(self.port):
             try:
                 # Verify we are still talking to it
                 self.link.RizomUVVersion() 
                 return True
             except:
                 # Link dead or port closed
                 self.port = None
                 
        # 2. Check if we can connect to saved port (regardless of process check)
        saved_port = self.settings.get_port()
        
        # If we have a saved port, check if it is open (this is the ultimate "is running" check)
        if saved_port and self.link.TCPPortIsOpen(saved_port):
             try:
                 print(f"RizomUV port {saved_port} is open. Connecting...")
                 self.link.Connect(saved_port)
                 # Verify connection
                 ver = self.link.RizomUVVersion()
                 if ver:
                     print(f"Connected to existing RizomUV {ver}")
                     self.port = saved_port
                     return True
             except Exception as e:
                 print(f"Failed to connect to existing instance on port {saved_port}: {e}")
                 # Fall through to launch new
        
        # 3. Launch new instance
        exe_path = self.settings.get_rizom_path()
        
        # If no custom path set, try to find via Registry
        if not exe_path or not os.path.exists(exe_path):
             # Try registry
             try:
                 reg_path = self.link.RizomUVWinRegisterInstallPath()
                 if reg_path:
                     exe_path = os.path.join(reg_path, "rizomuv.exe")
                     print(f"Found RizomUV via registry: {exe_path}")
             except:
                 pass
        
        # If still None, RunRizomUV will use its default relative logic (RizomUVPath)
        
        try:
            self.port = self.link.RunRizomUV(exePath=exe_path, connect=True, wait=True)
            if self.port:
                self.settings.set_port(self.port)
                # If we detected a path and it works, maybe save it?
                # Or keep it auto. Let's keep it auto unless user explicitly sets it.
            return True
        except Exception as e:
            print(f"RizomUV Connection Failed: {e}")
            return False

    def close(self, force=False):
        print("Closing RizomUV...")
        
        # clean exit via Link if possible
        if not force and self.link and self.port:
            try:
                # Try calling Quit() directly on the link wrapper if it exposes it,
                # or Execute "Quit" command if that is the mechanism.
                # User specifically requested link.Quit() style.
                # Checking if method exists or just calling it.
                if hasattr(self.link, "Quit"):
                    self.link.Quit()
                else:
                     # Fallback to Execute("Quit")
                     try:
                        self.link.Execute("Quit", {})
                     except:
                        pass
                
                # Wait briefly for it to close
                import time
                time.sleep(0.5)
            except Exception as e:
                print(f"Clean exit failed: {e}")
        
        # Always force kill as per latest requirement if it's still running
        # (Or if user asks for force kill, but even consistently to ensure cleanup)
        self._force_kill()
        self.link = None
        self.port = None

    def _force_kill(self):
        exe_name = self.settings.get_ini_setting("ProccessName", "exeName", "rizomuv.exe")
        if not exe_name:
            exe_name = "rizomuv.exe"
        
        # Method 1: Max DOS Command (Most reliable in this context)
        try:
            # Check if running first to avoid error spam? taskkill handles "not found" gracefully usually (or prints error)
            cmd = f'taskkill /F /IM "{exe_name}"'
            rt.dosCommand(cmd)
        except:
            pass
            
        # Method 2: Subprocess (Fallback)
        try:
            subprocess.call(['taskkill', '/F', '/IM', exe_name], shell=True)
        except:
            pass

    def load_mesh(self, filepath, file_format=None):
        if not self.connect():
             return False
        
        is_usd = False
        if file_format:
            is_usd = (file_format.upper() == "USD")
        else:
            is_usd = filepath.lower().endswith(('.usd', '.usda', '.usdc'))
        
        params = {
            "File.Path": filepath,
            "File.XYZUVW": True,
            "File.UV": True, 
            "File.Meta": True,
            "File.Normals": not is_usd, # User requested normals off for USD import in Rizom
            "File.ImportGroups": True,
        }


        
        # Add FBX specific params only if FBX
        if filepath.lower().endswith(".fbx") or (file_format and file_format.upper() == "FBX"):
             params["File.FBX.UseUVSetNames"] = True
        try:
            self.link.Load(params)
            return True
        except Exception as e:
            print(f"Load Mesh Failed: {e}")
            return False

    def save_mesh(self, fbx_path):
        if not self.connect():
             return False
        
        params = {
            "File.Path": fbx_path,
            "File.UVWProps": True
        }
        try:
            self.link.Save(params)
            return True
        except Exception as e:
            print(f"Save Mesh Failed: {e}")
            return False

    def run_script(self, script_path):
        if not self.connect():
             return False
             
        try:
            # Method: Remote Control File Watcher
            # 1. Enable monitoring
            self.link.Set({"Path": "Prefs.RemoteControlFileMonitoringOn", "Value": True})
            
            # 2. Set Path
            safe_path = script_path.replace("\\", "/")
            self.link.Set({"Path": "Prefs.RemoteControlFilePath", "Value": safe_path})
            
            # 3. Touch file to trigger
            os.utime(script_path, None)
            
            return True
        except Exception as e:
            print(f"Run Script Failed: {e}")
            return False

    def check_connection(self):
         if not self.connect():
             return False
         return True

    def unfold(self, params={}):
        if not self.check_connection(): return False
        try:
            # Default params if empty
            if not params:
                params = {
                    'PrimType': "Island", 
                    'WorkingSet': "Visible&UnLocked", 
                    'Mix': 1, 
                    'RoomSpace': 0, 
                    'MinAngle': 1e-05, 
                    'PreIterations': 5, 
                    'StopIfOutOFDomain': False, 
                    'PinMapName': "Pin", 
                    'BorderIntersections': True, 
                    'TriangleFlips': True, 
                    'FillHoles': True
                }
            self.link.Execute("Unfold", params)
            return True
        except Exception as e:
            print(f"Unfold Failed: {e}")
            return False

    def pack(self, params={}):
        if not self.check_connection(): return False
        try:
            if not params:
                params = {'WorkingSet': "Visible", 'AuxGroup': "RootGroup", 'Translate': True}
            self.link.Execute("Pack", params)
            return True
        except Exception as e:
            print(f"Pack Failed: {e}")
            return False

    def cut(self, params={}):
        if not self.check_connection(): return False
        try:
            if not params:
                params = { "PrimType": "Edge", "WorkingSet": "Visible" }
            self.link.Execute("Cut", params)
            return True
        except Exception as e:
            print(f"Cut Failed: {e}")
            return False

    def set_element_mode(self, mode):
        # 0: Vertex, 1: Edge, 2: Polygon, 3: Island
        if not self.check_connection(): return False
        try:
            # Try ZomSet then Set
            params = {"Path": "Vars.EditMode.ElementMode", "Value": int(mode)}
            try:
                self.link.Set(params) # Found in base
            except:
                self.link.Execute("ZomSet", params)
            return True
        except Exception as e:
            print(f"Set Element Mode Failed: {e}")
            return False

    def weld_all(self):
         if not self.check_connection(): return False
         try:
             # 1. Set Edge Mode (Mode 1)
             self.set_element_mode(1)
             
             # 2. Select All Edges
             select_params = {'PrimType':"Edge", 'WorkingSet':"Visible", 'Select':True, 'All':True}
             self.link.Select(select_params)
             
             # 3. Weld
             weld_params = {'PrimType':"Edge", 'WorkingSet':"Visible&UnLocked", 'Mode':"All"}
             self.link.Execute("Weld", weld_params)
             
             return True
         except Exception as e:
             print(f"Weld All Failed: {e}")
             return False

    def weld_selected(self):
         if not self.check_connection(): return False
         try:
             # User specified command parameters, but ZomWeld is not found. Using Weld.
             params = {"PrimType": "Polygon", "WorkingSet": "Visible&UnLocked", "Mode": "All"}
             self.link.Execute("Weld", params)
             return True
         except Exception as e:
             print(f"Weld Selected Failed: {e}")
             return False

    def optimize(self, iterations=None, room_space=None):
        if not self.check_connection(): return False
        try:
            params = {}
            if iterations is not None:
                params["Iterations"] = int(iterations)
            if room_space is not None:
                params["RoomSpace"] = float(room_space)
                
            self.link.Optimize(params)
            return True
        except Exception as e:
            print(f"Optimize Failed: {e}")
            return False

    def select(self, mode, ids):
        if not self.check_connection(): return False
        try:
            # Map mode int to PrimType string
            prim_type = "Polygon"
            if mode == 0: prim_type = "Vertex"
            elif mode == 1: prim_type = "Edge"
            elif mode == 2: prim_type = "Polygon"
            elif mode == 3: prim_type = "Island"
            
            # Select command
            params = {
                "PrimType": prim_type,
                "IDs": ids,
                "ResetBefore": True,
                "Select": True,
                "List": True,
                "XYZSpace": True,
                "WorkingSet": "Visible"
            }
            
            if mode == 1: # Edge
                 params["EdgesAsPolyEdgeIDs"] = True
                 
            self.link.Select(params)
            return True
        except Exception as e:
            print(f"Select Failed: {e}")
            return False
