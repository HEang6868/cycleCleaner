import maya.cmds as mc




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
