try:
    from PySide6 import QtWidgets, QtCore, QtGui
except ImportError:
    from PySide2 import QtWidgets, QtCore, QtGui
import os
import importlib
from pymxs import runtime as rt

# Force reload dependencies to ensure updates are picked up in 3ds Max
from . import settings
from . import max_ops
from . import rizom_client
from . import core

importlib.reload(settings)
importlib.reload(max_ops)
importlib.reload(rizom_client)
importlib.reload(core)

from .core import RizomUVBridgeCore

class CollapsibleBox(QtWidgets.QWidget):
    def __init__(self, title="", parent=None):
        super(CollapsibleBox, self).__init__(parent)
        self.toggle_button = QtWidgets.QToolButton(text=title, checkable=True, checked=False)
        self.toggle_button.setStyleSheet("QToolButton { border: none; font-weight: bold; }")
        self.toggle_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toggle_button.setArrowType(QtCore.Qt.RightArrow)
        self.toggle_button.toggled.connect(self.on_toggled)

        self.content_area = QtWidgets.QFrame()
        self.content_area.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.content_area.setFrameShadow(QtWidgets.QFrame.Raised)
        self.content_area.setVisible(False)

        
        lay = QtWidgets.QVBoxLayout(self)
        lay.setSpacing(0)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self.toggle_button)
        lay.addWidget(self.content_area)
        
        # Animations
        self.anim = QtCore.QParallelAnimationGroup()
        self.anim.finished.connect(self.on_anim_finished)
        
    def on_toggled(self, checked):
        self.toggle_button.setArrowType(QtCore.Qt.DownArrow if checked else QtCore.Qt.RightArrow)
        self.content_area.setVisible(checked)
        
    def on_anim_finished(self):
        pass

    def setContentLayout(self, layout):
        self.content_area.setLayout(layout)



class RizomUVBridgeDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(RizomUVBridgeDialog, self).__init__(parent)
        self.setWindowTitle("RizomUV Bridge")
        # self.resize(250, 300) # Removed for dynamic resizing

        
        # Ensure window is always on top
        # Ensure window is always on top (PySide2/6 compat)
        try:
            flag = QtCore.Qt.WindowStaysOnTopHint
        except AttributeError:
            flag = QtCore.Qt.WindowType.WindowStaysOnTopHint
        self.setWindowFlags(self.windowFlags() | flag)
        
        self.core = RizomUVBridgeCore()
        
        # UI State Variables
        self.mode = "New" # New, Edit. "Preset"/"Batch" removed or integrated?
        # User asked for "Send" and "Get" buttons
        
        self.temp_file_base = self.core.get_ini_setting("ExchangeFolder", "TempFile", "rizomuv_temp")
        self.temp_file_out = self.core.get_ini_setting("ExchangeFolder", "TempFile_out", "rizomuv_temp_out")
        
        self.setup_ui()
        
    def set_icon(self, button, icon_name):
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(base_dir, "IMG", icon_name)
            if os.path.exists(icon_path):
                button.setIcon(QtGui.QIcon(icon_path))
                button.setIconSize(QtCore.QSize(16, 16))
        except Exception as e:
            print(f"Icon load error for {icon_name}: {e}")

    def setup_ui(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        try:
             main_layout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        except AttributeError:
             # PySide6 might use SizeConstraint enum
             main_layout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetFixedSize)

        

        
        # --- Actions (Send/Get) ---
        # Kept separate but visibility controlled
        # Kept separate but visibility controlled
        action_layout = QtWidgets.QGridLayout()
        
        self.btn_send = QtWidgets.QPushButton("Send")
        self.btn_send.setMinimumHeight(24)
        self.set_icon(self.btn_send, "rizomuv.png")
        self.btn_send.clicked.connect(self.on_send_clicked)
        
        self.btn_get = QtWidgets.QPushButton("Get")
        self.btn_get.setMinimumHeight(24)
        self.set_icon(self.btn_get, "rizomuv_get.png")
        self.btn_get.clicked.connect(self.on_get_clicked)
        
        # Grid: Send|Get  Sync(Full)
        action_layout.addWidget(self.btn_send, 0, 0)
        action_layout.addWidget(self.btn_get, 0, 1)
        
        self.btn_sync = QtWidgets.QPushButton("Sync Sel")
        self.btn_sync.setMinimumHeight(24)
        self.set_icon(self.btn_sync, "rizomuv_refresh.png")
        self.btn_sync.setToolTip("Sync Selection Mode from Max")
        self.btn_sync.clicked.connect(self.on_sync_selection_clicked)
        action_layout.addWidget(self.btn_sync, 1, 0, 1, 2)
        

        
        self.layout_actions = action_layout # Save ref if needed, or just toggle buttons
        main_layout.addLayout(action_layout)
        
        # --- RizomUV Tools Group ---
        self.group_tools = QtWidgets.QGroupBox("RizomUV Tools")
        self.group_tools.setMinimumWidth(230) # Ensure window width is constant
        tools_layout = QtWidgets.QGridLayout()

        
        self.btn_cut = QtWidgets.QPushButton("Cut")
        self.set_icon(self.btn_cut, "rizomuv_cut.png")
        self.btn_cut.clicked.connect(self.on_cut_clicked)
        
        self.btn_unfold = QtWidgets.QPushButton("Unfold")
        self.set_icon(self.btn_unfold, "rizomuv_unfold.png")
        self.btn_unfold.clicked.connect(self.on_unfold_clicked)
        
        self.btn_pack = QtWidgets.QPushButton("Pack")
        self.set_icon(self.btn_pack, "rizomuv_pack.png")
        self.btn_pack.clicked.connect(self.on_pack_clicked)
        
        self.btn_weld = QtWidgets.QPushButton("Weld All")
        self.set_icon(self.btn_weld, "rizomuv_weld.png")
        self.btn_weld.clicked.connect(self.on_weld_clicked)
        
        self.btn_weld_selected = QtWidgets.QPushButton("Weld Selected")
        self.set_icon(self.btn_weld_selected, "rizomuv_weld.png")
        self.btn_weld_selected.clicked.connect(self.on_weld_selected_clicked)
        
        self.btn_optimize = QtWidgets.QPushButton("Optimize")
        self.set_icon(self.btn_optimize, "rizomuv_optimize.png")
        self.btn_optimize.clicked.connect(self.on_optimize_clicked)



        # Order Requested:
        # Row 0: Weld All | Weld Selected
        # Row 1: Cut (ColSpan 2)
        # Row 2: Unfold | Optimize
        # Row 3: Pack (ColSpan 2)
        
        tools_layout.addWidget(self.btn_weld, 0, 0)
        tools_layout.addWidget(self.btn_weld_selected, 0, 1)
        tools_layout.addWidget(self.btn_cut, 1, 0, 1, 2)
        tools_layout.addWidget(self.btn_unfold, 2, 0)
        tools_layout.addWidget(self.btn_optimize, 2, 1)

        tools_layout.addWidget(self.btn_pack, 3, 0, 1, 2)


        
        self.group_tools.setLayout(tools_layout)
        main_layout.addWidget(self.group_tools)
        
        # --- Script Section ---
        self.script_group = QtWidgets.QGroupBox("Scripts")
        script_layout = QtWidgets.QVBoxLayout()
        
        # Folder Selection
        folder_layout = QtWidgets.QHBoxLayout()
        self.lbl_folder = QtWidgets.QLabel("Folder:")
        self.btn_folder = QtWidgets.QPushButton("...")
        self.btn_folder.setFixedWidth(30)
        self.btn_folder.clicked.connect(self.on_set_folder_clicked)
        folder_layout.addWidget(self.lbl_folder)
        folder_layout.addWidget(self.btn_folder)
        script_layout.addLayout(folder_layout)
        
        # Script Dropdown & Run
        run_layout = QtWidgets.QHBoxLayout()
        self.combo_scripts = QtWidgets.QComboBox()
        self.refresh_scripts()
        
        self.btn_run_script = QtWidgets.QPushButton("Run Script")
        self.btn_run_script.setFixedWidth(80)
        self.btn_run_script.clicked.connect(self.on_run_script_clicked)
        
        run_layout.addWidget(self.combo_scripts)
        run_layout.addWidget(self.btn_run_script)
        script_layout.addLayout(run_layout)
        
        self.script_group.setLayout(script_layout)
        main_layout.addWidget(self.script_group)
        


        # --- RizomUV Link Group ---
        self.group_link = QtWidgets.QGroupBox("RizomUVLink")
        link_layout = QtWidgets.QHBoxLayout()
        
        self.btn_start = QtWidgets.QPushButton("Start RizomUV")
        self.set_icon(self.btn_start, "rizomuv.png")
        self.btn_start.clicked.connect(self.on_start_clicked)

        
        self.btn_close = QtWidgets.QPushButton("Close RizomUV")
        self.set_icon(self.btn_close, "rizomuv_close.png")
        self.btn_close.clicked.connect(self.on_close_clicked)
        
        link_layout.addWidget(self.btn_start)
        link_layout.addWidget(self.btn_close)
        self.group_link.setLayout(link_layout)
        
        main_layout.addWidget(self.group_link)

        # --- Preferences (Collapsible) ---
        self.group_pref = CollapsibleBox("Preferences")
        pref_layout = QtWidgets.QVBoxLayout()
        
        # --- File Format (Grouped) ---
        self.group_file_format = QtWidgets.QGroupBox("File Format")
        format_layout = QtWidgets.QHBoxLayout()
        format_layout.addWidget(QtWidgets.QLabel("Type:"))
        self.combo_file_type = QtWidgets.QComboBox()
        self.combo_file_type.addItems(["USD", "FBX"])
        self.combo_file_type.setCurrentIndex(1) 
        self.combo_file_type.currentIndexChanged.connect(self.on_file_type_changed)
        format_layout.addWidget(self.combo_file_type)
        
        self.lbl_fbx_ver = QtWidgets.QLabel("FBX Ver:")
        format_layout.addWidget(self.lbl_fbx_ver)
        self.combo_fbx = QtWidgets.QComboBox()
        self.combo_fbx.addItems(["FBX201200", "FBX202000"]) 
        format_layout.addWidget(self.combo_fbx)
        format_layout.addStretch()
        self.group_file_format.setLayout(format_layout)
        pref_layout.addWidget(self.group_file_format)
        
        # --- Cleanup Options (Grouped) ---
        self.group_cleanup = QtWidgets.QGroupBox("Export Cleanup Options")
        cleanup_layout = QtWidgets.QVBoxLayout()
        
        self.chk_collapse_dead = QtWidgets.QCheckBox("Collapse Dead Structs")
        self.chk_collapse_dead.setChecked(True) 
        cleanup_layout.addWidget(self.chk_collapse_dead)
        
        self.chk_del_iso_verts = QtWidgets.QCheckBox("Delete Iso Verts")
        self.chk_del_iso_verts.setChecked(True)
        cleanup_layout.addWidget(self.chk_del_iso_verts)
        
        self.chk_del_iso_map = QtWidgets.QCheckBox("Delete Iso Map Verts")
        self.chk_del_iso_map.setChecked(True)
        cleanup_layout.addWidget(self.chk_del_iso_map)
        
        self.chk_rebuild_poly = QtWidgets.QCheckBox("Rebuild Poly (Mesh->Poly)")
        self.chk_rebuild_poly.setChecked(True)
        cleanup_layout.addWidget(self.chk_rebuild_poly)
        
        self.group_cleanup.setLayout(cleanup_layout)
        pref_layout.addWidget(self.group_cleanup)

        # Mesh Inspector (Bottom)
        self.btn_inspector = QtWidgets.QPushButton("Mesh Inspector")
        self.btn_inspector.clicked.connect(self.on_inspector_clicked)
        pref_layout.addWidget(self.btn_inspector)
        # Help Button
        self.btn_help = QtWidgets.QPushButton("Help")
        self.btn_help.clicked.connect(self.on_help_clicked)
        pref_layout.addWidget(self.btn_help)


        self.group_pref.setContentLayout(pref_layout)
        main_layout.addWidget(self.group_pref)


        
        main_layout.addStretch()
        
        # Initial State
        self.update_ui_state()


    def on_file_type_changed(self, index=None):
        is_usd = self.combo_file_type.currentText() == "USD"
        self.lbl_fbx_ver.setVisible(not is_usd)
        self.combo_fbx.setVisible(not is_usd)

    def update_ui_state(self):
        is_running = self.core.is_rizom_running()
        
        # Link Group
        self.btn_start.setVisible(not is_running)
        self.btn_close.setVisible(is_running)
        
        # Other Elements
        self.btn_send.setVisible(is_running)
        self.btn_get.setVisible(is_running)
        self.btn_sync.setVisible(is_running)
        self.group_tools.setVisible(is_running)
        self.script_group.setVisible(is_running)
        self.group_tools.setVisible(is_running)
        self.script_group.setVisible(is_running)
        self.group_pref.setVisible(is_running)

        
        if is_running:
            self.on_file_type_changed()
        
        # Resize window to fit content
        self.adjustSize()

    def refresh_scripts(self):
        self.combo_scripts.clear()
        scripts = self.core.get_available_scripts()
        if scripts:
            self.combo_scripts.addItems(scripts)
            self.combo_scripts.setEnabled(True)
        else:
            self.combo_scripts.addItem("No scripts found")
            self.combo_scripts.setEnabled(False)
            
    def ensure_connection(self):
        if self.core.link and self.core.is_rizom_running():
            return True
            
        # Try to start/connect
        if self.core.start_rizom():
            return True
            
        # Failed, ask user
        path = self.core.get_rizom_path()
        if not path or not os.path.exists(path):
             res = QtWidgets.QMessageBox.question(self, "RizomUV Not Found", "RizomUV executable not found or connection failed.\nDo you want to specify the path manually?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
             if res == QtWidgets.QMessageBox.Yes:
                 exe_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select RizomUV Executable", "C:\\", "Executables (*.exe)")
                 if exe_path:
                     self.core.set_ini_setting("Path", "rizomuv", exe_path)
                     if self.core.start_rizom():
                         return True
        
        QtWidgets.QMessageBox.critical(self, "Error", "Could not connect to RizomUV.")
        return False

    def on_start_clicked(self):
        self.ensure_connection()
        self.update_ui_state()

    def on_set_folder_clicked(self):
        current = self.core.get_scripts_folder()
        new_folder = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Scripts Folder", current)
        if new_folder:
            self.core.set_scripts_folder(new_folder)
            self.refresh_scripts()


    def on_close_clicked(self):
        # Default to safe close
        self.core.close_rizom(force=False)
        self.update_ui_state()

    def on_send_clicked(self):
        selection = list(rt.selection)
        if not selection:
            QtWidgets.QMessageBox.warning(self, "Selection", "Please select objects.")
            return

        rebuild_poly = self.chk_rebuild_poly.isChecked()
        valid_objs = []
        
        if rebuild_poly:
             # Accept all Geometry if conversion is enabled
             valid_objs = [o for o in selection if rt.superClassOf(o) == rt.GeometryClass]
        else:
             # Strict check: Base Object must be Editable Poly or Editable Mesh
             valid_objs = []
             for o in selection:
                 if rt.isKindOf(o.baseObject, rt.Editable_Poly) or rt.isKindOf(o.baseObject, rt.Editable_Mesh):
                     valid_objs.append(o)
                     
        if not valid_objs:
             # Nothing to export, silent return or warning? User said "skip".
             # If selection was not empty but valid is empty, we just do nothing.
             if selection:
                 pass # Silent skip as requested ("If not -> skip")
             else:
                 # If selection was empty initially (handled above), but double check
                 pass
             return


        # Prepare Logic
        # Prepare Logic
        exchange_folder = self.core.get_exchange_folder()
        
        fmt = self.combo_file_type.currentText()
        ext = ".fbx"
        if fmt == "USD": 
            ext = ".usd"
            
        file_path = os.path.join(exchange_folder, self.temp_file_base + ext)
        
        # Check Mode
        # If New, maybe clear channels? 
        # For now, we trust the user knows "New" implies new UVs in Rizom.
        # Rizom "New" is handled by link.Load(XYZ=True) (without XYZUVW=True) usually, 
        # or we rely on Rizom UI.
        # But core.send_mesh sends with ImportGroups=True, XYZ=True, UV=True.
        # If we want "New", we maybe shouldn't send UVs?
        # Actually export_fbx sends what is in Max. If Max has UVs, they go.
        # If user selected "New (Clean)" we should clear channels on the TEMP objects.
        
        # Only apply channel fix for FBX. USD handles named channels differently 
        # and forcefully filling empty channels causes "index out of range" errors in USD.
        export_type_val = fmt
        if export_type_val == "FBX":
            fix_missing_channels = True
        else: # USD
            fix_missing_channels = False
            
        # Gather Cleanup Opts
        cleanup_opts = {
            "collapse_dead_structs": self.chk_collapse_dead.isChecked(),
            "delete_iso_verts": self.chk_del_iso_verts.isChecked(),
            "delete_iso_map_verts": self.chk_del_iso_map.isChecked(),
            "rebuild_poly": self.chk_rebuild_poly.isChecked()
        }
            
        temp_objs = self.core.prepare_temp_objects(valid_objs, fix_missing_channels=fix_missing_channels, cleanup_opts=cleanup_opts)

        
        # Cleanup geometry
        for o in temp_objs:
             self.core.cleanup_object(o)
             # All channels preserved as requested

        # Export
        rt.select(temp_objs)
        if fmt == "USD":
            self.core.export_usd(file_path, selected=True)
        else:
            self.core.export_fbx(file_path, selected=True)
            
        rt.delete(temp_objs)
        rt.select(valid_objs)
        
        # Send
        success = self.core.send_mesh(file_path, file_format=fmt)
        if not success:
            QtWidgets.QMessageBox.critical(self, "Error", "Failed to communicate with RizomUV.")
            return

        # Redraw Viewports as requested
        rt.redrawViews()

        # Auto-Run Logic (Implicit)

        try:
             self.core.link.Set({'Path': "Prefs.RemoteControlFileMonitoringOn", 'Value': True})
        except:
             pass

    def on_get_clicked(self):
        exchange_folder = self.core.get_exchange_folder()
        
        fmt = self.combo_file_type.currentText()
        ext = ".fbx"
        if fmt == "USD": 
            ext = ".usd"
            
        out_path = os.path.join(exchange_folder, self.temp_file_out + ext)
        
        # Helper to ensure file cleans up
        if os.path.exists(out_path):
            try:
                os.remove(out_path)
            except:
                pass
                
        # Get
        success = self.core.get_mesh(out_path)
        if not success:
            QtWidgets.QMessageBox.critical(self, "Error", "Failed to retrieve mesh from RizomUV.")
            return
            
        if not os.path.exists(out_path):
             QtWidgets.QMessageBox.warning(self, "Warning", "RizomUV did not save the file. Did you forget to pack/save inside Rizom?")
             return
             
        # Import
        # Import
        self.import_results(out_path)

    def on_run_script_clicked(self):
        script_name = self.combo_scripts.currentText()
        if not script_name or script_name == "No scripts found":
            return
            
        folder = self.core.get_scripts_folder()
        path = os.path.join(folder, script_name)
        
        if not os.path.exists(path):
            QtWidgets.QMessageBox.warning(self, "Error", "Script file not found.")
            return

        success = self.core.run_script(path)
        if not success:
             QtWidgets.QMessageBox.critical(self, "Error", "Failed to run script.")

    def on_cut_clicked(self):
        self.core.cut()

    def on_unfold_clicked(self):
        self.core.unfold()
        
    def on_optimize_clicked(self):
        self.core.optimize()

    def on_pack_clicked(self):
        self.core.pack()

    def on_inspector_clicked(self):
        self.core.open_inspector()
        QtWidgets.QMessageBox.information(self, "Mesh Inspector", "Mesh Inspector triggered.\n\nNote: The dialog only appears if errors are found.")



    def on_help_clicked(self):
        # Open Help URL
        url = QtCore.QUrl("https://tituslvr.github.io/RizomuvBridge/")
        QtGui.QDesktopServices.openUrl(url)

    def on_weld_clicked(self):
        self.core.weld_all() 

    def on_weld_selected_clicked(self):
        self.core.weld_selected()
        
    def on_sync_selection_clicked(self):
        self.core.sync_selection()

    def import_results(self, file_path):
        old_objs = list(rt.objects) # List for safe snapshot
        
        if file_path.lower().endswith(".usd") or file_path.lower().endswith(".usda") or file_path.lower().endswith(".usdc"):
             self.core.import_usd(file_path)
        else:
             self.core.import_fbx(file_path)
        
        curr_objs = list(rt.objects)
        new_objs = [o for o in curr_objs if o not in old_objs]
        
        self.core.transfer_uvs_from_imported(new_objs)
        # Focus Viewport (Zoom Extents Selected)
        try:
            # actionMan.executeAction 0 "310"  -- Tools: Zoom Extents Selected
            rt.actionMan.executeAction(0, "310")
        except:
            pass
            
        rt.redrawViews()




def show():
    # Helper to show dialog
    # Parent to Max Window handle usually needed
    parent = None
    try:
        max_hwnd = rt.windows.getMAXHWND()
    except:
        max_hwnd = None
        
    # PySide2 parenting to HWND is tricky without a helper; 
    # usually `GetQMaxMainWindow()` if available (in 2025/2024?) or generic parenting.
    # For now, parent=None is acceptable for a top-level tool.
    
    global _rizom_dialog
    try:
        _rizom_dialog.close()
    except:
        pass
        
    _rizom_dialog = RizomUVBridgeDialog(parent)
    _rizom_dialog.show()

