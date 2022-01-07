-- Do not change --
U3dLoad({File={Path="c:/RizomuvBridge_TMP/rizomuv_TMP.fbx", ImportGroups=true, XYZ=true}, NormalizeUVW=true})
U3dSet({Path="Prefs.FileSuffix", Value="_out"})
-- Put your parameters below --
U3dSet({Path="Vars.AutoSelect.SharpEdges.Angle", Value=65})
U3dSelect({PrimType="Edge", Select=true, ResetBefore=true, WorkingSetPrimType="Island", ProtectMapName="Protect", FilterIslandVisible=true, Auto={SharpEdges={AngleMin=65}, PipesCutter=true, HandleCutter=true}})
U3dCut({PrimType="Edge"})
U3dUnfold({PrimType="Edge", MinAngle=1e-005, Mix=1, Iterations=1, PreIterations=5, StopIfOutOFDomain=false, RoomSpace=0.01, PinMapName="Pin", ProcessNonFlats=true, ProcessSelection=true, ProcessAllIfNoneSelected=true, ProcessJustCut=true})
U3dIslandGroups({Mode="SetGroupsProperties", MergingPolicy=8322, GroupPaths={ "RootGroup" }, Properties={Pack={MarginSize=0.006}}})
U3dIslandGroups({Mode="SetGroupsProperties", MergingPolicy=8322, GroupPaths={ "RootGroup" }, Properties={Pack={SpacingSize=0.006}}})
U3dIslandGroups({Mode="DistributeInTilesByBBox", MergingPolicy=8322})
U3dIslandGroups({Mode="DistributeInTilesEvenly", MergingPolicy=8322, UseTileLocks=true, UseIslandLocks=true})
U3dPack({ProcessTileSelection=false, RecursionDepth=1000, RootGroup="RootGroup", Scaling={Mode=3}, Rotate={}, Translate=true, LayoutScalingMode=2})
-- Put this parameter if you want to do something in auto mode --
U3dSave({File={Path="c:/RizomuvBridge_TMP/rizomuv_TMP_out.fbx", UVWProps=true}, __UpdateUIObjFileName=true})


