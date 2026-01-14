bl_info = {
    "name": "Unreal Batch Exporter",
    "author": "Antti Heikkinen",
    "version": (0, 1, 0),
    "blender": (5, 0, 0),
    "description": "Batch export meshes to Unreal. Moves each root object to world origin and exports them as an .fbx",
    "category": "Utility",
    "doc_url": "",
}


# exports each selected object into its own file

import bpy
import os
# import mathutils as mu

def batch_export(context): 
    scene = context.scene
    
    # export to blend file location
    export_dir = bpy.path.abspath(scene.ah_prop_export_path)

    if export_dir == "" or export_dir == "//":
        raise Exception("No path")

    view_layer = context.view_layer

    obj_active = view_layer.objects.active
    selection = context.selected_objects

    bpy.ops.object.select_all(action='DESELECT')

    for obj in selection:
        
        for child in obj.children:
            child.select_set(True)
            
        obj.select_set(True)
    
        # some exporters only use the active object
        view_layer.objects.active = obj
        original_pos = obj.location.copy()
        obj.location = (0., 0., 0.)

        name = bpy.path.clean_name(obj.name)
        fn = os.path.join(export_dir, name)

        bpy.ops.export_scene.fbx(filepath=fn + ".fbx", use_selection=True)

        # Can be used for multiple formats
        # bpy.ops.export_scene.x3d(filepath=fn + ".x3d", use_selection=True)

        obj.location = original_pos

        bpy.ops.object.select_all(action='DESELECT')

        print("written:", fn)


    view_layer.objects.active = obj_active

    for obj in selection:
        obj.select_set(True)


class OBJECT_OT_Exporter(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "ah.batch_exporter"
    bl_label = "Batch Exporter"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        batch_export(context)
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return self.execute(context)
    
class OBJECT_PT_ExporterPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Batch Export"
    bl_idname = "OBJECT_PT_ExporterPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Batch Exporter"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        layout.prop(scene, "ah_prop_export_path")
        
        layout.separator()
        
        # Export Button
        row = layout.row()
        row.scale_y = 3.0
        row.operator("ah.batch_exporter")



# Register and add to the "object" menu (required to also use F3 search "Simple Object Operator" for quick access).
def register():
    bpy.utils.register_class(OBJECT_OT_Exporter)
    bpy.types.Scene.ah_prop_export_path = bpy.props.StringProperty(name="Output Path", subtype="DIR_PATH", default="")
    bpy.utils.register_class(OBJECT_PT_ExporterPanel)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_Exporter)
    del bpy.types.Scene.ah_prop_export_path
    bpy.utils.unregister_class(OBJECT_PT_ExporterPanel)


if __name__ == "__main__":
    register()



