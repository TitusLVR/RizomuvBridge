## Connecting 3ds Max and RizomUV for UVW Channel Exchange

This bridge script connects 3ds Max by Autodesk with RizomUV by RizomLabs, enabling efficient UVW channel exchange between the two tools.

## Installation Instructions:
 - Drag and Drop: Simply drag and drop the MZP file into the 3ds Max viewport.
 - Run Script: Alternatively, go to 3ds Max > Scripting > Run Script, then select the RizomUV Bridge MZP file.
 - After installation, you will see the RizomUV icon appear on the main toolbar of the 3ds Max application.
Note: Administrator rights may be required for installation.

## How It Works:
In 3ds Max:
 - Select an object or multiple objects.
 - Choose the desired editing mode.
 - Press the RizomUV button on the toolbar to send objects to RizomUV.

In RizomUV:
 - Create or edit UVs as needed.
 - Press the Save button.
Once you press Save, RizomUV will close, and the 3ds Max window will reappear. The updated UVs will be applied to your objects as modifiers.


## 3dsmax INFO:
 - Primary Button: Clicking the large RizomUV logo sends the selected objects to RizomUV
 - Objects must be in an editable poly format.
 - If the object has a modifier stack, the script will automatically collapse it to an editable poly. Please proceed cautiously to avoid unintended changes.
 - Right Mouse Button (RMB) on Mode Options (New, Edit, Preset): Opens the current Lua script in Notepad, allowing you to edit and save it or create a new preset.
 - RMB on Preset Dropdown: Reloads or updates the presets list.

## Editing Preset Files:
  In RizomUV, open the Script and Command Log window (default shortcut: L).
  The log will display the commands and parameters for any changes made.
  Copy the relevant lines and paste them into your preset file. Save the file to complete the update.

## Script Requirements:
 - 3ds Max: Compatible with versions 2020, 2021, and 2022.
 - RizomUV: Compatible with versions 2021 and 2022.
 - Note: Older versions of 3ds Max may work but are not officially supported. Use them at your own risk.

## Additional Information:
Current version: 1.5.1
Thank you for using this script! Happy UV-ing!
