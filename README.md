# Connecting 3ds Max and RizomUV for UVW Channel Exchange

This bridge script connects **3ds Max** (Autodesk) with **RizomUV** (RizomLabs), enabling efficient UVW channel exchange between the two tools.

## Installation Instructions

1.  **Drag and Drop**: Simply drag and drop the `install.ms` or MZP file into the 3ds Max viewport.
2.  **Run Script**: Alternatively, go to **Scripting > Run Script**, then select the RizomUV Bridge installer.
3.  **Toolbar**: After installation, you will see the RizomUV icon on the main toolbar or find the macro in **Customize User Interface** under the `TitusLVR` category.

## How It Works

### Sending to RizomUV
1.  **Select** one or more **Editable Poly** objects in 3ds Max.
2.  Click **"Send"** (or "Start RizomUV" if not open).
3.  The objects are exported and loaded into RizomUV automatically.

### Editing in RizomUV
-   Use RizomUV to Unfold, Pack, and Optimize your UVs.
-   You can also use the **Bridge Tools** directly from 3ds Max (Cut, Unfold, Pack, Weld) to control RizomUV remotely.

### getting Results
1.  **Save** your work in RizomUV (standard Save `Ctrl+S`).
2.  Click **"Get"** in the Bridge UI to import the updated UVs back to 3ds Max.

## UI Overview

### Actions
-   **Send**: Exports selected objects to RizomUV.
-   **Get**: Imports the current mesh from RizomUV back to 3ds Max.
-   **Sync Sel**: Syncs the selection mode (Edge/Poly/Vertex) from 3ds Max to RizomUV.

### Tools
-   **Weld / Weld Selected**: Weld vertices.
-   **Cut / Unfold / Optimize / Pack**: Standard RizomUV operations accessible directly from 3ds Max.

### Scripts
-   Run custom Lua scripts located in the configured scripts folder.

### Preferences (Collapsible)
-   **File Format**: Choose between **FBX** (default) and **USD**.
-   **Export Cleanup Options**:
    -   *Collapse Dead Structs*: Clean up dead structures.
    -   *Delete Iso Verts*: Remove isolated vertices.
    -   *Rebuild Poly*: Convert to Editable Poly on export.
-   **Mesh Inspector**: Check mesh integrity.
-   **Help**: Link to documentation.

## Requirements
-   **3ds Max**: 2020, 2021, 2022+
-   **RizomUV**: 2022.1+ (VSRS)

## Additional Information
Current version: 1.5.2
Happy UV-ing!
