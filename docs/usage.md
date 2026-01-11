# User Guide

This guide explains the interface and workflows of the RizomUV Bridge.

## Interface Overview

The RizomUV Bridge window is divided into several logical sections:

1.  **Actions**: The main controls for transferring data (Send, Get, Sync).
2.  **RizomUV Tools**: Access to common RizomUV algorithms (Cut, Pack, etc.).
3.  **Scripts**: Execute custom Lua scripts.
4.  **Connection**: Manage the link to RizomUV application (Start/Close).
5.  **Preferences**: Collapsible section for configuration.

---

## Workflow: Send & Get

### Sending Objects
1.  **Selection**: Select one or more **Editable Poly** objects in 3ds Max.
    *   *Tip: The bridge works best with Editable Poly objects.*
2.  **Click "Send"**: This exports the geometry to a temporary file and commands RizomUV to load it.
3.  **RizomUV Opens**: The application will launch (if not running) and load your mesh.

### Getting Results
Usually, the bridge automates the return process. However, you can manually trigger it:
1.  **Save in RizomUV**: Press `Ctrl+S` in RizomUV to save the temp file.
2.  **Click "Get"**: Checks for the output file from RizomUV and imports the updated UVs onto your original mesh.

---

## RizomUV Tools

The bridge exposes direct buttons for common RizomUV commands so you don't always have to switch windows:

*   **Weld All / Weld Selected**: Welds UV vertices.
*   **Cut**: Performs a cut operation based on current selection/seams.
*   **Unfold**: Runs the Unfold algorithm.
*   **Optimize**: Optimizes the UV distortion.
*   **Pack**: Packs the UV islands into the UV tile.

## Running Scripts

You can execute custom Lua scripts on your mesh within RizomUV:

1.  **Select Script**: Choose a script from the dropdown menu.
2.  **Folder**: Click `...` to change the folder where your scripts are stored.
3.  **Run Script**: Executes the selected script immediately in RizomUV.

---

## Preferences

This section is collapsible to save space. Click "Preferences" to expand.

### File Format
You can choose the intermediate format used for data exchange:
*   **FBX** (Default): Robust and widely supported.
*   **USD**: Uses Universal Scene Description for exchange.

### Export Cleanup Options
Configure how meshes are processed before sending to RizomUV:

*   **Collapse Dead Structs**: Removes unused data structures.
*   **Delete Iso Verts**: Deletes isolated vertices.
*   **Delete Iso Map Verts**: Deletes isolated map vertices.
*   **Rebuild Poly**: Rebuilds the Editable Poly object to ensure data integrity.

### Other
*   **Mesh Inspector**: Launches the Mesh Inspector tool to verify geometry.
*   **Help**: Opens the online documentation.

---

## Troubleshooting

### Connection Issues
If the bridge cannot find `rizomuv.exe`:

1.  Ensure RizomUV is installed.
2.  The bridge will prompt you to locate the `.exe` file manually if auto-detection fails.
