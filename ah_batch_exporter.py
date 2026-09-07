bl_info = {
    "name": "Unreal Batch Exporter",
    "author": "Antti Heikkinen",
    "version": (0, 1, 5),
    "blender": (5, 0, 0),
    "description": "Batch export meshes to Unreal. Moves each root object to world origin and exports them as an .fbx",
    "category": "Utility",
    "doc_url": "https://github.com/CarelessAntics/Blender_Utility_Scripts",
}


import bpy
import os


class LodGroupProps(bpy.types.PropertyGroup):
    
    ah_selector_prefix : bpy.props.StringProperty(name= "Prefix", description= "Adds LodGroup properties for all empties with the selected prefix", default= "SM_")
    ah_prop_export_path : bpy.props.StringProperty(name="Output Path", subtype="DIR_PATH", default="")



class UEBATCHEXPORT_OT_Exporter(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "ah.batch_exporter"
    bl_label = "Batch Exporter"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        self.batch_export(context)
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return self.execute(context)
    
    def batch_export(self, context): 
        scene = context.scene
        exporter = scene.ue_batch_export
        
        # export to blend file location
        export_dir = bpy.path.abspath(exporter.ah_prop_export_path)

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

            bpy.ops.export_scene.fbx(filepath=fn + ".fbx", use_selection=True, global_scale=1, apply_unit_scale=True, apply_scale_options='FBX_SCALE_ALL', use_mesh_modifiers=True, axis_forward='Y', axis_up='Z', use_metadata=False, mesh_smooth_type='OFF')

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
    
    
class UEBATCHEXPORT_OT_LodGroups(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "ah.batch_exporter_lodgroups"
    bl_label = "Add Lodgroup property"
    
    action : bpy.props.StringProperty()
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def execute(self, context):
        if self.action == 'SEL':
            self.set_property_selected(context)
            
        if self.action == 'ALL':
            self.set_property_all(context)
            
        if self.action == 'PRE':
            self.set_property_prefix(context)
            
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return self.execute(context)
    
    def add_LodGroups(self, obj):
        if "fbx_type" not in obj.keys():
            obj["fbx_type"] = "LodGroup"
            
        obj["fbx_type"] = "LodGroup"
        
    def set_property_selected(self, context):
        scene = context.scene
        selection = context.selected_objects
        
        for obj in selection:
            if obj.type == 'EMPTY':
                self.add_LodGroups(obj)
        
    def set_property_all(self, context):
        scene = context.scene
        selection = scene.objects
        
        for obj in selection:
            if obj.type == 'EMPTY':
                self.add_LodGroups(obj)
        
    def set_property_prefix(self, context):
        scene = context.scene
        selection = scene.objects
        exporter = scene.ue_batch_export
        
        for obj in selection:
            if obj.type == 'EMPTY' and obj.name.startswith(exporter.ah_selector_prefix):
                self.add_LodGroups(obj)
    
    
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
        exporter = scene.ue_batch_export
        
        layout.prop(exporter, "ah_prop_export_path")
        
        layout.separator()
        
        # Export Button
        row = layout.row()
        row.scale_y = 3.0
        row.operator("ah.batch_exporter")
        
        layout.separator()
        
        layout.label(text = "Add the LodGroup property to enable LOD exports to UE")
        
        layout.prop(exporter, "ah_selector_prefix")
        
        row = layout.row()
        row.scale_y = 3.0
        row.operator("ah.batch_exporter_lodgroups", text = "Selected").action = 'SEL'
        row.operator("ah.batch_exporter_lodgroups", text = "All").action = 'ALL'
        row.operator("ah.batch_exporter_lodgroups", text = "Prefix").action = 'PRE'
        
        
classes = [LodGroupProps, UEBATCHEXPORT_OT_Exporter, UEBATCHEXPORT_OT_LodGroups, UEBATCHEXPORT_PT_ExporterPanel]


# Register and add to the "object" menu (required to also use F3 search "Simple Object Operator" for quick access).
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        bpy.types.Scene.ue_batch_export = bpy.props.PointerProperty(type=LodGroupProps)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        del bpy.types.Scene.ue_batch_export

if __name__ == "__main__":
    register()



