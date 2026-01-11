from pymxs import runtime as rt
import time

class RizomUVBridgeMaxOps:
    
    @staticmethod
    def export_fbx(filepath, fbx_version=None, selected=True):
        rt.pluginManager.loadClass(rt.FBXEXP)
        
        rt.FBXExporterSetParam("Animation", False)
        rt.FBXExporterSetParam("ASCII", True)
        rt.FBXExporterSetParam("Cameras", False)
        rt.FBXExporterSetParam("ColladaTriangulate", False) 
        rt.FBXExporterSetParam("Lights", False)
        rt.FBXExporterSetParam("NormalsPerPoly", False)
        rt.FBXExporterSetParam("Preserveinstances", False)
        rt.FBXExporterSetParam("Removesinglekeys", False)
        rt.FBXExporterSetParam("Shape", False)
        rt.FBXExporterSetParam("Skin", False)
        rt.FBXExporterSetParam("ShowWarnings", False)
        rt.FBXExporterSetParam("SmoothingGroups", True)
        rt.FBXExporterSetParam("SmoothMeshExport", True)


        rt.FBXExporterSetParam("TangentSpaceExport", False)
        rt.FBXExporterSetParam("Triangulate", False)
        rt.FBXExporterSetParam("UpAxis", "Y")
        rt.FBXExporterSetParam("UseSceneName", False)
        rt.FBXExporterSetParam("UseSceneName", False)
        rt.FBXExporterSetParam("PreserveEdgeOrientation", False)
        rt.FBXExporterSetParam("MappingCoordinates", True) # Ensure UV channels are exported
        
        if fbx_version:
             rt.FBXExporterSetParam("FileVersion", fbx_version)

        rt.exportFile(filepath, rt.Name("noPrompt"), selectedOnly=selected, usage=rt.FBXEXP)

    @staticmethod
    def export_usd(filepath, selected=True):
        # Explicitly set UpAxis to Y for Rizom (which expects Y-up)
        # 3ds Max is Z-up. Rizom expects Y-up.
        try:
             # Max 2022/2023+ USD Interface
             usd_opts = rt.USDExporter.CreateOptions()
             
             # User Example Integration
             # MaxScript Docs say: UpAxis expects a Name value #y or #z
             # User requested specific order
             usd_opts.Meshes = True
             usd_opts.Lights = False
             usd_opts.Cameras = False
             usd_opts.Materials = False
             
             # usd_opts.FileFormat = rt.Name("ascii") # Optional, defaults to binary/ext usually
             
             usd_opts.UpAxis = rt.Name("y") 
             
             # usd_opts.LogLevel = rt.Name("info")
             # usd_opts.LogPath = ...
             
             usd_opts.PreserveEdgeOrientation = False # Keep False to prevent faceting
             usd_opts.Normals = rt.Name("asPrimvar") 
             usd_opts.TimeMode = rt.Name("current")
             
             # Extra settings we added
             usd_opts.BakeObjectOffsetTransform = True 
             usd_opts.MeshFormat = rt.Name("polyMesh")
             usd_opts.Shapes = False
             
             print(f"Exporting USD to {filepath} using USDExporter Interface with UpAxis=Y")

             # We need to pass the selected nodes if selected=True
             if selected:
                 # Get selection as safe python list for nodeList argument
                 sel_list = list(rt.selection)
                 rt.USDExporter.ExportFile(filepath, exportOptions=usd_opts, nodeList=sel_list, contentSource=rt.Name("nodeList"))
             else:
                 rt.USDExporter.ExportFile(filepath, exportOptions=usd_opts)
             
             return
        except Exception as e:
             # Important: Print error to see if we are falling back
             print(f"Advanced USD Export failed (Falling back to legacy): {e}")
             pass

        # Fallback for older versions or if interface differs
        rt.exportFile(filepath, rt.Name("noPrompt"), selectedOnly=selected, using=rt.USDExporter)

    @staticmethod
    def import_fbx(filepath):
        rt.pluginManager.loadClass(rt.FBXIMP)
        rt.FBXImporterSetParam("Mode", rt.Name("create"))
        rt.FBXImporterSetParam("Animation", False)
        rt.FBXImporterSetParam("Skin", False)
        rt.FBXImporterSetParam("Shape", False)
        rt.FBXImporterSetParam("SmoothingGroups", True)
        rt.FBXImporterSetParam("Cameras", False)
        rt.FBXImporterSetParam("Lights", False)
        rt.FBXImporterSetParam("UpAxis", "Y")
        rt.FBXImporterSetParam("ScaleConversion", False)
        rt.FBXImporterSetParam("GenerateLog", False)
        
        rt.importFile(filepath, rt.Name("noprompt"), usage=rt.FBXIMP)

    @staticmethod
    def import_usd(filepath):
        rt.importFile(filepath, rt.Name("noprompt"), using=rt.USDImporter)

    @staticmethod
    def prepare_temp_objects(objects, fix_missing_channels=False, cleanup_opts=None):
        if cleanup_opts is None:
            cleanup_opts = {}
            
        temp_objs = []
        timestamp = str(int(time.time()))
        for obj in objects:
            snap = rt.copy(obj)
            # Check if we should process this object
            should_process = False
            
            # If Rebuild Poly is enabled, we assume we can convert any geometry
            if cleanup_opts.get("rebuild_poly", False):
                 if rt.superClassOf(snap) == rt.GeometryClass:
                     should_process = True
            else:
                 # Standard check
                 if RizomUVBridgeMaxOps.is_editable_poly(snap) or RizomUVBridgeMaxOps.is_editable_mesh(snap):
                     should_process = True
            
            if should_process:
                RizomUVBridgeMaxOps.cleanup_object(snap, cleanup_opts)
            else:
                rt.delete(snap)
                continue

            
            if fix_missing_channels:
                # Explicitly disable Vertex Color (Channel 0)
                try:
                    if rt.polyop.getMapSupport(snap, 0):
                        rt.polyop.setMapSupport(snap, 0, False)
                except:
                    pass

                # Force map support for all available channels to ensure 
                # FBX export preserves indices (preventing 5 becoming 2 if 2-4 are empty).
                # Start at 1 to SKIP Channel 0 (Vertex Color).
                num_maps = rt.polyop.getNumMaps(snap)
                for i in range(1, num_maps):
                    if not rt.polyop.getMapSupport(snap, i):
                        rt.polyop.setMapSupport(snap, i, True)
                    
                    # Sync Channel Name
                    try:
                        # 3 = "Map Channel" in ChannelInfo enum/ID
                        name = rt.ChannelInfo.GetChannelName(obj, 3, i)
                        if name:
                            rt.ChannelInfo.NameChannel(snap, 3, i, name)
                    except:
                        pass
            
            handle = rt.GetHandleByAnim(obj)
            snap.name = f"{timestamp}__{handle}"
            temp_objs.append(snap)
        return temp_objs

    @staticmethod
    def is_editable_poly(obj):
        return rt.isKindOf(obj.baseObject, rt.Editable_Poly)

    @staticmethod
    def is_editable_mesh(obj):
        return rt.isKindOf(obj.baseObject, rt.Editable_Mesh)

    @staticmethod
    def cleanup_object(obj, opts={}):
         # User provided cleanup:
         # polyop.CollapseDeadStructs o
         # o.deleteIsoVerts()
         # o.DeleteIsoMapVerts()
         # convertToMesh o
         # convertToPoly o

         # Apply selected options (default to False if not passed, or True if we want defaults?)
         # Assuming UI passed values.
         
         if opts.get("collapse_dead_structs", False):
             try:
                 rt.polyop.CollapseDeadStructs(obj)
             except: pass
             
         if opts.get("delete_iso_verts", False):
             try:
                 obj.deleteIsoVerts() # or rt.polyop.deleteIsoVerts(obj)
             except: pass
             
         if opts.get("delete_iso_map_verts", False):
             try:
                 obj.DeleteIsoMapVerts() # or rt.polyop.deleteIsoMapVerts(obj)
             except: pass
         
         if opts.get("rebuild_poly", False):
             try:
                 rt.convertToMesh(obj)
                 rt.convertToPoly(obj)
             except: pass

    @staticmethod
    def transfer_uvs_from_imported(imported_objects):
        modified_nodes = []
        for obj in imported_objects:
            if rt.classOf(obj) == rt.Dummy:
                rt.delete(obj)
                continue
            
            try:
                # USD import might rename "123__456" to "_123__456" or similar
                # Robustly find handle part
                parts = obj.name.split("__")
                if len(parts) < 2:
                    # Fallback: maybe double underscore was lost/converted to single?
                    # Try to parse from end if we assume format timestamp_handle
                    pass 
                
                if len(parts) >= 2:
                    # Handle is in the last part (or second part)
                    # Use parts[-1] to be safe against prefixes
                    handle_part = parts[-1] 
                    
                    # Remove any suffix added by importer (e.g. _Shape, _001) if separator is _
                    # But handle is int.
                    # We expect handle_part to start with the handle number.
                    # Filter digits
                    import re
                    match = re.search(r'^(\d+)', handle_part)
                    if match:
                        handle = int(match.group(1))
                        original_node = rt.GetAnimByHandle(handle)
                    
                        if original_node:
                            rt.convertToPoly(obj)
                            # Get number of map channels
                            # channel 1 is UV
                            # Rizom usually exports to standard channels.
                            count = rt.polyop.getNumMaps(obj) - 1
                            
                            for i in range(1, count + 1):
                                 rt.ChannelInfo.CopyChannel(obj, 3, i)
                                 rt.ChannelInfo.PasteChannel(original_node, 3, i)
                                 
                                 if original_node.modifiers.count > 0:
                                     try:
                                         original_node.modifiers[0].name = f"RizomUV's ch{i}"
                                     except:
                                         pass
                            
                            if original_node not in modified_nodes:
                                modified_nodes.append(original_node)
            except Exception as e:
                print(f"Error transferring UVs for {obj.name}: {e}")
            
            rt.delete(obj)
            
        if modified_nodes:
            rt.select(modified_nodes)


    @staticmethod
    def get_selection():
        """
        Returns (mode, element_ids)
        Mode: 0=Vertex, 1=Edge, 2=Polygon, 3=Island (Island not used yet)
        IDs: List of 0-based indices
        """
        sel = list(rt.selection)
        if not sel or len(sel) > 1:
            return None, [] # Only support single object sync for now
            
        obj = sel[0]
        if not rt.isKindOf(obj, rt.Editable_Poly):
            return None, []
            
        try:
            level = rt.subObjectLevel
        except:
            level = 0
            
        mode = -1
        ids = []
        
        # Helper to convert MAXScript BitArray to Python list
        bg_to_array = rt.execute("fn _ba2arr ba = (ba as array)")
        
        # Helper for Edge -> PolySide conversion
        # Returns flat array [PolyID, SideID, PolyID, SideID...]
        edge_to_polyside = rt.execute("""
        fn _edgeToPolySide obj edgeBits = (
            local result = #()
            local edgeFaces = polyop.getEdgeFaces
            local getFaceEdges = polyop.getFaceEdges
            
            for e in edgeBits do (
                local f = (edgeFaces obj e)[1] -- Get first face
                if f != undefined do (
                    local faceEdges = getFaceEdges obj f
                    local sideIndex = 0
                    for i = 1 to faceEdges.count do (
                        if faceEdges[i] == e do (
                            sideIndex = i - 1 -- 0-based for Rizom
                            exit
                        )
                    )
                    append result (f-1) -- 0-based Face ID
                    append result sideIndex
                )
            )
            result
        )
        """)
        
        # Max Levels: 1:Vert, 2:Edge, 3:Border, 4:Poly, 5:Element
        if level == 1: # Vertex
            mode = 0
            ba = rt.polyop.getVertSelection(obj)
            max_ids = bg_to_array(ba)
            ids = [int(x)-1 for x in list(max_ids)]
            
        elif level == 2 or level == 3: # Edge / Border
            mode = 1
            ba = rt.polyop.getEdgeSelection(obj)
            # Use PolySide conversion for Edges to ensure stability across FBX
            max_ids = edge_to_polyside(obj, ba)
            ids = [int(x) for x in list(max_ids)] # Already 0-based from helper
            
        elif level == 4 or level == 5:
            mode = 2
            ba = rt.polyop.getFaceSelection(obj)
            max_ids = bg_to_array(ba)
            ids = [int(x)-1 for x in list(max_ids)]
            
        return mode, ids

    @staticmethod
    def open_inspector():
        try:
             # Enable, Disable Auto-Repair (to force dialog?), Show Dialog
             rt.execute("MeshInspector.Enable = true")
             # Try disabling auto-repair to ensure dialog appears
             rt.execute("MeshInspector.RepairMesh = false") 
             rt.execute("MeshInspector.ShowDialog = true")
        except Exception as e:
             print(f"Failed to open Mesh Inspector: {e}")

            

