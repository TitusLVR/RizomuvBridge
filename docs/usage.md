# User Guide

This guide explains the interface and workflows of the RizomUV Bridge.

## Interface Overview

The RizomUV Bridge window is divided into several logical sections:

1.  **Actions**: The main controls for transferring data.
2.  **RizomUV Tools**: Access to common RizomUV algorithms.
3.  **Scripts**: Execute custom Lua scripts.
4.  **File Format**: Configure data exchange settings.
5.  **Connection**: Manage the link to RizomUV application.

---

## Workflow: Send & Get

### Sending Objects
1.  **Selection**: Select one or more **Editable Poly** objects in 3ds Max.
    *   *Tip: If your object is not an Editable Poly, the bridge will ask to convert it.*
2.  **Click "Send"**: This exports the geometry to a temporary file and commands RizomUV to load it.
3.  **RizomUV Opens**: The application will launch (if not running) and load your mesh.

### Getting Results
Usually, the bridge automates the return process. However, you can manually trigger it:
1.  **Click "Get"**: Checks for the output file from RizomUV and imports the updated UVs onto your original mesh.

---

## RizomUV Tools

The bridge exposes direct buttons for common RizomUV commands so you don't always have to switch windows:

*   **Weld All**: Welds all UV vertices.
*   **Weld Selected**: Welds only currently selected UV components.
*   **Cut**: Performs a cut operation based on current selection/seams.
*   **Unfold**: Runs the Unfold algorithm.
*   **Optimize**: Optimizes the UV distortion.
*   **Pack**: Packs the UV islands into the UV tile.

---

## File Formats

You can choose the intermediate format used for data exchange:

*   **FBX** (Default): Robust and widely supported.
    *   *FBX Version*: Choose between 2012 and 2020 versions if needed for compatibility.
*   **USD**: Uses Universal Scene Description for exchange.
    *   *Note*: When using USD, certain options like "FBX Version" are hidden.

---

## Running Scripts

You can execute custom Lua scripts on your mesh within RizomUV:

1.  **Select Script**: Choose a script from the dropdown menu.
2.  **Folder**: Click `...` to change the folder where your scripts are stored.
3.  **Run Script**: Executes the selected script immediately in RizomUV.

## Troubleshooting

### Connection Issues
If the bridge cannot find `rizomuv.exe`:
1.  Ensure RizomUV is installed.
2.  The bridge will prompt you to locate the `.exe` file manually if auto-detection fails.

### Selection Issues
*   The bridge works best with **Editable Poly** objects.
*   Ensure your object has valid geometry before sending.
