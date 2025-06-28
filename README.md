This is an animation tool built in Maya 2025 meant for cleaning sliding feet in a walk cycle.

To install it, place this folder wherever you save Maya scripts (recommended: C:/Users/Documents/maya/scripts) and follow these steps:
1. Close Maya if it's open.
2. In your Maya version folder (ex. C:\Users\Documents\maya\2025), find a folder named "modules", or create one if it doesn't exist.
3. Write the following in a blank text document, using notepad or a similar app, replacing the file path in the example with wherever you saved this tool.:
   "+ CycleCleaner 1.0 C:/Users/Documents/maya/scripts
   C:/Users/Documents/maya/scripts"
4. Launch Maya.
5. In a text editor, open the file named, cycleCleanerINSTALL.py and copy its text into a shelf button in Maya.

Pressing the newly added button should launch the tool.

To use the tool, you'll need a scene where a character's locomotion is animated with a world or base control, in such a way that their feet might be sliding. Their cycle must be uniform throughout the time that you run the tool.
1. Select their right IK foot control and press the "<" button next to the "Right Foot Control" text field.
2. Repeat the above step fo rthe left foot control.
3. Enter the frame range that you want the tool to run over. You can enter it manually or press the "<" button next to the frame range text fields to fill them in with your current start and end frames in your Maya scene.
4. Check the radio button for whichever foot starts in front.
5. Enter how long one loop of the character's walk cycle is. (How many frames until the starting foot reaches the frame before its starting position again.)
6. Within the cycle, enter which frames the starting foot is supposed to be on the ground. These values are relative to the cycle, not to the whole timeline.
7. Check the box next to "Anim Layer", and enter a name for the layer, if you want the changes made by the tool to be added on an anim layer. If your walk cycle is repeating the same loop (using Maya's post/pre-infinity curves) an anim layer is necessary.
   If the layer name you entered already exists, the tool will add the controls to that layer and make the changes on it. Otherwise it will create the layer.
