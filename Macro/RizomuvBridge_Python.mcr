macroScript RizomuvBridgePy
	category:"Titus_Scripts"
	buttonText:"RizomUV"
	toolTip:"RizomUV Bridge"
	Icon:#("rizomuv" ,1)
(
    -- Add the repo root directory to sys.path so we can import 'RizomuvBridge' package
    python.Execute "import sys; import os; p = r'd:\\git\\RizomuvBridge'; sys.path.append(p) if p not in sys.path else None"
    
    -- Import and show
    python.Execute "import RizomuvBridge.ui; import importlib; importlib.reload(RizomuvBridge.ui); RizomuvBridge.ui.show()"
)
