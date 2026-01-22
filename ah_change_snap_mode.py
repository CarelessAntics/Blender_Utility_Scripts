
bl_info = {
    "name": "Scroll Snapping Mode",
    "author": "Antti Heikkinen",
    "version": (0, 1, 0),
    "blender": (5, 0, 0),
    "description": "Scroll through the snap modes with a hotkey",
    "category": "Utility",
    "doc_url": "https://github.com/CarelessAntics/Blender_Utility_Scripts",
}


import bpy


def scroll_snaps(context, direction):
    
    AREA = 'VIEW_3D'
    snaps = ['INCREMENT', 'GRID', 'VERTEX', 'EDGE', 'FACE', 'VOLUME', 'EDGE_MIDPOINT', 'EDGE_PERPENDICULAR']
    current = list(bpy.context.scene.tool_settings.snap_elements_base)[0]
    current_index = snaps.index(current)
    
    for window in context.window_manager.windows:
        for area in window.screen.areas:
            if not area.type == AREA:
                continue
            
            for s in area.spaces:
                if s.type == AREA:
                    new_snap = {snaps[(current_index + direction) % len(snaps)]}
                    bpy.context.scene.tool_settings.snap_elements_base = new_snap
                    
                    
def set_snap_mode(context, mode):
    
    AREA = 'VIEW_3D'
    
    for window in context.window_manager.windows:
        for area in window.screen.areas:
            if not area.type == AREA:
                continue
            
            for s in area.spaces:
                if s.type == AREA:
                    bpy.context.scene.tool_settings.snap_elements_base = mode
        
        
class IncreaseSnap(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "ah.increase_snapmode"
    bl_label = "Scroll Snap Modes Forward"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        scroll_snaps(context, 1)
        return {'FINISHED'}
    

class DecreaseSnap(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "ah.decrease_snapmode"
    bl_label = "Scroll Snap Modes Bacward"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        scroll_snaps(context, -1)
        return {'FINISHED'}
    
    
class SetSnapToVertex(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "ah.setsnap_vertex"
    bl_label = "Set Snapping Mode to Vertex"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        set_snap_mode(context, {'VERTEX'})
        return {'FINISHED'}
   
    
class SetSnapToGrid(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "ah.setsnap_grid"
    bl_label = "Set Snapping Mode to Grid"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        set_snap_mode(context, {'GRID'})
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(IncreaseSnap.bl_idname, text=IncreaseSnap.bl_label)
    self.layout.operator(DecreaseSnap.bl_idname, text=DecreaseSnap.bl_label)


addon_keymaps = []

# Register and add to the "object" menu (required to also use F3 search "Simple Object Operator" for quick access).
def register():
    bpy.utils.register_class(IncreaseSnap)
    bpy.utils.register_class(DecreaseSnap)
    bpy.utils.register_class(SetSnapToVertex)
    bpy.utils.register_class(SetSnapToGrid)
    
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    
    if kc:
        km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
        kmi_inc = km.keymap_items.new("ah.increase_snapmode", type="NONE", value="PRESS")
        kmi_dec = km.keymap_items.new("ah.decrease_snapmode", type="NONE", value="PRESS")
        kmi_vert = km.keymap_items.new("ah.setsnap_vertex", type="NONE", value="PRESS")
        kmi_grid = km.keymap_items.new("ah.setsnap_grid", type="NONE", value="PRESS")
        
        addon_keymaps.extend(((km, kmi_inc), (km, kmi_dec), (km, kmi_vert), (km, kmi_grid)))
    
    bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
        
    addon_keymaps.clear()
    
    bpy.utils.unregister_class(IncreaseSnap)
    bpy.utils.unregister_class(DecreaseSnap)
    bpy.utils.unregister_class(SetSnapToVertex)
    bpy.utils.unregister_class(SetSnapToGrid)
    bpy.types.VIEW3D_MT_object.remove(menu_func)


if __name__ == "__scroll_snaps__":
    register()

