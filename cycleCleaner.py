import maya.cmds as mc
import cycleCleaner.utils as cUt
import imp
imp.reload(cUt)
from cycleCleaner.utils import funcLoop, addToAnimLYR, focusAnimLyr



###############################
###   WINDOW CONSTRUCTION   ###
###############################

class CycleCleanup():
    """
    Tool window that rebuilds a joint chain to have a chosen number of joints.
    """
    def __init__(self):
        self.winName = "WalkCycleCleanup"
        self.winWidth = 440
        self.winHeight = 360

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
        self.fRangeStartInput = mc.textFieldGrp(parent=fRangeLayout, 
                                       label="Frame Range: ",
                                        columnAlign=(1, "left"),
                                        columnWidth2=(110, 50),
                                        )
        self.fRangeEndInput = mc.textFieldButtonGrp(parent=fRangeLayout, 
                                       label="  -  ",
                                        columnAlign=(1, "left"),
                                        columnWidth3=(20, 50, 20),
                                        buttonLabel=" < ",
                                        buttonCommand=self.getFrameRange
                                        )
        #Create the starting foot radioButtonGrp.
        self.startFootRBtns = mc.radioButtonGrp(label="Starting Foot: ",
                                                parent=mainFormLayout,
                                                numberOfRadioButtons=2,
                                                labelArray2=["Right", "Left"],
                                                columnAlign3=("left", "center", "center"),
                                                columnWidth3=(110, 80, 50)
                                                )
        #Create the layout to hold the cycle length input.
        stepLenLayout = mc.rowLayout(parent=mainFormLayout, numberOfColumns=2)
        self.stepLenInput = mc.textFieldGrp(label="Cycle Length: ",
                                             parent=stepLenLayout,
                                            columnAlign=(1, "left"),
                                            columnWidth2=(110, 50),
                                            )
        mc.text("The frame range of one step.", parent=stepLenLayout)

        #Create a layout to hold the frame range inputs.
        stepFramesLayout = mc.rowLayout(parent=mainFormLayout, numberOfColumns=4, columnAlign=(3, "left"))
        self.stepStartInput = mc.textFieldGrp(parent=stepFramesLayout, 
                                       label="Step Frames: ",
                                        columnAlign=(1, "left"),
                                        columnWidth2=(110, 50),
                                        )
        self.stepEndInput = mc.textFieldGrp(parent=stepFramesLayout, 
                                       label="  -  ",
                                        columnAlign=(1, "left"),
                                        columnWidth2=(20, 50),
                                        )
        mc.text("The frames in the cycle when\n the foot is on the ground.", parent=stepFramesLayout)

        #Create a layout to hold the animLayer options.
        animLYRLayout = mc.rowLayout(parent=mainFormLayout, numberOfColumns=4)
        mc.text("Anim Layer: ", parent=animLYRLayout, width=110, align="left")
        self.animLYRChkBox = mc.checkBox(label="", 
                                         parent=animLYRLayout,
                                         width=20,
                                         changeCommand=self.UICheck
                                         )
        self.animLYRNameInput = mc.textFieldGrp(placeholderText="Layer Name",
                                                parent=animLYRLayout,
                                                width=130,
                                                enable=False,
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
                                [self.startFootRBtns, "right", 5],
                                [stepLenLayout, "left", 5],
                                [stepLenLayout, "right", 5],
                                [stepFramesLayout, "left", 5],
                                [stepFramesLayout, "right", 5],
                                [animLYRLayout, "left", 5],
                                [animLYRLayout, "right", 5]   
                                 ),
                    attachControl=( [self.lFootInput, "top", 5, self.rFootInput],
                                   [fRangeLayout, "top", 8, self.lFootInput],
                                   [self.startFootRBtns, "top", 8, fRangeLayout],                                   
                                   [stepLenLayout, "top", 8, self.startFootRBtns],                                   
                                   [stepFramesLayout, "top", 8, stepLenLayout],                                   
                                   [animLYRLayout, "top", 8, stepFramesLayout],                                   
                                     )
                    )
        #Button that runs the script.
        mc.button(label="Clean Up walk Cycle!!", parent=mainLayout, command=self.cycleClean)

        mc.showWindow()


