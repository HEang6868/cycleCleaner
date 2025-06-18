import maya.cmds as mc


class CycleCleanup():
    """
    Tool window that rebuilds a joint chain to have a chosen number of joints.
    """
    def __init__(self):
        self.winName = "WalkCycleCleanup"
        self.winWidth = 410
        self.winHeight = 290

        if mc.window(self.winName, exists=True):
            mc.deleteUI(self.winName)
        
        mc.window(self.winName, widthHeight=(self.winWidth, self.winHeight), title="Walk Cycle Cleaner")

        mainLayout = mc.columnLayout(adj=True, margins=10, rowSpacing=15, columnAlign="left")

        mc.text("Cleans up sliding feet in a walk cycle.", parent=mainLayout)

        

        #Button that runs the script.
        mc.button(label="Cleanup Walk Cycle", parent=mainLayout, command=self.cycleCleanup)

        mc.showWindow()