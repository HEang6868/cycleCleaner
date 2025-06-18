import maya.cmds as mc


class CycleCleanup():
    """
    Tool window that rebuilds a joint chain to have a chosen number of joints.
    """
    def __init__(self):
        self.winName = "WalkCycleCleanup"
        self.winWidth = 430
        self.winHeight = 290

        if mc.window(self.winName, exists=True):
            mc.deleteUI(self.winName)
        
        mc.window(self.winName, widthHeight=(self.winWidth, self.winHeight), title="Walk Cycle Cleaner")

        #Setup the main layout for the window.
        mainLayout = mc.columnLayout(adj=True, margins=10, rowSpacing=15, columnAlign="left")
        mc.text("Cleans up sliding feet in a walk cycle.", parent=mainLayout)
        #Create the layout that holds the controls.
        mainFormLayout = mc.formLayout(parent=mainLayout, numberOfDivisions=100)
        #Create the inputs that hold the left and right foot controls.
        self.rFootInput = mc.textFieldButtonGrp(label="Right Foot Control: ", 
                                           columnAlign=(1, "left"), 
                                           columnWidth3=(110, 140, 20),
                                           buttonLabel=" < ", 
                                           buttonCommand=lambda: self.inputObj(self.rFootInput)
                                           )
        self.lFootInput = mc.textFieldButtonGrp(label="Left Foot Control: ", 
                                           columnAlign=(1, "left"), 
                                           columnWidth3=(110, 140, 20),
                                           buttonLabel=" < ", 
                                           buttonCommand=lambda: self.inputObj(self.lFootInput)
                                           )
        #Create a layout to hold the frame range inputs.
        fRangeLayout = mc.rowLayout(numberOfColumns=3)
        self.fRangeInputA = mc.textFieldGrp(parent=fRangeLayout, 
                                       label="Frame Range: ",
                                        columnAlign=(1, "left"),
                                        columnWidth2=(110, 50),
                                        )
        self.fRangeInputB = mc.textFieldButtonGrp(parent=fRangeLayout, 
                                       label="  -  ",
                                        columnAlign=(1, "left"),
                                        columnWidth3=(20, 50, 20),
                                        buttonLabel=" < ",
                                        buttonCommand=self.getFrameRange
                                        )
        #Create the starting foot radioButtonGrp.
        self.startFootRBtns = mc.radioButtonGrp(label="Starting Foot",
                                                numberOfRadioButtons=2,
                                                labelArray2=["Right", "Left"],
                                                columnWidth2=(50, 50)
                                                )
        
        #Add the controls to the form layout.
        mc.formLayout(mainFormLayout, e=True, 
                    attachForm=( [self.rFootInput, "left", 5],
                                [self.rFootInput, "right", 5],
                                [self.rFootInput, "top", 5],
                                [self.lFootInput, "left", 5],
                                [self.lFootInput, "right", 5],
                                [fRangeLayout, "left", 5],
                                [fRangeLayout, "right", 5],
                                [self.startFootRBtns, "left", 5],
                                [self.startFootRBtns, "right", 5] 
                                 ),
                    attachControl=( [self.lFootInput, "top", 5, self.rFootInput],
                                   [fRangeLayout, "top", 8, self.lFootInput],
                                   [self.startFootRBtns, "top", 8, fRangeLayout]
                                     )
                    )

        


        #Button that runs the script.
        #mc.button(label="Cleanup Walk Cycle", parent=mainLayout, command=self.cycleCleanup)

        mc.showWindow()



    def inputObj(self, field):
        """
        Gets the last selected object and inputs its name into the given textField.
        """
        selObj = mc.ls(sl=True)[0]
        mc.textFieldButtonGrp(field, e=True, text=selObj)

    
    def getFrameRange(self, *args):
        """
        Checks if there's a selection in the timeline. If there is, input the selected frame range into the fRange textFields. Otherwise input the current frame range.
        """
        TlSel = mc.playbackOptions(q=True, selectionVisible=True)
        if TlSel:
            start = mc.playbackOptions(q=True, selectionStartTime=True)
            end = mc.playbackOptions(q=True, selectionEndTime=True)
        else:
            start = mc.playbackOptions(q=True, minTime=True)
            end = mc.playbackOptions(q=True, maxTime=True)
        mc.textFieldGrp(self.fRangeInputA, e=True, text=start)
        mc.textFieldGrp(self.fRangeInputB, e=True, text=end)
        

        


CycleCleanup()