########################
###   UI FUNCTIONS   ###
########################

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
        mc.textFieldGrp(self.fRangeStartInput, e=True, text=start)
        mc.textFieldGrp(self.fRangeEndInput, e=True, text=end)
    

    def UICheck(self, *args):
        """
        Checks the animLayer checkbox and toggles the matching textField.
        """
        getChkboxChk = mc.checkBox(self.animLYRChkBox, q=True, value=True)
        mc.textFieldGrp(self.animLYRNameInput, e=True, enable=getChkboxChk)
    

##########################
###   TOOL FUNCTIONS   ###
##########################

    def getData(self, *args):
        """
        Checks that the window is filled out properly and gets the data in it if it is.
        """
        try:
            self.getRFootCtrl = mc.textFieldButtonGrp(self.rFootInput, q=True, text=True)
            self.getLFootCtrl = mc.textFieldButtonGrp(self.lFootInput, q=True, text=True)
            self.getFRangeStart = int(float(mc.textFieldGrp(self.fRangeStartInput, q=True, text=True)))
            self.getFRangeEnd = int(float(mc.textFieldGrp(self.fRangeEndInput, q=True, text=True)))
            self.getStartFoot = int(float(mc.radioButtonGrp(self.startFootRBtns, q=True, sl=True)))
            self.getCycle = int(mc.textFieldGrp(self.stepLenInput, q=True, text=True))
            self.getStepA = int(mc.textFieldGrp(self.stepStartInput, q=True, text=True))
            self.getStepB = int(mc.textFieldGrp(self.stepEndInput, q=True, text=True))
            self.animLYRName = None
            if mc.textFieldGrp(self.animLYRNameInput, q=True, enable=True):
                self.animLYRName = mc.textFieldGrp(self.animLYRNameInput, q=True, text=True)
        except ValueError:
            return print("ERROR: The window is missing information. Double check that you've filled out every section.")
        print("Cleaning walk cycle!")
        print(self.getRFootCtrl, self.getLFootCtrl, self.getFRangeStart, self.getFRangeEnd, self.getStartFoot, self.getCycle, self.getStepA, self.getStepB, self.animLYRName)
        return self.getRFootCtrl, self.getLFootCtrl, self.getFRangeStart, self.getFRangeEnd, self.getStartFoot, self.getCycle, self.getStepA, self.getStepB, self.animLYRName


    def cycleClean(self, *args):
        self.getData()              #-> self.getRFootCtrl, self.getLFootCtrl, self.getFRangeStart, self.getFRangeEnd, self.getStartFoot, self.getCycle, self.getStepA, self.getStepB, self.animLYRName
        #Set which foot is in front.
        if self.getStartFoot == 1:
            footOrder = [self.getRFootCtrl, self.getLFootCtrl]
        else:
            footOrder = [self.getLFootCtrl, self.getRFootCtrl]
        print(footOrder)
        #Check if autokey is on and turn it off it is.
        autoKey = mc.autoKeyframe(q=True, state=True)
        if autoKey:
            mc.autoKeyframe(state=False)
        #If an animLayer is wanted, create and/or add the foot controls to it.
        if self.animLYRName:
            for foot in footOrder:
                addToAnimLYR(foot, self.animLYRName)
            focusAnimLyr(self.animLYRName)
            print(self.animLYRName)
        funcLoop(self.getFRangeStart, self.getFRangeEnd, self.getCycle, footOrder[0], self.getStepA, self.getStepB, self.animLYRName)
        funcLoop(self.getFRangeStart, self.getFRangeEnd, self.getCycle, footOrder[1], self.getStepA+self.getCycle, self.getStepB+self.getCycle, self.animLYRName)

        # if self.animLYRName:
        #     halfStep = int(self.getCycle / 2)
        #     for foot in footOrder:
        #         for frame in range(self.getFRangeStart, self.getFRangeEnd, halfStep+self.getCycle):
        #             animLyrZero(foot, frame,self.animLYRName)
        
        #If autokey was on when the tool was run, turn it back on.
        if autoKey:
            mc.autoKeyframe(state=True)

        
        


CycleCleanup()



