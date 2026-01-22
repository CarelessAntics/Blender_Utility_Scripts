
bl_info = {
    "name": "Quick Vcol",
    "author": "Antti Heikkinen",
    "version": (0, 1, 0),
    "blender": (5, 0, 0),
    "description": "Change color values directly for selected vertices in a handy menu",
    "category": "Utility",
    "doc_url": "https://github.com/CarelessAntics/Blender_Utility_Scripts",
}


import bpy
         

class QuickVcolProps(bpy.types.PropertyGroup):
    
    color_enum_items = [('R', "Red", ""),
                        ('G', "Green", ""),
                        ('B', "Blue", ""),
                        ('A', "Alpha", "")]
    
    color_increment : bpy.props.FloatProperty(name= "Addition Increment", description= "Adds or subtracts vertex colors by this amount (can be negative)", default=.1, min=-1, max=1)
    color_amount : bpy.props.FloatProperty(name= "Set Color Value", description= "Sets the chosen vertex color channels to this value", default=1, min=0, max=1)
    color_channel : bpy.props.EnumProperty(items= color_enum_items, name= "Affected Channels", description= "which color channels are affected (shift+click to select multiple)", default= {'R'}, options= {'ENUM_FLAG'})
        

class QUICKVCOL_OT_ModColor(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "ah.modifycolor"
    bl_label = "Modify Vertex Color"
    bl_options = {'UNDO'}
    
    action : bpy.props.StringProperty()
    channel_indices = {'R': 0, 'G': 1, 'B': 2, 'A': 3}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        scene = context.scene
        vcol_tool = scene.quick_vcol_tool
        
        color = [0, 0, 0, 0]
        
        # see if any channels are selected
        if vcol_tool.color_channel:
            
            # Set the color based on mode and selected channels
            if self.action == 'SET':
                for ch in vcol_tool.color_channel:
                    channel_index = self.channel_indices[ch]
                    color[channel_index] = vcol_tool.color_amount
            
            elif self.action == 'ADD':
                for ch in vcol_tool.color_channel:
                    channel_index = self.channel_indices[ch]
                    color[channel_index] = vcol_tool.color_increment
       
            self.color_vertices(context, color)
            
        return {'FINISHED'}   
    
    def color_vertices(self, context, color : list):    
        import numpy as np
        layername = "Color"
        scene = context.scene
        vcol_tool = scene.quick_vcol_tool
        selection = context.selected_objects
            
        for obj in selection:
            mesh = obj.data
            editmode = False
            
            if obj.mode == 'EDIT':
                
                bpy.ops.object.mode_set(mode='OBJECT')
                editmode = True
                
                # This was for edit mode using bmesh, but I couldn't get it working so I just switch to object mode and then back and it works fine
                # Leaving this here in case I want to return to it some day
                ''' 
                bpy.ops.object.mode_set(mode='EDIT')
                
                bm = bmesh.new()
                bm.from_mesh(mesh)  
                
                selected_verts = [v for v in bm.verts if v.select]
                
                color_layer = bm.verts.layers.float_color.new(layername)
                print(selected_verts)
                
                for vert in selected_verts:
                    vert[color_layer] = color
                    
                bm.to_mesh(mesh)
                mesh.data.update()
                
                bm.free()
                '''
                
            # Create a new color layer and initialize it to black
            if not mesh.color_attributes:
                colattr = mesh.color_attributes.new(layername, 'FLOAT_COLOR', 'POINT')
                colors_init = np.zeros((len(mesh.vertices), 4), dtype=np.float32)
                colattr.data.foreach_set('color', np.ravel(colors_init))
                    
            colattr = mesh.attributes.active_color
            print(colattr)
            selected_verts = [v.index for v in mesh.vertices if v.select]
            
            for vert in selected_verts:
                
                # If directly setting, set only the selected channels and leave the rest as is
                if self.action == 'SET':
                    old_color = colattr.data[vert].color
                    channel_indices = [self.channel_indices[ch] for ch in vcol_tool.color_channel]
                    new_color = [col if i in channel_indices else old_color[i] for i, col in enumerate(color)]
                
                # Add the new vertex colors to old ones with list comprehension                
                if self.action == 'ADD':
                    new_color = [max(c[0] + c[1], 0) for c in zip(color, colattr.data[vert].color)]
                    
                colattr.data[vert].color = new_color
                
            # Reset mode to edit mode
            if editmode:
                bpy.ops.object.mode_set(mode='EDIT')


class QUICKVCOL_PT_VcolPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Quick Vertex Colors"
    bl_idname = "QUICKVCOL_PT_VcolPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "ah tools"
    # bl_options = {'REGISTER', 'UNDO'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        vcol_tool = scene.quick_vcol_tool
        
        layout.prop(vcol_tool, "color_amount")
        layout.prop(vcol_tool, "color_increment")
        layout.prop(vcol_tool, "color_channel", expand=True)
        
        layout.separator()
        
        # Buttons
        layout.operator("ah.modifycolor", text= "Set Vertex Color").action = 'SET'
        layout.operator("ah.modifycolor", text= "Add Vertex Color").action = 'ADD'


classes = [QuickVcolProps, QUICKVCOL_OT_ModColor, QUICKVCOL_PT_VcolPanel]


# Register and add to the "object" menu (required to also use F3 search "Simple Object Operator" for quick access).
def register():
    
    for cls in classes:
        bpy.utils.register_class(cls)
        bpy.types.Scene.quick_vcol_tool = bpy.props.PointerProperty(type=QuickVcolProps)
    

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        del bpy.types.Scene.quick_vcol_tool


if __name__ == "__main__":
    register()

