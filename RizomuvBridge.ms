/*
Unfold3D bridge by Tit Lavrov  -  Titus.mailbox@gmail.com
Spesial thanks to :
UV Pipe by Robert Fletcher - http://www.scriptspot.com/3ds-max/scripts/3dsmax-uvlayout-uvpipe-mod-by-miauu
Mod by Norman Schaar -- norman.schaar@gmail.com
Mod by Kostadin Kotev -- http://miauumaxscript.blogspot.com/
Because some ideas were taken from it.

CHANGE LOG:
------------------------------------------------------------------------------
20 January 2022 v 1.5
-- Fixed Linked Geo Error

02 January 2022 v 1.4
- Added Batch preset
- small fixes

09 march 2019 v 1.3
- changed to RizomUV

26 October 2017 v.1.26
-Sleep time now 0.1
--Channels cleanup for Mode "New" - cleans from N-ch to 2ch, 1ch will be new in Unfold3d
24 October 2017 v.1.25
-Added Channels cleanup for Mode "New"

23 October 2017 v.1.22:
-Added check of end of file for huge meshes.

21 October 2017 v1.21:
- Some bugs fixed
- Code optimization
- Works with EditPoly modifier 

17 October 2017 v1.15:
-Code optimization
------------------------------------------------------------------------------
12 October 2017 v1.13:
- Some code rework
- Fixed FBX presets 
- FBX presets are moved to PlugCGF folder
- Added presets option and open fn by RMB
------------------------------------------------------------------------------
10 October 2017 v1.12:
- right click on radio-buttons for changing lua scripts 
- added button icon
- changed toolbar icons
- save win position
- check for U3D closing without saving
------------------------------------------------------------------------------
10 October 2017 v1.11:
- Unexpected results with FBX --wier things in 3dsmax with vertex indexes -- added hack like convertToMesh and convertToPoly for selection
------------------------------------------------------------------------------
10 October 2017 v1.1:
Interface changed:
-Removed get button
-Added modes
-Added Lua scripts for launching the Unfold3d
------------------------------------------------------------------------------
05 October 2017 v1.0:
- Hi there it's a release version, and mayby with some bugs :P
------------------------------------------------------------------------------ 
*/
try(destroydialog rizomuvBridge_Rollout)catch()
rollout rizomuvBridge_Rollout "RizomUV Bridge" 
(
	include "$userscripts\\RizomuvBridge\\RizomuvBridge_functions.mse"
	
	button btn_1 "RizomUV" images:#(RUVB_BTN_IMG, RUVB_BTN_IMG_A, 1,1,1,1,1,True)  pos:[5,5] width:60 height:75 tooltip:"Send to RizomUV"
	radiobuttons rbtn_1 "Mode:"	labels:#("New","Edit","Preset","Batch") tooltip:#("Create new UVs but current UVs will be deleted","Edit current UVs","Open object with specific options","Batch, apply selected preset per object in selection") default:1 columns:1 pos: [70,5] 
	dropdownlist ddl1 "" items:RUVB_LUA_PresetFilesDDL selection:RUVB_LUA_DDL_Sel height:5 width:120 tooltip:"RizomUV Presets"  pos:[5,85] enabled:false
	Timer tmr_checkForUvs "wait" pos:[200,200] width:24 height:24 interval:500 active:false
	subrollout prefs "Prefs" height:715 width:125 pos:[2,110]
	
	
	-- Execute INI file 
	--Export Button	
	on btn_1 pressed do 
	(	
		if selection.count != 0 then
		(			
			NonEPolyObjs = SelNonEPoly()
			
			if NonEPolyObjs.count >=1 then 
				(
					messageBox "Selection contains non EditablePoly object(s)!" title:"Non EditablePoly object(s) selected!" beep:off
					select NonEPolyObjs					
				)
				else 
					(
						RUVB_Objs = for o in selection where (classof o.baseObject == Editable_Poly) collect o
			
						if RUVB_Objs.count != 0 then
							(
								if rbtn_1.state == 1 do
								(
									for o in RUVB_Objs do
									(
									oChannels = (polyop.getNumMaps o) - 1
									for i = oChannels to 2 by -1 do channelInfo.ClearChannel o i									 
									convertToPoly o
									)
									RUVB_ObjsCount = RUVB_Objs.count
									ObjectCleanUP RUVB_Objs
									RUVB_ExportObjs RUVB_Objs rbtn_1.state RUVB_Folder RUVB_TempFile ddl1.selection
									tmr_checkForUvs.active = true
								)
								if rbtn_1.state == 2  or rbtn_1.state == 3 do
								(									
									RUVB_ObjsCount = RUVB_Objs.count
									ObjectCleanUP RUVB_Objs
									RUVB_ExportObjs RUVB_Objs  rbtn_1.state RUVB_Folder RUVB_TempFile ddl1.selection
									tmr_checkForUvs.active = true
								)
								
								if rbtn_1.state == 4 do
								(
									RUVB_ObjsCount = RUVB_Objs.count
									ObjectCleanUP RUVB_Objs
									RUVB_ExportObjs RUVB_Objs  rbtn_1.state RUVB_Folder RUVB_TempFile ddl1.selection
									tmr_checkForUvs.active = true									
								)								
							)
					)
		)
		else ( messagebox "Select some Editable Poly objects" title:"Invalid Selection" )	
	)

	on tmr_checkForUvs tick do
	(
		
		if RizomUV() == True then			
		(
			tmr_checkForUvs.active = false			
			messageBox "RizomUV process deosn't exists." title:"Warning" beep:off
		)		
		else 
			( 	
				if RUVB_Objs.count == RUVB_ObjsCount then
				(
					if rbtn_1.state != 4 then
						(			
							if doesFileExist (RUVB_Folder + RUVB_TempFile_out +".fbx") do						
							(						  
								FileExistCheckCountA = getFileSize (RUVB_Folder + RUVB_TempFile_out +".fbx")
								sleep 0.1																			
								if FileExistCheckCountA == getFileSize (RUVB_Folder + RUVB_TempFile_out +".fbx") then
										(
											tmr_checkForUvs.active = false
											RizomUVKill()
											RUVB_GetResult RUVB_Folder RUVB_TempFile_out							
											select RUVB_Objs					
											max modify mode
											max views redraw
											max tool zoomextents all						
											deleteFile (RUVB_Folder + RUVB_TempFile_out +".fbx")		
										)
										else 
											(
											 tmr_checkForUvs.ticks += 1	
											)							
							)
						)
					
					else
						(							
							if doesFileExist (RUVB_Folder + "rizomuv.txt" ) then
								(	
									tmr_checkForUvs.active = false
									RizomUVKill()
									
									if RUVB_BatchObjs.count != 0 do
										(
											for f in RUVB_BatchObjs do										
												(										
													if doesFileExist (RUVB_Folder+ f + ".fbx") do										
													(	
														RUVB_GetResult RUVB_Folder f 
														deleteFile (RUVB_Folder + f + ".fbx")
													)											
												)	
									
											select RUVB_Objs	
											max modify mode
											max views redraw
											max tool zoomextents all	
											deleteFile (RUVB_Folder + "rizomuv.txt")								
										)
								)
								else
									(
										tmr_checkForUvs.ticks += 1
									)
						)
					)
					else 
						(
							local theQuestion = querybox "You have deleted the object or objects you were editing in RizomUV. Do you want to close RizomUV?"
							if theQuestion == true do
							(
								tmr_checkForUvs.active = false
								RizomUVKill()							
								if doesFileExist (RUVB_Folder + RUVB_TempFile_out +".fbx") do
									(
										deleteFile (RUVB_Folder + RUVB_TempFile_out +".fbx")	
									)
							)
						)
			)
	)

	on rbtn_1 rightClick do 
	(	
		case rbtn_1.state of 
		(
			1: (
				shelllaunch "notepad.exe"  RUVB_LUA_newUV							
				)							
			2: (
				shelllaunch "notepad.exe" RUVB_LUA_EditUV							
				)							
			3: (
					if RUVB_LUA_PresetFiles.count ==0 then 
					(
						messageBox "There are no preset files, folder is empty!" title:"Presets folder is empty!" beep:off	
					)
					else
						(
							shelllaunch "notepad.exe" RUVB_LUA_PresetFiles[ddl1.selection]
						)								
				)
			4: (
					if RUVB_LUA_PresetFiles.count ==0 then 
					(
						messageBox "There are no preset files, folder is empty!" title:"Presets folder is empty!" beep:off	
					)
					else
						(
							shelllaunch "notepad.exe" RUVB_LUA_PresetFiles[ddl1.selection]
						)								
				)
		)	
	)

	on rbtn_1 changed state do 
	(	
		if rbtn_1.state >= 3 then (ddl1.enabled=true)	else (ddl1.enabled=false)						
	)

	on ddl1 rightClick do 
	(
		RUVB_LUA_PresetFiles = getFiles ((getdir #userscripts) + "\\RizomuvBridge\\Lua\\Presets\\*.lua")
		RUVB_LUA_PresetFilesDDL = for i in RUVB_LUA_PresetFiles collect (getFilenameFile i)
		ddl1.items = RUVB_LUA_PresetFilesDDL	
	)

	on ddl1 selected item do
	(
		NewDdl_sel = ddl1.selection
		setINISetting ("$userscripts\\RizomuvBridge\\RizomuvBridge_settings.ini") "Preset" "Selection" (( NewDdl_sel ) as string)
	)	

	on rizomuvBridge_Rollout close do 
	(	
		NewWinPos = getDialogpos rizomuvBridge_Rollout
		NewDdl_sel = ddl1.selection
		setINISetting ("$userscripts\\RizomuvBridge\\RizomuvBridge_settings.ini") "Position" "PosX" ( (NewWinPos[1]  as integer ) as string)
		setINISetting ("$userscripts\\RizomuvBridge\\RizomuvBridge_settings.ini") "Position" "PosY" ( (NewWinPos[2]  as integer ) as string)
		tmr_checkForUvs.active = false
	)
	
	rollout rizomuvBridge_prefs_Rollout "Preferences" rolledUp: True
	(	
		groupBox grp_export "Export:" pos:[2,2] width:110 height:120 align:#left
		label lbl_fbx_version "FBX Version:" pos:[8,20]
		dropdownlist dd_e_fbx_ver "" pos:[7,35] items:#("FBX201200", "FBX201300", "FBX201400", "FBX201600", "FBX201800", "FBX201900", "FBX202000", "FBX202100") selection:(getINISetting ("$userscripts\\BMAX\\bmax.ini") "Export" "FBX_Version" as integer) width:100 height:16 tooltip:"Select FBX format version. Blender is using FBX Version 7.1 or newer.(FBX 2014)"
		label lbl_temp_folder "Temp Folder Path:" pos:[8,70]
		edittext temp_folder_path ""  pos:[2,85] width:105 enabled:true labelOnTop:false text:((getINISetting("$userscripts\\RizomuvBridge\\RizomuvBridge_settings.ini") "ExchangeFolder" "Folder") as string) bold:false readOnly:true
		button btn_new_temp_folder "Set New Path"  pos:[18,105] width:80 height:18 align:#left tooltip:"Set the new temp folder"
		
		on rizomuvBridge_prefs_Rollout rolledUp state do
		(
			if state then 
				(			
					rizomuvBridge_Rollout.height = 265
				)
				else
					(
						rizomuvBridge_Rollout.height = 135
					)
		)
		on dd_e_fbx_ver selected val do
		(
			setINISetting ("$userscripts\\RizomuvBridge\\RizomuvBridge_settings.ini") "FileFormat" "FBX_Version" ((dd_e_fbx_ver.selection) as string)
			setINISetting ("$userscripts\\RizomuvBridge\\RizomuvBridge_settings.ini") "FileFormat" "FBX_Version_sys" ((dd_e_fbx_ver.items[val]) as string)
		)
		
		on btn_new_temp_folder pressed do
		(
			temp_folder = getINISetting RUVB_INI "ExchangeFolder" "Folder"
			newFolder = getSavePath caption:"Custom RizomUV Bridge exchange folder" initialDir:temp_folder
			if newFolder != undefined then
				(
					setINISetting RUVB_INI "ExchangeFolder" "Folder" (newFolder + "\\")
					generate_LUA_file_new (newFolder + "\\" + RUVB_TempFile + ".fbx")
					generate_LUA_file_edit (newFolder + "\\" + RUVB_TempFile + ".fbx")
					messageBox "New and Edit LUA files were regenerated" title:"Warning" beep:off
				)
				else 
				(
					default_folder = (sysInfo.tempdir) + "RizomuvBridge\\"
					setINISetting RUVB_INI "ExchangeFolder" "Folder" default_folder
					generate_LUA_file_new ( default_folder + RUVB_TempFile + ".fbx")
					generate_LUA_file_edit (default_folder + RUVB_TempFile + ".fbx")
					messageBox "New and Edit LUA files were regenerated" title:"Warning" beep:off
					messageBox "Default path restored" title:"Warning" beep:off
				)
			
			temp_folder_path.text = getINISetting RUVB_INI "ExchangeFolder" "Folder"	
		)
		
	)
	
	on rizomuvBridge_Rollout open do 
	(
		RUVB_posX =  getINISetting("$userscripts\\RizomuvBridge\\RizomuvBridge_settings.ini") "Position" "PosX" as float 	
		RUVB_posY =  getINISetting("$userscripts\\RizomuvBridge\\RizomuvBridge_settings.ini") "Position" "PosY" as float	
		RUVB_Init()
		addSubRollout prefs rizomuvBridge_prefs_Rollout	
	)
)
createDialog rizomuvBridge_Rollout 130 135 style:#(#style_titlebar, #style_sysmenu, #style_toolwindow) 