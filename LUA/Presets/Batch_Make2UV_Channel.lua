
 local file = io.open("C:\\Users\\YOUR_NAME\\AppData\\Local\\Temp\\RizomuvBridge\\batch.txt", "r")
 local arr = {}
 for line in file:lines() do 
 	table.insert(arr, line) 
 	end
ZomSet({Path="Prefs.FileSuffix", Value="_out"})
for i, file in ipairs(arr) do
	--ZomLoad({File={Path=file ..".fbx", ImportGroups=true, XYZ=true, FBX={UseUVSetNames=true}}, NormalizeUVW=true, __Focus=true})
	ZomLoad({File={Path=file ..".fbx", ImportGroups=true, XYZUVW=true, UVWProps=true}})	
	-- Put your parameters below --
	-- Copy UV channel from 1 to 2
	ZomUvset({Mode="Create", Name="ch2"})
	ZomUvset({Mode="SetCurrent", Name="ch2"})
	ZomUvset({Mode="Copy", Name="UVChannel_1"})
	-- 90 pack rotation enable and other setup	
	ZomIslandGroups({Mode="SetGroupsProperties", WorkingSet="Visible", MergingPolicyString="A_ADD|AIB_ADD_A_VALUE_B|B_CLONE", GroupPaths={ "RootGroup" }, Properties={Pack={Rotate={Step=90}}}})
	ZomIslandGroups({Mode="SetGroupsProperties", WorkingSet="Visible", MergingPolicyString="A_ADD|AIB_ADD_A_VALUE_B|B_CLONE", GroupPaths={ "RootGroup" }, Properties={Pack={Rotate={Mode=0}}}})
	ZomIslandGroups({Mode="SetGroupsProperties", WorkingSet="Visible", MergingPolicyString="A_ADD|AIB_ADD_A_VALUE_B|B_CLONE", GroupPaths={ "RootGroup" }, Properties={Pack={MarginSize=0.00585938}}})
	ZomIslandGroups({Mode="SetGroupsProperties", WorkingSet="Visible", MergingPolicyString="A_ADD|AIB_ADD_A_VALUE_B|B_CLONE", GroupPaths={ "RootGroup" }, Properties={Pack={SpacingSize=0.0078125}}})	
	ZomSelect({PrimType="Island", WorkingSet="Visible", Select=true, InvertedNormals=true})
	ZomDeform({WorkingSet="Visible&Selected", PrimType="Island", ApplyOptimizeOnUpdate=true, Optimize={PrimType="Island", Iterations=1, RoomSpace=0.001, PinMapName="Pin"}, Geometrical="AlignHorizontal"})
	ZomSelect({PrimType="IslandGroup", WorkingSet="Visible", DeSelect=true, Names={ "RootGroup", "Tile_0_0" }})
	ZomSelect({PrimType="Island", WorkingSet="Visible", ResetBefore=true, Select=true})
	ZomIslandGroups({Mode="DistributeInTilesEvenly", WorkingSet="Visible", MergingPolicyString="A_ADD|AIB_ADD_A_VALUE_B|B_CLONE", UseTileLocks=true, UseIslandLocks=true})
	ZomPack({RootGroup="RootGroup", WorkingSet="Visible", ProcessTileSelection=false, RecursionDepth=1000, Translate=true, LayoutScalingMode=2, Scaling={Mode=2}})

	--select inverted
	ZomSelect({PrimType="Island", WorkingSet="Visible", Select=true, InvertedNormals=true})

	-- Check for flipped (if some island selected)
	itemNames = ZomItemNames("Lib.Mesh.Islands")
	for i,itemName in pairs(itemNames) do
	    isSelected = ZomGet("Lib.Mesh.Islands." .. itemName .. ".TopoStable.Selected")
	    if isSelected == true then
	    	ZomDeform({WorkingSet="Visible&Selected", PrimType="Island", ApplyOptimizeOnUpdate=true, Optimize={PrimType="Island", Iterations=1, RoomSpace=0.001, PinMapName="Pin"}, Geometrical="FlipHorizontal", CenterMode="MultiCOG"})
	    	ZomSelect({PrimType="Island", WorkingSet="Visible", DeSelect=true, All=true})
			ZomSelect({PrimType="IslandGroup", WorkingSet="Visible", DeSelect=true, All=true})		
			break
	    end    
	end

	--Pack everything
	ZomIslandGroups({Mode="DistributeInTilesEvenly", WorkingSet="Visible", MergingPolicyString="A_ADD|AIB_ADD_A_VALUE_B|B_CLONE", UseTileLocks=true, UseIslandLocks=true})
	ZomPack({RootGroup="RootGroup", WorkingSet="Visible", ProcessTileSelection=false, RecursionDepth=1000, Translate=true, LayoutScalingMode=2, Scaling={Mode=2}})
	
	

	-- Put your parameters above --
	ZomSave({File={Path=file .."_out.fbx", UVWProps=true, FBX={UseUVSetNames=true}}})
	
	if i == #arr then 
		f_done = io.open("C:\\Users\\YOUR_NAME\\AppData\\Local\\Temp\\RizomuvBridge\\rizomuv.txt", "w")
		f_done:write("Exit")
		f_done:close()
		end	
end

