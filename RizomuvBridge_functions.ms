local RUVB_EXE
local RUVB_Objs
local RUVB_ObjsCount
local RUVB_BatchObjs = #()
local RUVB_posX =  getINISetting  ("$userscripts\\RizomuvBridge\\RizomuvBridge_settings.ini") "Position" "PosX" as float 	
local RUVB_posY =  getINISetting  ("$userscripts\\RizomuvBridge\\RizomuvBridge_settings.ini") "Position" "PosY" as float		
local RUVB_INI = ("$userscripts\\RizomuvBridge\\RizomuvBridge_settings.ini")
local RUVB_Folder = (getINISetting RUVB_INI "ExchangeFolder" "Folder")	
local RUVB_TempFile = (getINISetting RUVB_INI "ExchangeFolder" "TempFile")
local RUVB_TempFile_out = (getINISetting RUVB_INI "ExchangeFolder" "TempFile_out")
local RUVB_LUA_newUV = ((getdir #userscripts) + "\\RizomuvBridge\\Lua\\" + (getINISetting RUVB_INI "Lua" "Open"))
local RUVB_LUA_EditUV = ((getdir #userscripts) + "\\RizomuvBridge\\Lua\\" + (getINISetting RUVB_INI "Lua" "OpenUV"))	
local RUVB_LUA_PresetFiles = getFiles ((getdir #userscripts) + "\\RizomuvBridge\\Lua\\Presets\\*.lua")
local RUVB_LUA_PresetFilesDDL = for i in RUVB_LUA_PresetFiles collect (getFilenameFile i)
local RUVB_LUA_DDL_Sel =  ((getINISetting RUVB_INI "Preset" "selection") as integer) 
local RUVB_BTN_IMG = ((getdir #userscripts) + "\\RizomuvBridge\\IMG\\" + (getINISetting RUVB_INI "Button" "Image"))   
local RUVB_BTN_IMG_A = ((getdir #userscripts) + "\\RizomuvBridge\\IMG\\" + (getINISetting RUVB_INI "Button" "Image_a"))

fn RizomUV =		
	(
	local RUVB_EXENAME = (getINISetting RUVB_INI "ProccessName" "exeName") as string
	local rizomuv = (dotnetclass "System.Diagnostics.Process").GetProcessesByName RUVB_EXENAME
	if rizomuv.count == 0 then true else false
	)
	
fn RizomUVKill = 
	(
		local RUVB_EXENAME = (getINISetting RUVB_INI "ProccessName" "exeName") as string
		local rizomuv = (dotnetclass "System.Diagnostics.Process").GetProcessesByName RUVB_EXENAME		
		if rizomuv.count != 0 do (rizomuv[1].kill())		
	)	
	
fn RUVB_Export_FBX Folder FileName =
	(
		file = Folder + FileName + ".fbx"
		MaxVer = maxVersion()
		pluginManager.loadClass FBXEXP		
		--commented out settings left as defualt, here for future revision purposes, but most likely not needed
		FBXExporterSetParam "Animation" false 
		FBXExporterSetParam "ASCII" True
		FBXExporterSetParam "AxisConversionMethod" "Animation"
		FBXExporterSetParam "BakeAnimation" False 
		-- FBXExporterSetParam "BakeFrameStart" --derived from length of playback range
		-- FBXExporterSetParam "BakeFrameEnd"
		-- FBXExporterSetParam "BakeFrameStep"
		-- FBXExporterSetParam "BakeResampleAnimation"
		FBXExporterSetParam "Cameras" false
		-- FBXExporterSetParam "CAT2HIK"
		FBXExporterSetParam "ColladaTriangulate" false
		-- FBXExporterSetParam "ColladaSingleMatrix"
		-- FBXExporterSetParam "ColladaFrameRate" 
		FBXExporterSetParam "Convert2Tiff" false
		--FBXExporterSetParam "ConvertUnit" "cm" --should be Auto if SYSTEM UNITS are correct
		FBXExporterSetParam "EmbedTextures"false
		FBXExporterSetParam "FilterKeyReducer" false --OPTIMIZE PASS : curve filter stuff
		FBXExporterSetParam "GeomAsBone" false --only real bones should be exporting
		FBXExporterSetParam "GenerateLog" false
		FBXExporterSetParam "Lights" false
		--FBXExporterSetParam "LoadExportPresetFile"--this very code block negates a need for a preset
		FBXExporterSetParam "NormalsPerPoly" false--MoBu setting
		FBXExporterSetParam "PointCache" false--VERTEX ANIMATION		
		--FBXExporterSetParam "PopSettings"--for 'one click' operations
		FBXExporterSetParam "Preserveinstances" false--OPTIMIZE PASS if instances used
		--FBXExporterSetParam "PushSettings--for 'one click' operations
		FBXExporterSetParam "Removesinglekeys"false--OPTIMIZE PASS if motionless scenes
		--FBXExporterSetParam "Resampling"--for anim curves
		--FBXExporterSetParam "ResetExport"-reverts Loads the Autodesk Media & Entertainment export preset.
		--FBXExporterSetParam "ScaleFactor" 1.0 --should be Auto if SYSTEM UNITS are correct
		--FBXExporterSetParam "SelectionSet"--VERTEX ANIMATION
		--FBXExporterSetParam "SelectionSetExport"--VERTEX ANIMATION 
		FBXExporterSetParam "Shape" false-- per conv w MG
		FBXExporterSetParam "Skin" false --skined bones is what we're all about
		FBXExporterSetParam "ShowWarnings" false 
		FBXExporterSetParam "SmoothingGroups" true --asked kelsey
		FBXExporterSetParam "SmoothMeshExport" true -- for turbosmooth
		--FBXExporterSetParam "SplitAnimationIntoTakes"-- one anim per file
		FBXExporterSetParam "TangentSpaceExport" false
		FBXExporterSetParam "Triangulate" false
		FBXExporterSetParam "UpAxis" "Y"
		FBXExporterSetParam "UseSceneName" false
		FBXExporterSetParam "PreserveEdgeOrientation" false
			
		FBXExporterSetParam "FileVersion" (getINISetting RUVB_INI "FileFormat" "FBX_Version_sys")
		exportFile file #noPrompt selectedOnly:true usage:FBXEXP
	)
	
fn ObjectCleanUP Objs =
	(
		for o in Objs do
		(
			polyop.CollapseDeadStructs o
			o.deleteIsoVerts()	
			o.DeleteIsoMapVerts()
			convertToMesh o
			convertToPoly o
		)
	)	
	
fn RUVB_ExportObjs Objs RUVB_Mode RUVB_Folder FileName PresetNo = 
	(		
		local ObjsToExport = #()
		for Obj in Objs do
		(
			local meshSnapshot = copy Obj
			convertToPoly meshSnapshot			
			meshSnapshot.name = (timestamp() as string) + "__" + (GetHandleByAnim Obj) as string
			append ObjsToExport meshSnapshot
		)
		--Launch Unfold3D			
		case RUVB_Mode of 
			(
				1: (
						--Export the Obj
						select ObjsToExport		
						RUVB_Export_FBX RUVB_Folder FileName 	
						--Delete Temp meshes
						for o in ObjsToExport do delete o
							
						shelllaunch RUVB_EXE ("-cfi " + "\""+ RUVB_LUA_newUV)						
					)
				2: (	
						--Export the Obj
						select ObjsToExport		
						RUVB_Export_FBX RUVB_Folder FileName 	
						--Delete Temp meshes
						for o in ObjsToExport do delete o
						
						shelllaunch RUVB_EXE ("-cfi " + "\""+ RUVB_LUA_EditUV)					
					)
				3: (
						if RUVB_LUA_PresetFiles.count ==0 then 
						(
							messageBox "There are no preset files, folder is empty!" title:"Warning" beep:off	
						)
						else
							(
								--Export the Obj
								select ObjsToExport		
								RUVB_Export_FBX RUVB_Folder FileName 	
								--Delete Temp meshes
								for o in ObjsToExport do delete o
								shelllaunch RUVB_EXE ("-cfi " + "\""+ RUVB_LUA_PresetFiles[PresetNo])
							)								
					)				
				4: (
					if RUVB_LUA_PresetFiles.count ==0 then 
					(
						messageBox "There are no preset files, folder is empty!" title:"Warning" beep:off	
					)
					else
						(	
							max select none
							fileName = RUVB_Folder + "batch.txt"
							file = createfile fileName writeBOM:False
							if file != undefined then
							(
								for i=1  to  ObjsToExport.count do (format "%\n" (RUVB_Folder + RUVB_TempFile + "__" + (i as string)) to:file)
								close file
								free file									
							)
							
							for i=1 to ObjsToExport.count do
								(
									select ObjsToExport[i]																						
									_file = RUVB_TempFile + "__" + (i as string)
									RUVB_Export_FBX RUVB_Folder _file 
									append RUVB_BatchObjs (_file + "_out")
								)
							for o in ObjsToExport do delete o
							 	
							shelllaunch RUVB_EXE ("-cfi " + "\""+ RUVB_LUA_PresetFiles[PresetNo])							
						)								
				)
			)	
	)
	
fn RUVB_Import_FBX RUVB_Folder FileName=
	(
		file = RUVB_Folder + FileName + ".fbx"
		pluginManager.loadClass FBXIMP	
		--commented out settings left as defualt, here for future revision purposes, but most likely not needed
		FBXImporterSetParam "Mode" #create
		--Animation
		FBXImporterSetParam "Animation" false
		FBXImporterSetParam "Skin" false
		--Geometry
		FBXImporterSetParam "Shape" false
		FBXImporterSetParam "SmoothingGroups" true
		--Cameras
		FBXImporterSetParam "Cameras" false	
		--Lights
		FBXImporterSetParam "Lights" false
		--Units_Axis
		FBXImporterSetParam "UpAxis" "Y"
		FBXImporterSetParam "ScaleConversion" false
		FBXImporterSetParam "ScaleFactor" 1.0
		--LOG
		FBXImporterSetParam "GenerateLog" false

		importFile file #noprompt usage:FBXIMP
	)	
		
fn RUVB_GetResult RUVB_Folder FileName= 
	(		
		with redraw off
		(
			--get the current objects
			oldObjs = objects as array
			--import the unwraped objects
			RUVB_Import_FBX RUVB_Folder FileName
			--get imported objects			
			newObjs = for o in objects where ((findItem oldObjs o) == 0) collect o
			
			for o in newObjs do
			(
				parentNodeHandle = (execute (filterString o.name "__")[2])
				--get the parent node
				parentNode = undefined
				for obj in objects where (GetHandleByAnim obj) == (parentNodeHandle) do
				parentNode = obj
					
				if parentNode != undefined do
				(
					convertToPoly o					
					chCount = (polyop.getNumMaps o) - 1									
					for i=1 to chCount do 
					(
						ChannelInfo.CopyChannel o 3 i
						ChannelInfo.PasteChannel parentNode 3 i	
						parentNode.modifiers[1].name = "RizomUV's" + " ch" + (i as string)						
					)
					delete o
				)					
			)
		)		
	)

fn SelNonEPoly = 
	(	
	for o in selection where isKindOf o.baseObject editable_poly == false collect o	
	)	

fn generate_LUA_file_new filepath =
	(
		rizom_filepath = substituteString filepath "\\" "\\\\"
		New_LUA_file = createfile RUVB_LUA_newUV writeBOM:False
		format "-- Do not change --\n" to:New_LUA_file
		format "ZomLoad({File={Path=\"%\", ImportGroups=true, XYZ=true}, NormalizeUVW=true})\n" rizom_filepath to:New_LUA_file
		format "ZomSet({Path=\"Prefs.FileSuffix\", Value=\"_out\"})\n" to:New_LUA_file
		format "-- Put your parameters below --\n" to:New_LUA_file
		flush New_LUA_file	--clear the file from memory
		close New_LUA_file	--close the file stream
	)
	
fn generate_LUA_file_edit filepath =
	(
		rizom_filepath = substituteString filepath "\\" "\\\\"
		Edit_LUA_file = createfile RUVB_LUA_EditUV writeBOM:False
		format "-- Do not change --\n" to:Edit_LUA_file
		format "ZomLoad({File={Path=\"%\", ImportGroups=true, XYZUVW=true, UVWProps=true}})\n" rizom_filepath to:Edit_LUA_file
		format "ZomSet({Path=\"Prefs.FileSuffix\", Value=\"_out\"})\n" to:Edit_LUA_file
		format "-- Put your parameters below --\n" to:Edit_LUA_file
		flush Edit_LUA_file	--clear the file from memory
		close Edit_LUA_file	--close the file stream
	)

fn RUVB_Init = 
	(
		local RUVB_INI = "$userscripts\\RizomuvBridge\\RizomuvBridge_settings.ini"
		if doesFileExist RUVB_INI do
		(
			RUVB_EXE = getINISetting RUVB_INI "Path" "rizomuv"
			RUVB_Folder = getINISetting RUVB_INI "ExchangeFolder" "Folder"
			format "RizomUVBridge_1.4: INI file - Tweak it here: %\n" ((getdir #userscripts) + "\\RizomuvBridge\\RizomuvBridge_settings.ini")
		)
		
		if doesFileExist (RUVB_Folder + RUVB_TempFile_out +".fbx") do
		(
			deleteFile (RUVB_Folder + RUVB_TempFile_out +".fbx")	
		)
		
		-- Setup temp folder
		if RUVB_Folder == "" OR RUVB_Folder == undefined do
		(
			RUVB_Folder = false
		)
		
		if RUVB_Folder == false then
		(

			local temp_folder = (sysInfo.tempdir) + "RizomuvBridge\\"			
			makeDir temp_folder
			
			if doesFileExist(temp_folder) then
			(
				RUVB_Folder = temp_folder
				setINISetting RUVB_INI "ExchangeFolder" "Folder" RUVB_Folder
				format "RizomUVBridge_1.4: Temp Folder Path: %\n" (RUVB_Folder)
			)
			else
			(
				messagebox "RizomUV Bridge needs exchange folder. RizomUV Bridge will now close."
				destroyDialog rizomuvBridge_Rollout
			)
		)
		
		-- Setup LUA initial files			
		max_filepath = RUVB_Folder + RUVB_TempFile + ".fbx"
		

		if doesFileExist (RUVB_LUA_newUV) == false then
			(
				generate_LUA_file_new max_filepath
				format "RizomUVBridge_1.4: LUA New File Created: %\n" (RUVB_LUA_newUV)
			)
		
		if doesFileExist (RUVB_LUA_EditUV) == false then
			(
				generate_LUA_file_edit max_filepath				
				format "RizomUVBridge_1.4: LUA Edit File Created: %\n" (RUVB_LUA_EditUV)
			)

		-- Setup EXE
		if RUVB_EXE == "" OR RUVB_EXE == undefined do
		(
			RUVB_EXE = false
		)
		
		if RUVB_EXE == false then
		(
			local pickResult = getOpenFileName caption:"Select RizomUV Executable file" filename:"rizomuv.exe" types:"Executable(*.exe)|*.exe"
			makeDir "$userscripts\\RizomuvBridge\\"
			if pickResult != undefined then
			(
				RUVB_EXE = pickResult
			)
			else
			(
				messagebox "RizomUV Bridge needs rizomuv.exe to work. RizomUV Bridge will now close."
				destroyDialog rizomuvBridge_Rollout
			)
		)
		if RUVB_EXE != false do
		(
			setINISetting RUVB_INI "Path" "rizomuv" RUVB_EXE
			format "RizomUVBridge_1.4: Rizomuv File: %\n" (RUVB_EXE)
		)		
		
		setDialogPos rizomuvBridge_Rollout [(RUVB_posX),(RUVB_posY)]	
		format "RizomUVBridge_1.4: Loaded :) \n"
	)