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
    def prepare_temp_objects(objects):
        temp_objs = []
        timestamp = str(int(time.time()))
        for obj in objects:
            snap = rt.copy(obj)
            rt.convertToPoly(snap)
            handle = rt.GetHandleByAnim(obj)
            snap.name = f"{timestamp}__{handle}"
            temp_objs.append(snap)
        return temp_objs

    @staticmethod
    def cleanup_object(obj):
        # We intentionally skip destructive cleanup (convertToMesh/Poly)
        # to preserve vertex/edge/face IDs for synchronization.
        pass

    @staticmethod
    def transfer_uvs_from_imported(imported_objects):
        for obj in imported_objects:
            if rt.classOf(obj) == rt.Dummy:
                rt.delete(obj)
                continue
            
            try:
                parts = obj.name.split("__")
                if len(parts) >= 2:
                    handle_str = parts[1].split("_")[0] 
                    handle = int(handle_str)
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
            except Exception as e:
                print(f"Error transferring UVs for {obj.name}: {e}")
            
            rt.delete(obj)

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
            

