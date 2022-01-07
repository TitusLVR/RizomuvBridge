--Do not change
U3dLoad({File={Path="c:/RizomuvBridge_TMP/rizomuv_TMP.fbx", ImportGroups=true, XYZ=true}, NormalizeUVW=true})
U3dSet({Path="Prefs.FileSuffix", Value="_out"})
-- Put your parameters below --
U3dSymmetrySet({Point={0, 0, 0}, Normal={1, 0, 0}, Threshold=0.01, Enabled=true, UPos=0.5, LocalMode=false})
U3dSelect({PrimType="Edge", Select=true, ResetBefore=true, WorkingSetPrimType="Island", ProtectMapName="Protect", FilterIslandVisible=true, Auto={Skeleton={}, Open=true, PipesCutter=true, HandleCutter=true}})
U3dCut({PrimType="Edge"})
U3dUnfold({PrimType="Edge", MinAngle=1e-005, Mix=1, Iterations=1, PreIterations=5, StopIfOutOFDomain=false, RoomSpace=0, PinMapName="Pin", ProcessNonFlats=true, ProcessSelection=true, ProcessAllIfNoneSelected=true, ProcessJustCut=true, BorderIntersections=true, TriangleFlips=true})
U3dIslandGroups({Mode="DistributeInTilesEvenly", MergingPolicy=8322, GroupPath="RootGroup"})
U3dPack({ProcessTileSelection=false, RecursionDepth=1, RootGroup="RootGroup", Scaling={}, Rotate={}, Translate=true, LayoutScalingMode=2})
