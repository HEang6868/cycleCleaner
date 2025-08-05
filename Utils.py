import maya.cmds as mc

# import imp
# imp.reload(mc)


# def inputObj(self, field):
#     """
#     The start of a universal function that gets the last selected object and inputs its name into the given textField, no matter what type of textField..
#     """
#     selObj = mc.ls(sl=True)[0]
#     fieldType = mc.objectTypeUI(field)
#     print(fieldType)
#     if fieldType == "rowGroupLayout":
#         divider = field.rfind("|")
#         textField = field[divider+1:]
#         lastChar = textField[-1]
#         while lastChar.isdigit():
#             textField = textField[:-1]
#             lastChar = textField[-1]
#         print(textField)


def hold_pose(obj, posFrame, holdLen, layer=None):
    """
    Saves a given object's position and rotation, and freezes it in world space for a given frame range to match its tranforms on a given frame.
    """
    #Sets the timeline to the first frame it wants to hold.
    mc.currentTime(posFrame)
    #Sets the animLayer if one hasn't been given.
    if not layer:
        layer = "BaseAnimation"
    else:
        attributes=["translateX", "translateY", "translateZ", "rotateX", "rotateY", "rotateZ"]
        #Reset the keyframe values at the first frame where the foot holds.
        mc.setKeyframe(obj, 
                        attribute=attributes,
                        animLayer=layer,
                        value=0,
                        noResolve=True,
                        time=posFrame
                        )
        #Update the scene by changing the current frame (Otherwise the object will be in the wrong place when the following keys are set.)
        for attr in attributes:
            mc.currentTime(posFrame)

    #Make a locator and match its translation and rotation to the control.
    conLoc = mc.spaceLocator()
    #mc.delete(mc.parentConstraint(obj, conLoc, mo=False) )
    mc.matchTransform(conLoc, obj)

    # For each loop of the walk cycle,
    for frm in range(posFrame, (posFrame+holdLen)):
        #Set the current frame to the given frame.
        mc.currentTime(frm)
        # Match the object's tranforms to the locator.
        mc.matchTransform(obj, conLoc)
        # Set a keyframe.
        mc.setKeyframe(obj, 
                        attribute=["translateX", "translateY", "translateZ", "rotateX", "rotateY", "rotateZ"],
                        animLayer=layer
                        )
        print(f"keyFrame {frm} Set")
    
    #Delete the locator.
    mc.delete(conLoc)

        
# FUNCTION TEST
# poseHold("R_Foot", int(mc.currentTime(q=True)), 4, layer="test_LYR")


def function_loop(start, end, cycleLen, obj, stepA, stepB, animLayer):
    """
    Runs poseFreeze() and animLyrZero() functions for a given object for every cycle.
    """
    for frame in range(start, end, cycleLen):
        print(f"\nRunning function loop on frame {frame}.")
        hold_pose(obj=obj, posFrame=frame+stepA, holdLen=stepB-stepA, layer=animLayer)
        

# FUNCTION TEST

# control = "R_Hand"
# startFrame = 1
# endFrame = 110
# cycle = 15
# stepA = 3
# stepB = 6
# animLayer = "test_LYR"
 
# funcLoop(startFrame, endFrame, cycle, control, stepA, stepB, animLayer)

# control = "L_Hand"
# startFrame = 1
# endframe = 110
# cycle = 15
# stepA = 3
# stepB = 6

# funcLoop(startFrame, endframe, cycle, control, stepA, stepB)


def add_to_anim_lyr(obj=False, layer=False):
    """
    Checks for an animLayer and creates it if it doesn't exist. Adds a given object to the layer.
    """
    #Clears selection and selects the given objects.
    mc.select(clear=True)
    print(f"Adding {obj} to animLayer: {layer}.")
    mc.select(obj)
    #If the animLayer already exists add the object to the layer.
    if mc.animLayer(layer, q=True, exists=True):
        mc.animLayer(layer, e=True, addSelectedObjects=True)
    #Otherwise, make the layer and add the object to it.
    else:
        print(f"Creating animLayer: {layer}. \nAdding {obj} to it.")
        mc.animLayer(layer, addSelectedObjects=True)

# FUNCTION TEST
# addToAnimLYR("pCube1","Front_LYR")
# addToAnimLYR("pCube2","Front_LYR")

def focus_anim_lyr(layer):
    """
    Deselect all animLayers then select the created animLayer.
    """
    if mc.animLayer(layer, q=True, exists=True):
        animLayers = mc.ls(type="animLayer")
        for animLyr in animLayers:
            mc.animLayer(animLyr, e=True, selected=False)
        mc.animLayer(layer, e=True, selected=True)
    else:
        print(f"ERROR: AnimLayer: {layer} is missing.")




