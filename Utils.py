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


def poseHold(obj, posFrame, holdLen, layer=None):
    """
    Saves a given object's position and rotation, and freezes it in world space for a given frame range to match its tranforms on a given frame.
    """
    mc.currentTime(posFrame)
    pos = mc.xform(obj, q=True, ws=True, t=True)
    rot = mc.xform(obj, q=True, ws=True, ro=True)
    if not layer:
        layer = "BaseAnimation"
    print(f"{obj=}: {posFrame=}, {holdLen=}\n{pos=}\n{rot=}")
    for frm in range(posFrame, (posFrame+holdLen)):
        mc.currentTime(frm)
        mc.xform(obj, ws=True,t=pos, ro=rot)
        mc.setKeyframe(obj, 
                        attribute=["translateX", "translateY", "translateZ", "rotateX", "rotateY", "rotateZ"],
                        animLayer=layer
                        )
        print(f"keyFrame {frm} Set")
        

#poseFreeze("R_Hand", int(mc.currentTime(q=True)), 3)

def funcLoop(start, end, cycleLen, obj, stepA, stepB, animLayer):
    """
    Runs poseFreeze() and animLyrZero() functions for a given object for every loop.
    """
    for frame in range(start, end, cycleLen):
        print(f"\nRunning function loop on frame {frame}.")
        poseHold(obj=obj, posFrame=frame+stepA, holdLen=stepB-stepA, layer=animLayer)
        if animLayer:
            resetFrame = int(frame + (cycleLen/2) + stepB)
            animLyrZero(obj=obj, frame=resetFrame, layer=animLayer)


# control = "R_Hand"
# startFrame = 1
# endFrame = 110
# freezeLen = 3
# cycle = 15
# stepA = 3
# stepB = 6
# animLayer = "test_LYR"

# funcLoop(startFrame, endFrame, cycle, control, stepA, stepB, animLayer)

# control = "L_Hand"
# startFrame = 1
# endframe = 110
# freezeLen = 3
# cycle = 15
# stepA = 3
# stepB = 6

# funcLoop(startFrame, endframe, cycle, control, stepA, stepB)


def addToAnimLYR(obj=False, layer=False):
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

# addToAnimLYR("pCube1","Front_LYR")
# addToAnimLYR("pCube2","Front_LYR")

def focusAnimLyr(layer):
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


def animLyrZero(obj, frame, layer):
    """
    Zeroes out a given object's animation on a given animLayer.
    """
    print(f"Zeroing out frame {frame} on animLayer {layer}")
    mc.setKeyframe(obj, attribute=["translateX", "translateY", "translateZ", "rotateX", "rotateY", "rotateZ"], time=frame, animLayer=layer)
    #focusAnimLyr(layer)
    mc.keyframe(obj, e=True, attribute=["translateX", "translateY", "translateZ", "rotateX", "rotateY", "rotateZ"], absolute=True, valueChange=0, time=(frame,))

# list = [14, 29, 44, 59, 74]
# for num in list:
#     animLyrZero("R_Hand", num, "test_LYR")