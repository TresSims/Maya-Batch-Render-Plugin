import sys
import maya.OpenMaya as om
import maya.OpenMayaMPx as MPx
import maya.cmds as cmds

pluginName = "Batch Render Special"
pyPluginCommand = "batchRenderSpecial"

frameArray = [1, 200]

fileType = ".jpeg"

editor = "renderView"

filePath = ""

# Command
class scriptedCommand(MPx.MPxCommand):
    def __init__(self):
        MPx.MPxCommand.__init__(self)
        
    # Invoked when the command is run.
    def doIt(self,argList):
        renderImage()

# Creator
def cmdCreator():
    return MPx.asMPxPtr( scriptedCommand() )
    
# Initialize the script plug-in
def initializePlugin(mobject):
    mplugin = MPx.MFnPlugin(mobject)

    try:
        mplugin.registerCommand( pyPluginCommand, cmdCreator)
    except:
        sys.stderr.write("Failed to register command %s\n" % pyPluginCommand)

    #create default filepath on init
    if(filePath == ""):
        filePath = cmds.workspace(q=True, dir=True)+"/images"


# Uninitialize the script plug-in
def uninitializePlugin(mobject):
    mplugin = MPx.MFnPlugin(mobject)

    if(cmds.menu(label=pluginName, ex=True)):
        try:
            cmds.menu(label=pluginName, dai=True )
        except:
            sys.stderr.write("Failed to remove window for %s\n" % pluginName)
            raise


    try:
        mplugin.deregisterCommand( pyPluginCommand )
    except:
        sys.stderr.write( "Failed to unregister command: %s\n" % pyPluginCommand )

#TODO: create GUI for using the command
def createRenderMenu():

    print("unimplemented")


def renderImages():

    if(filePath == None):
        sys.stderr.write("Your save directory isn't set! \n")

    #sets render region to currently visible region
    frameArray = cmds.timeControl(ra=True)

    for frame in range(frameArray[0], frameArray[1]):
        cmds.currentTime(frame)
        try:
            cmds.renderWindowEditor(editor, e=True, writeImage='%s%d%s' % (filePath, frame, fileType))
        except:
            sys.stderr.write("We couldn't render your image at frame %d\n!" % frame)
            raise
