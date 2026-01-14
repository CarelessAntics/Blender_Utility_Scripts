
bl_info = {
    "name": "Resize Grid",
    "author": "Antti Heikkinen",
    "version": (0, 1, 0),
    "blender": (5, 0, 0),
    "description": "Use hotkeys to resize grid, doubling or halving the size",
    "category": "Utility",
    "doc_url": "",
}


import bpy


def main(context, multiplier):
    
    AREA = 'VIEW_3D'
    
    for window in context.window_manager.windows:
        for area in window.screen.areas:
            if not area.type == AREA:
                continue
            
            for s in area.spaces:
                if s.type == AREA:
                    if multiplier == 0:
                        s.overlay.grid_scale = 1.0
                    else:
                        s.overlay.grid_scale *= multiplier
        
        

class DivideGrid(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "ah.divide_grid"
    bl_label = "Divide Grid Scale"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(context, .5)
        return {'FINISHED'}
    

class MultiplyGrid(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "ah.multiply_grid"
    bl_label = "Multiply Grid Scale"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(context, 2)
        return {'FINISHED'}
        
class ResetGrid(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "ah.reset_grid"
    bl_label = "Reset Grid Scale"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(context, 0)
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(DivideGrid.bl_idname, text=DivideGrid.bl_label)
    self.layout.operator(MultiplyGrid.bl_idname, text=MultiplyGrid.bl_label)
    self.layout.operator(ResetGrid.bl_idname, text=ResetGrid.bl_label)


addon_keymaps = []

# Register and add to the "object" menu (required to also use F3 search "Simple Object Operator" for quick access).
def register():
    bpy.utils.register_class(DivideGrid)
    bpy.utils.register_class(MultiplyGrid)
    bpy.utils.register_class(ResetGrid)
    
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    
    if kc:
        km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
        kmi_div = km.keymap_items.new("ah.divide_grid", type="NUMPAD_MINUS", value="PRESS", shift=True)
        kmi_mul = km.keymap_items.new("ah.multiply_grid", type="NUMPAD_PLUS", value="PRESS", shift=True)
        kmi_res = km.keymap_items.new("ah.reset_grid", type="NUMPAD_0", value="PRESS", shift=True)
        
        addon_keymaps.extend(((km, kmi_div), (km, kmi_mul), (km, kmi_res)))
    
    bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
        
    addon_keymaps.clear()
    
    bpy.utils.unregister_class(DivideGrid)
    bpy.utils.unregister_class(MultiplyGrid)
    bpy.utils.unregister_class(ResetGrid)
    bpy.types.VIEW3D_MT_object.remove(menu_func)


if __name__ == "__main__":
    register()

