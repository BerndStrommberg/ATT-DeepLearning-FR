bl_info = {
    "name": "Blendshape Importer",
    "category": "Import",
}
import bpy
import csv
import os
from bpy_extras.io_utils import ImportHelper 
from bpy.props import StringProperty, BoolProperty, EnumProperty, CollectionProperty, FloatProperty
from bpy.types import Operator 
 

#
#    Menu in window region, object context
#
class ObjectPanel(bpy.types.Panel):
    bl_label = "Import Blendshape Data"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"
 
    def draw(self, context):
        scn = context.scene
        row = self.layout.row(align=True)
        row.alignment = 'EXPAND'
        row.prop(scn, 'BS_Filename')
        row.operator("object.custom_path", icon='FILE')
        row = self.layout.row(align=False)
        row.alignment = 'RIGHT'
        row.prop(scn, 'BS_FPS')
        row = self.layout.row(align=False)
        row.alignment = 'RIGHT'
        row.operator("bs.import", text='Import')



#
#    The Hello button prints a message in the console
#
class ImportButton(bpy.types.Operator):
    bl_idname = "bs.import"
    bl_label = "Import"
 
    def execute(self, context):
        if context.scene.BS_Filename == '':
            print("filename not set")
        else:
            obj = context.active_object.data.shape_keys
            filename = context.scene.BS_Filename
            fps = context.scene.BS_FPS
            with open(filename) as csvfile:
                reader = csv.reader(csvfile)
                frameTime=0.0
                currentFrame = 0.0

                nextFrame = False
        
                for row in reader:
                    if nextFrame == True:
                        nextFrame=False
                        frameTime += float(row[0])
                        currentFrame = fps*frameTime
                        print('frame: %.2f' % (currentFrame) )
                    else:
                        if row[0] == '#':
                            nextFrame=True
                            print('next network frame')
                        else:                
                            obj.key_blocks.get(row[0]).value=float(row[1])
                            obj.keyframe_insert(data_path='key_blocks["'+row[0]+'"].value', frame = currentFrame)            
            
        return{'FINISHED'}  
    

class OpenFile(bpy.types.Operator):
    bl_idname = "object.custom_path"
    bl_label = ""
    __doc__ = ""


    filename_ext = ".txt"
    filter_glob = StringProperty(default="*.txt", options={'HIDDEN'})    


    #this can be look into the one of the export or import python file.
    #need to set a path so so we can get the file name and path
    filepath = StringProperty(name="File Path", description="Filepath used for importing txt files", maxlen= 1024, default= "")
    files = CollectionProperty(
        name="File Path",
        type=bpy.types.OperatorFileListElement,
        )    
    def execute(self, context):
        #set the string path fo the file here.
        #this is a variable created from the top to start it
        context.scene.BS_Filename = self.properties.filepath



        print("*************SELECTED FILES ***********")
        for file in self.files:
            print(file.name)

        print("FILEPATH %s"%self.properties.filepath)#display the file name and current path        
        return {'FINISHED'}


    def draw(self, context):
        self.layout.operator('file.select_all_toggle')        
    def invoke(self, context, event):
        wm = context.window_manager
        wm.fileselect_add(self)
        return {'RUNNING_MODAL'}

def printProp(label, key, scn):
    try:
        val = scn[key]
    except:
        val = 'Undefined'
    print("%s %s" % (key, val))
 


def register():
    bpy.utils.register_module(__name__)
    bpy.types.Scene.BS_FPS = FloatProperty(
        name = "FPS", 
        description = "fps from timeline",
        default = 30,
        min = 1,
        max = 999)
 
    bpy.types.Scene.MyBool = BoolProperty(
        name = "Boolean", 
        default = True,
        description = "True or False?")   
 
    bpy.types.Scene.BS_Filename = StringProperty(
        name = "Filename",
        default = "")
 
def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.BS_FPS
    del bpy.types.Scene.MyBool
    del bpy.types.Scene.BS_Filename
 
if __name__ == "__main__":
    register()