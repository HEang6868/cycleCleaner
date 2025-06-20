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


def poseFreeze(obj, posFrame, freezeLen): #, animLayer=False 
    """
    Saves a given object's position and rotation, and freezes it in world space for a given frame range to match its tranforms on a given frame.
    """
    mc.currentTime(posFrame)
    pos = mc.xform(obj, q=True, ws=True, t=True)
    rot = mc.xform(obj, q=True, ws=True, ro=True)
    print(f"{obj=}\n{posFrame=}, {freezeLen=}\n{pos=} {rot=}")
    for frm in range(posFrame, (posFrame+freezeLen)):
        mc.currentTime(frm)
        mc.xform(obj, ws=True,t=pos, ro=rot)
        mc.setKeyframe(obj, 
                        attribute=["translateX", "translateY", "translateZ", "rotateX", "rotateY", "rotateZ"]
                        )
        print(f"keyFrame {frm} Set")
        


#poseFreeze("R_Hand", int(mc.currentTime(q=True)), 3)

def funcLoop(start, end, cycleLen, obj, stepA, stepB, animLayer):
    """
    Runs poseFreeze() and animLyrZero() functions for a given object for every loop.
    """
    for frame in range(start, end, cycleLen):
        focusAnimLyr(animLayer)
        poseFreeze(obj=obj, posFrame=frame+stepA, freezeLen=stepB-stepA)
        # if animLayer:
        #     resetFrame = int( (cycleLen + cycleLen - stepB) / 2 )
        #     animLyrZero(obj=obj, frame=resetFrame, layer=animLayer)


# control = "R_Hand"
# startFrame = 1
# endFrame = 110
# freezeLen = 3
# cycle = 15
# stepA = 3
# stepB = 6
# animLayer = "Test"

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
        mc.animLayer(layer, addSelectedObjects=True)

# addToAnimLYR("pCube1","Front_LYR")
# addToAnimLYR("pCube2","Front_LYR")

def focusAnimLyr(layer):
    """
    Deselect all animLayers then select the created animLayer.
    """
    animLayers = mc.ls(type="animLayer")
    for animLyr in animLayers:
        mc.animLayer(animLyr, e=True, selected=False)
    mc.animLayer(layer, e=True, selected=True)



def animLyrZero(obj, frame, layer):
    """
    Zeroes out a given object's animation on a given animLayer.
    """
    print("zeroing out")
    focusAnimLyr(layer)
    mc.setKeyframe(obj, attribute=["translateX", "translateY", "translateZ", "rotateX", "rotateY", "rotateZ"], time=frame)
    mc.keyframe(obj, e=True, attribute=["translateX", "translateY", "translateZ", "rotateX", "rotateY", "rotateZ"], absolute=True, valueChange=0, time=(frame,))

#animLyrZero("R_Hand", 11, "test")