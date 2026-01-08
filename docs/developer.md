# Developer Guide

This document provides an overview of the internal structure of the **RizomuvBridge** for developers who wish to contribute or modify the tool.

## Project Structure

The project is organized efficiently to separate UI, Core Logic, and Max-specific operations.

```text
RizomuvBridge/
├── core.py             # Main Logic Controller
├── ui.py               # PySide Interface
├── max_ops.py          # 3ds Max Specific Operations (pymxs)
├── rizom_client.py     # Communication with RizomUV (TCP/Pipe)
├── settings.py         # Configuration management
├── RizomUVLink/        # Low-level communication library
└── __init__.py         # Package initialization
```

## Key Modules

### `core.py`
The `RizomUVBridgeCore` class acts as the central hub. It coordinates between the UI, the Max operations, and the Rizom client.
*   **Responsibilities**:
    *   Initialize connection.
    *   Orchestrate Export -> Send -> Wait -> Import flow.
    *   Manage temporary file paths.

### `ui.py`
Built with **PySide** (supports both PySide2 and PySide6), this module defines the dockable dialog window.
*   It handles button clicks and updates the UI state based on connection status.
*   It delegates actual logic to `self.core`.

### `max_ops.py`
Encapsulates all direct interactions with the 3ds Max Python API (`pymxs`).
*   **Functions**: `export_fbx`, `import_fbx`, `get_selection`, `transfer_uvs`.
*   This abstraction allows for easier testing and potential porting to other DCCs if `max_ops` is swapped out.

### `rizom_client.py`
Manages the external process control of RizomUV.
*   Handles launching the executable.
*   Sends Lua commands via command-line or TCP socket (depending on implementation in `RizomUVLink`).

## Extension Guide

### Adding a New Button

1.  **Update UI**: In `ui.py`, add a `QPushButton` to the layout.
2.  **Add Logic**: Implement the handler method in `ui.py` (e.g., `on_new_action_clicked`).
3.  **Implement Core**: Call the relevant method in `core.py`. If it's a Rizom command, add a wrapped method in `core.py` that sends the Lua command.

### modifying Export Settings

Check `max_ops.py` to modify how `rt.exportFile` is called. You can adjust flags for FBX or USD export there.

## Debugging

*   Use `print()` statements; these will appear in the 3ds Max Listener window.
*   The module intentionally uses `importlib.reload()` to allow for code updates without restarting 3ds Max.
