ZomLoad({File={Path="C:\\Users\\UserName\\AppData\\Local\\Temp\\RizomuvBridge\\rizomuv_TMP.fbx", ImportGroups=true, XYZ=true}, NormalizeUVW=true})
-- Do not change --
ZomSet({Path="Prefs.FileSuffix", Value="_out"})
-- Put your parameters below --
ZomSet({Path="Vars.Viewport.ColorMapIDDisplayMode", Value=1})
ZomSet({Path="Prefs.UI.DisplayPx", Value=true})
ZomIslandGroups({Mode="SetGroupsProperties", WorkingSet="Visible", GroupPaths={ "RootGroup" }, Properties={Pack={Scaling={Min=0}}}})
ZomIslandGroups({Mode="SetGroupsProperties", WorkingSet="Visible", GroupPaths={ "RootGroup" }, Properties={Pack={Resolution=512}}})
ZomSelect({PrimType="Edge", WorkingSet="Visible&UnLocked", IslandGroupMode="Group", Select=true, ResetBefore=true, ProtectMapName="Protect", FilterIslandVisible=true, Auto={SharpEdges={AngleMin=39}, PipesCutter=false, HandleCutter=true, QuadLoopCutter=true, StretchLimiter=true, Quality=0.25, StoreCoordsUVW=true, FlatteningMode=0, FlatteningUnfoldParams={StopIfZeroMix=true, BorderIntersections=true, TriangleFlips=true}}})
ZomCut({PrimType="Edge", WorkingSet="Visible&UnLocked"})
ZomLoad({DefaultUnit="m", Data={CoordsUVWInternalPath="#Mesh.Tmp.AutoSelect.UVW "}})
ZomOptimize({PrimType="Edge", WorkingSet="Visible&Flat&UnLocked", Mix=1, AngleDistanceMix=1, RoomSpace=0.001, MinAngle=1e-05, BorderIntersections=true, TriangleFlips=true, KeepMetric=true, PinMapName="Pin"})
ZomIslandGroups({Mode="DistributeTilesContent", WorkingSet="Visible&UnLocked", FreezeIslands=true, UseTileLocks=true, UseIslandLocks=true, GroupPaths={ "RootGroup" }})
ZomPack({RootGroup="RootGroup", WorkingSet="Visible", ProcessTileSelection=false, RecursionDepth=1000, Translate=true, AuxGroup="RootGroup", LayoutScalingMode=0, Scaling={Mix=true, Mode=0}})
-- Put this parameter if you want to do something in auto mode --
ZomSave({File={Path="C:/Users/UserName/AppData/Local/Temp/RizomuvBridge/rizomuv_TMP_out.fbx", UVWProps=true}