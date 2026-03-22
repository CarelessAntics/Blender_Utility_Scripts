bl_info = {
    "name": "Unreal Batch Exporter",
    "author": "Antti Heikkinen",
    "version": (0, 1, 4),
    "blender": (5, 0, 0),
    "description": "Batch export meshes to Unreal. Moves each root object to world origin and exports them as an .fbx",
    "category": "Utility",
    "doc_url": "https://github.com/CarelessAntics/Blender_Utility_Scripts",
}


import bpy
import os


def batch_export(context): 
    scene = context.scene
    
    # export to blend file location
    export_dir = bpy.path.abspath(scene.ah_prop_export_path)

    if export_dir == "" or export_dir == "//":
        raise Exception("No path")
        
    # Must be in object mode for the export to work. Also seems like you can't always switch back when you have empties selected, so this just leaves you in export mode
    if context.object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    view_layer = context.view_layer

    obj_active = view_layer.objects.active
    selection = context.selected_objects

    bpy.ops.object.select_all(action='DESELECT')

    for obj in selection:
        # Dictionary to contain empties (sockets) and their original scales so they can be scaled down. Otherwise unreal shows them as way too large
        empty_scales = {}
        
        # Select child objects
        for child in obj.children_recursive:
            child.select_set(True)
            
            # Scale down the parented empties
            if child.type == 'EMPTY':
                print(child)
                empty_scales[child] = tuple(child.scale)
                child.scale = (.01, .01, .01)
            
        obj.select_set(True)
    
        # Move Root object to origin
        view_layer.objects.active = obj
        original_pos = obj.location.copy()
        obj.location = (0., 0., 0.)

        name = bpy.path.clean_name(obj.name)
        fn = os.path.join(export_dir, name)

        bpy.ops.export_scene.fbx(filepath=fn + ".fbx", use_selection=True, global_scale=1, apply_unit_scale=True, apply_scale_options='FBX_SCALE_ALL', use_mesh_modifiers=True, axis_forward='Y', axis_up='Z', use_metadata=False)

        # Return root back to original location
        obj.location = original_pos
        
        # Return empty object (socket) scales back to normal
        for empty, old_scale in empty_scales.items():
            empty.scale = old_scale

        bpy.ops.object.select_all(action='DESELECT')

    view_layer.objects.active = obj_active

    # Reselect previous selections
    for obj in selection:
        obj.select_set(True)


class UEBATCHEXPORT_OT_Exporter(bpy.types.Operator):
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
    
class UEBATCHEXPORT_PT_ExporterPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Batch Export"
    bl_idname = "UEBATCHEXPORT_PT_ExporterPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "ah tools"

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
    bpy.utils.register_class(UEBATCHEXPORT_OT_Exporter)
    bpy.types.Scene.ah_prop_export_path = bpy.props.StringProperty(name="Output Path", subtype="DIR_PATH", default="")
    bpy.utils.register_class(UEBATCHEXPORT_PT_ExporterPanel)


def unregister():
    bpy.utils.unregister_class(UEBATCHEXPORT_OT_Exporter)
    del bpy.types.Scene.ah_prop_export_path
    bpy.utils.unregister_class(UEBATCHEXPORT_PT_ExporterPanel)


if __name__ == "__main__":
    register()



