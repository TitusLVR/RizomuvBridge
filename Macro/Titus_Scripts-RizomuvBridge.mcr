macroScript RizomuvBridge
	category:"Titus_Scripts"
	buttonText:"RizomUV"
	toolTip:"RizomUV Bridge"
	Icon:#("rizomuv" ,1)
(
    -- Dynamic path to user scripts (where mzp.run installed the package)
    python.Execute ("import sys; import os; p = r'" + (getDir #userScripts) + "'; sys.path.append(p) if p not in sys.path else None")
    
    -- Import and show
    python.Execute "import RizomuvBridge.ui; import importlib; importlib.reload(RizomuvBridge.ui); RizomuvBridge.ui.show()"
)
