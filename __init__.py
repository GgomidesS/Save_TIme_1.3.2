# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "Save TIme",
    "author" : "Gabriel Gomides Surjus", 
    "description" : "",
    "blender" : (3, 3, 1),
    "version" : (1, 3, 2),
    "location" : "",
    "warning" : "",
    "doc_url": "", 
    "tracker_url": "", 
    "category" : "Geral" 
}


import bpy
import bpy.utils.previews
from .easybpy import *
from bpy.app.handlers import persistent
import os


addon_keymaps = {}
_icons = None
class SNA_OT_Auto_Material_9714F(bpy.types.Operator):
    bl_idname = "sna.auto_material_9714f"
    bl_label = "Auto_Material"
    bl_description = "Nome Tex = T_Chunk_nomeDoObjeto_DF/NR/MRA/MRE/MRO. As texturas devem estar no .blend. SimplrBake não importa os MRs para dentro do .blend"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        import string

        def percorreObjetosCelecionados(objetos):
            for obj in objetos:
                if obj.type == 'MESH':
                    bpy.ops.object.select_all(action='DESELECT')
                    bpy.context.view_layer.objects.active = obj
                    nomeChunk_nomeDoObjeto = montaNomeChunk_nomeDoObjeto(obj)            
                    removeMateriaisAntigos(obj)            
                    novoMaterial, materialExiste = criaMaterial(obj, nomeChunk_nomeDoObjeto)
                    if not(materialExiste):
                        nodes, bsdf, NormalMap, SeparateColor = criaPrincipaisNodes(obj, novoMaterial)
                        todasImagens = retornaTodasImagens()
                        imagensDF = retornaImagens(todasImagens, 'DF')
                        imagensNR = retornaImagens(todasImagens, 'NR')
                        imagensMRA = retornaImagens(todasImagens, 'MRA')
                        imagensMRE = retornaImagens(todasImagens, 'MRE')
                        imagensMRO = retornaImagens(todasImagens, 'MRO')
                        imagensRG = retornaImagens(todasImagens, 'RG')
                        imagensMT = retornaImagens(todasImagens, 'MT')
                        imagensEM = retornaImagens(todasImagens, 'EM')
                        montaNodesDeImagens(nodes, bsdf, NormalMap, SeparateColor, imagensDF, imagensNR, imagensMRA, imagensMRE, imagensMRO, imagensRG, imagensMT, imagensEM, nomeChunk_nomeDoObjeto)
        #--------------------------------------------------------------------------

        def montaNodesDeImagens(nodes, bsdf, NormalMap, SeparateColor, imagensDF, imagensNR, imagensMRA, imagensMRE, imagensMRO, imagensRG, imagensMT, imagensEM, nomeChunk_nomeDoObjeto):
            nomeChunk_nomeDoObjetoSplit = nomeChunk_nomeDoObjeto.split('_')
            tamnahoVetNomeChunk_nomeDoObjeto = len(nomeChunk_nomeDoObjetoSplit)
            imagemDFSplit = []
            for i in imagensDF:
                cont = int(0)
                imagemDFSplit = i.name.split('_')
                for n in nomeChunk_nomeDoObjetoSplit:
                    for d in imagemDFSplit:
                        if (n == d):
                            cont += 1
                if (cont == tamnahoVetNomeChunk_nomeDoObjeto):
                    texDF = create_node(nodes, 'ShaderNodeTexImage')
                    texDF.image = get_image(i) 
                    texDF.location.x = -400
                    texDF.location.y = 300
                    create_node_link(texDF.outputs[0], bsdf.inputs[0])
                    imagemNRSplit = []
                    for i in imagensNR:
                        cont = int(0)
                        imagemNRSplit = i.name.split('_')
                        for n in nomeChunk_nomeDoObjetoSplit:
                            for d in imagemNRSplit:
                                if (n == d):
                                    cont += 1
                        if (cont == tamnahoVetNomeChunk_nomeDoObjeto):
                            texNR = create_node(nodes, 'ShaderNodeTexImage')
                            texNR.image = get_image(i)
                            bpy.data.images[texNR.image.name].colorspace_settings.name = 'Non-Color'
                            texNR.location.x = -500
                            texNR.location.y = -260
                            create_node_link(texNR.outputs[0], NormalMap.inputs[1])
                    imagemMRASplit = []
                    for i in imagensMRA:
                        cont = int(0)
                        imagemMRASplit = i.name.split('_')
                        for n in nomeChunk_nomeDoObjetoSplit:
                            for d in imagemMRASplit:
                                if (n == d):
                                    cont += 1
                        if (cont == tamnahoVetNomeChunk_nomeDoObjeto):
                            texMR = create_node(nodes, 'ShaderNodeTexImage')
                            texMR.image = get_image(i)
                            bpy.data.images[texMR.image.name].colorspace_settings.name = 'Linear'
                            create_node_link(texMR.outputs[0], SeparateColor.inputs[0])
                            texMR.location.x = -800
                            texMR.location.y = 0
                    imagemMRESplit = []
                    for i in imagensMRE:
                        cont = int(0)
                        imagemMRESplit = i.name.split('_')
                        for n in nomeChunk_nomeDoObjetoSplit:
                            for d in imagemMRESplit:
                                if (n == d):
                                    cont += 1
                        if (cont == tamnahoVetNomeChunk_nomeDoObjeto):
                            texMR = create_node(nodes, 'ShaderNodeTexImage')
                            texMR.image = get_image(i)
                            bpy.data.images[texMR.image.name].colorspace_settings.name = 'Linear'
                            create_node_link(texMR.outputs[0], SeparateColor.inputs[0])
                            texMR.location.x = -800
                            texMR.location.y = 0
                            create_node_link(SeparateColor.outputs[2], bsdf.inputs[19])
                    imagemMROSplit = []
                    for i in imagensMRO:
                        cont = int(0)
                        imagemMROSplit = i.name.split('_')
                        for n in nomeChunk_nomeDoObjetoSplit:
                            for d in imagemMROSplit:
                                if (n == d):
                                    cont += 1
                        if (cont == tamnahoVetNomeChunk_nomeDoObjeto):
                            texMR = create_node(nodes, 'ShaderNodeTexImage')
                            texMR.image = get_image(i)
                            bpy.data.images[texMR.image.name].colorspace_settings.name = 'Linear'
                            create_node_link(texMR.outputs[0], SeparateColor.inputs[0])
                            texMR.location.x = -800
                            texMR.location.y = 0
                            create_node_link(texMR.outputs[1], bsdf.inputs[21])
                            bpy.context.object.active_material.blend_method = 'CLIP'
                    imagemRGSplit = []
                    for i in imagensRG:
                        cont = int(0)
                        imagemRGSplit = i.name.split('_')
                        for n in nomeChunk_nomeDoObjetoSplit:
                            for d in imagemRGSplit:
                                if (n == d):
                                    cont += 1
                        if (cont == tamnahoVetNomeChunk_nomeDoObjeto):
                            texMR = create_node(nodes, 'ShaderNodeTexImage')
                            texMR.image = get_image(i)
                            bpy.data.images[texMR.image.name].colorspace_settings.name = 'Linear'
                            create_node_link(texMR.outputs[0], bsdf.inputs[9])
                            texMR.location.x = -800
                            texMR.location.y = 0
                    imagemMTSplit = []
                    for i in imagensMT:
                        cont = int(0)
                        imagemMTSplit = i.name.split('_')
                        for n in nomeChunk_nomeDoObjetoSplit:
                            for d in imagemMTSplit:
                                if (n == d):
                                    cont += 1
                        if (cont == tamnahoVetNomeChunk_nomeDoObjeto):
                            texMR = create_node(nodes, 'ShaderNodeTexImage')
                            texMR.image = get_image(i)
                            bpy.data.images[texMR.image.name].colorspace_settings.name = 'Linear'
                            create_node_link(texMR.outputs[0], bsdf.inputs[6])
                            texMR.location.x = -800
                            texMR.location.y = 0
                    imagemEMSplit = []
                    for i in imagensEM:
                        cont = int(0)
                        imagemEMSplit = i.name.split('_')
                        for n in nomeChunk_nomeDoObjetoSplit:
                            for d in imagemEMSplit:
                                if (n == d):
                                    cont += 1
                        if (cont == tamnahoVetNomeChunk_nomeDoObjeto):
                            texMR = create_node(nodes, 'ShaderNodeTexImage')
                            texMR.image = get_image(i)
                            bpy.data.images[texMR.image.name].colorspace_settings.name = 'Linear'
                            create_node_link(texMR.outputs[0], bsdf.inputs[19])
                            texMR.location.x = -800
                            texMR.location.y = 0
        #--------------------------------------------------------------------------

        def retornaImagens(imagens, nome):
            imagensSelecionadas = []
            for i in imagens:
                nomeImagemSplit = i.name.split('_')
                for n in nomeImagemSplit:
                    if (n == nome or n == nome + '.png'):
                        imagensSelecionadas.append(i)    
            return imagensSelecionadas
        #--------------------------------------------------------------------------

        def retornaTodasImagens():
            return get_all_images()
        #--------------------------------------------------------------------------

        def criaPrincipaisNodes(obj, material):     
            nodes = get_nodes(material)
            bsdf = get_node(nodes, 'Principled BSDF')
            NormalMap = create_node(nodes , 'ShaderNodeNormalMap')
            NormalMap.location.x = -200
            NormalMap.location.y = -260
            create_node_link(NormalMap.outputs[0], bsdf.inputs[22])
            SeparateColor = create_node(nodes , 'ShaderNodeSeparateColor')
            SeparateColor.location.x = -400
            SeparateColor.location.y = 0
            create_node_link(SeparateColor.outputs[0], bsdf.inputs[6])
            create_node_link(SeparateColor.outputs[1], bsdf.inputs[9])
            return nodes, bsdf, NormalMap, SeparateColor
        #--------------------------------------------------------------------------

        def criaMaterial(obj, nomeMaterial):
            novoNomeMaterial = 'MI_' + nomeMaterial
            vetMateriais = get_all_materials()   
            existe = material_exists(novoNomeMaterial)
            if (existe):        
                novoMaterial = add_material_to_object(obj, novoNomeMaterial)
                materialExiste = True
                return novoMaterial, materialExiste
            else:
                novoMaterial = create_material(novoNomeMaterial)
                novoMaterial.use_nodes = True
                add_material_to_object(obj, novoMaterial) 
                materialExiste = False
                return novoMaterial, materialExiste  
        #--------------------------------------------------------------------------

        def removeMateriaisAntigos(obj):
            materiaisDoObjeto = get_materials_from_object(obj)
            nomeSplit = []   
            for material in materiaisDoObjeto:
                key = True 
                nomeSplit = []
                saveNomeSplit = material.name.split('_')
                saveNome = ''
                for nome in saveNomeSplit:
                    saveNome = nome.split('.')
                    nomeSplit.extend(saveNome)
                for n in nomeSplit:
                    if(n.lower() == 'glass' or n.lower() == 'mirror'):
                        key = False
                    elif(n.lower() == 'finishkit' or n.lower() == 'trimsheet'):            
                        bpy.ops.object.material_slot_remove()                
                        key = False
                if (key):
                    material.name = str(material.name) + '_OLD'
                    bpy.ops.object.material_slot_remove()       
        #--------------------------------------------------------------------------            

        def montaNomeChunk_nomeDoObjeto(obj):
            nomeSplit = obj.name.split('_')
            tamanhoVetNomeSplit = len(nomeSplit)
            chunk = nomeSplit[tamanhoVetNomeSplit - 1]
            novoNome = chunk
            alfabeto = list(string.ascii_lowercase)
            letra = ''       
            for n in nomeSplit:
                for a in alfabeto:
                    if (n == a):
                        letra = a                   
            for n in nomeSplit:                               
                if (n != chunk and n != letra):
                    novoNome += '_' + n               
            return novoNome
        #--------------------------------------------------------------------------    
        percorreObjetosCelecionados(selected_objects())
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Corrige_Undefinednode_De0Bc(bpy.types.Operator):
    bl_idname = "sna.corrige_undefinednode_de0bc"
    bl_label = "corrige_UndefinedNode"
    bl_description = "corrige_UndefinedNode"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):

        def percorreObjetosCelecionados(objetos):
            for obj in objetos:
                if obj.type == 'MESH':
                    bpy.ops.object.select_all(action='DESELECT')
                    bpy.context.view_layer.objects.active = obj
                    materiais = pegaMaterialObj(obj)
                    trocaUndefinedNode(materiais, obj)
        #-----------------------------------------------------------

        def trocaUndefinedNode(materials, obj):
            for material in materials:
                key = False        
                nodes = get_nodes(material)
                vetImagens = []    
                for n in nodes:
                    if (n.type == 'TEX_IMAGE'):
                        vetImagens.append(n) 
                    DFBool, NRBool, MRABool, MREBool, MROBool, nomeNodeDF, nomeNodeMR, nomeNodeNR = retornaDFMRNR(vetImagens)                              
                    if (n.name == 'Separate Color' or n.name == 'Separate RGB'):
                        nodes.remove(n)
                        montaShader(DFBool, NRBool, MRABool, MREBool, MROBool, nomeNodeDF, nomeNodeMR, nomeNodeNR, nodes)
        #-----------------------------------------------------------

        def montaShader(DFBool, NRBool, MRABool, MREBool, MROBool, nomeNodeDF, nomeNodeMR, nomeNodeNR, nodes):
            bsdf = get_node(nodes, 'Principled BSDF')
            SeparateColor = create_node(nodes , 'ShaderNodeSeparateColor')
            SeparateColor.location.x = -400
            SeparateColor.location.y = 0
            create_node_link(SeparateColor.outputs[0], bsdf.inputs[6])
            create_node_link(SeparateColor.outputs[1], bsdf.inputs[9])
            if (MRABool or MREBool or MROBool):
                MR = get_node(nodes, nomeNodeMR)
                MR.location.x = -800
                MR.location.y = 0
                create_node_link(MR.outputs[0], SeparateColor.inputs[0])
                bpy.data.images[MR.image.name].colorspace_settings.name = 'Linear'
                if (DFBool and MRABool):
                    mixRGB = create_node(nodes , 'ShaderNodeMixRGB')
                    mixRGB.location.x = -400
                    mixRGB.location.y = 200            
                    create_node_link(mixRGB.outputs[0], bsdf.inputs[0])
                    DF = get_node(nodes, nomeNodeDF)
                    DF.location.x = -800
                    DF.location.y = 300
                    create_node_link(DF.outputs[0], mixRGB.inputs[1])
                    create_node_link(SeparateColor.outputs[2], mixRGB.inputs[2])
                elif (MREBool):
                    create_node_link(SeparateColor.outputs[2], bsdf.inputs[19])
                elif(MROBool):
                    create_node_link(MR.outputs[1], bsdf.inputs[21])
                    bpy.context.object.active_material.blend_method = 'CLIP'
            if(NRBool):
                NR = get_node(nodes, nomeNodeNR)
                bpy.data.images[NR.image.name].colorspace_settings.name = 'Non-Color'
                NR.location.x = -800
                NR.location.y = -300
        #-----------------------------------------------------------

        def retornaDFMRNR(imagens):    
            DF = False    
            NR = False
            MRA = False
            MRE = False
            MRO = False   
            DFNodeNome = ''
            MRNodeNome = ''
            NRNodeNome = ''
            for i in imagens:
                nomeSplitImagem = i.image.name.split('_')
                for n in nomeSplitImagem:
                    if (n == 'DF'):        
                        DF = True
                        DFNodeNome = i.name
                    elif (n == 'NR'):
                        NR = True
                        NRNodeNome = i.name
                    elif (n == 'MRA'):
                        MRA = True
                        MRNodeNome = i.name
                    elif (n == 'MRE'):
                        MRE = True
                        MRNodeNome = i.name
                    elif (n == 'MRO'):
                        MRO = True
                        MRNodeNome = i.name
            return DF, NR, MRA, MRE, MRO, DFNodeNome, MRNodeNome, NRNodeNome
        #-----------------------------------------------------------

        def pegaMaterialObj(obj):
            materiais = get_materials_from_object(obj)
            return materiais
        #-----------------------------------------------------------
        percorreObjetosCelecionados(selected_objects())
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Limpa_Mesh_8D290(bpy.types.Operator):
    bl_idname = "sna.limpa_mesh_8d290"
    bl_label = "Limpa_Mesh"
    bl_description = "Remove Mark Sharp, Remove Triangulos, Limpo Custom Split Normals, liga AutoSmooth 66. Configura a Viewport"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        #---------------------------------------------------------

        def start(): 
            objetosSelecionados = retornaObjetosSelecionados()
            percorreObjetosSelecionados(objetosSelecionados)
            configuraViewport()     
        #---------------------------------------------------------

        def percorreObjetosSelecionados(objetos):
            for obj in objetos:
                    if obj.type == 'MESH':
                        bpy.ops.object.select_all(action='DESELECT')
                        bpy.context.view_layer.objects.active = obj                
                        limpaMeshs(obj)               
        #---------------------------------------------------------

        def configuraViewport():
            win = bpy.context.window
            scr = win.screen
            areas3d  = [area for area in scr.areas if area.type == 'VIEW_3D']
            area = areas3d[0]
            space = area.spaces[0]
            regions   = [region for region in areas3d[0].regions if region.type == 'WINDOW']
            shading = space.shading
            shading.type='SOLID' # 'WIREFRAME' 'SOLID', 'MATERIAL', 'RENDERED'
            shading.light='MATCAP' # 'MATCAP' 'STUDIO' 'FLAT'
            shading.color_type='RANDOM' # 'MATERIAL', 'SINGLE', 'OBJECT', 'RANDOM', 'VERTEX', 'TEXTURE'
            shading.studio_light='basic_1.exr'
            shading.show_cavity = True
            shading.cavity_type = 'BOTH'
            shading.cavity_ridge_factor = 2.5
            shading.cavity_valley_factor = 2.5
            bpy.ops.render.opengl()
        #---------------------------------------------------------

        def limpaMeshs(obj):
            set_edit_mode(obj)
            bpy.ops.mesh.reveal()
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.mark_sharp(clear=True)
            bpy.ops.mesh.tris_convert_to_quads(shape_threshold=3.14159)
            set_object_mode(obj)
            bpy.ops.mesh.customdata_custom_splitnormals_clear()               
            shade_object_smooth(obj)
            set_smooth_angle(obj, 66)
        #---------------------------------------------------------

        def retornaObjetosSelecionados():
            return selected_objects()
        #---------------------------------------------------------
        start()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Renomeia_Malha_7F608(bpy.types.Operator):
    bl_idname = "sna.renomeia_malha_7f608"
    bl_label = "Renomeia_Malha"
    bl_description = "Renomeia Malha com Nome do Objeto"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        ObjetosSelecionados = selected_objects()
        for obj in ObjetosSelecionados:
            if obj.type == 'MESH':
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.view_layer.objects.active = obj
                bpy.context.view_layer.objects.active.data.name = bpy.context.view_layer.objects.active.name
        #---------------------------------------------------------------------

        def start():
            objetosSelecionados = retornaObjetosSelecionados()
            percorreObjetosSelecionados(objetosSelecionados)    
        #---------------------------------------------------------------------

        def nomeiaMalha():
            bpy.context.view_layer.objects.active.data.name = bpy.context.view_layer.objects.active.name
        #---------------------------------------------------------------------

        def percorreObjetosSelecionados(objetos):
            for obj in objetos:
                if obj.type == 'MESH':
                    bpy.ops.object.select_all(action='DESELECT')
                    bpy.context.view_layer.objects.active = obj
                    nomeiaMalha()
        #---------------------------------------------------------------------    

        def retornaObjetosSelecionados():
            return selected_objects()    
        #---------------------------------------------------------------------
        start()    
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Clear_Parent_6A9Dc(bpy.types.Operator):
    bl_idname = "sna.clear_parent_6a9dc"
    bl_label = "Clear_Parent"
    bl_description = "Limpa Parent De todos os Objetos vistos na cena"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):

        def start():
            limpaParent()

        def limpaParent():
            select_all_objects()
            bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
        start()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Applyall_B0Bb8(bpy.types.Operator):
    bl_idname = "sna.applyall_b0bb8"
    bl_label = "ApplyAll"
    bl_description = "Da ``ApplyAll`` em todos os objetos vistos na cena"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):

        def start():
            aplicaObjetos()

        def aplicaObjetos():
            select_all_objects()
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        start()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_PT_TRIMSHEET_UV_MANIPULATION_6912C(bpy.types.Panel):
    bl_label = 'TrimSheet UV Manipulation'
    bl_idname = 'SNA_PT_TRIMSHEET_UV_MANIPULATION_6912C'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_category = 'TrimSheet UV Manipulation'
    bl_order = 0
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not ((not 'EDIT_MESH'==bpy.context.mode))

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        box_39B85 = layout.box()
        box_39B85.alert = False
        box_39B85.enabled = True
        box_39B85.active = True
        box_39B85.use_property_split = False
        box_39B85.use_property_decorate = False
        box_39B85.alignment = 'Expand'.upper()
        box_39B85.scale_x = 1.0
        box_39B85.scale_y = 1.0
        box_39B85.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        split_01933 = box_39B85.split(factor=0.5, align=False)
        split_01933.alert = False
        split_01933.enabled = True
        split_01933.active = True
        split_01933.use_property_split = False
        split_01933.use_property_decorate = False
        split_01933.scale_x = 1.0
        split_01933.scale_y = 1.0
        split_01933.alignment = 'Expand'.upper()
        split_01933.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        op = split_01933.operator('sna.mover_uv_trimsheet_l01_b67e0', text='L01 - Luz', icon_value=0, emboss=True, depress=False)
        op = split_01933.operator('sna.mover_uv_trimsheet_r01_67ada', text='R01 - Parede Branca', icon_value=0, emboss=True, depress=False)
        split_3607F = box_39B85.split(factor=0.5, align=False)
        split_3607F.alert = False
        split_3607F.enabled = True
        split_3607F.active = True
        split_3607F.use_property_split = False
        split_3607F.use_property_decorate = False
        split_3607F.scale_x = 1.0
        split_3607F.scale_y = 1.0
        split_3607F.alignment = 'Expand'.upper()
        split_3607F.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        op = split_3607F.operator('sna.mover_uv_trimsheet_l02_56d52', text='L02 - Plástico Branco', icon_value=0, emboss=True, depress=False)
        op = split_3607F.operator('sna.mover_uv_trimsheet_r02_8ad95', text='R02', icon_value=0, emboss=True, depress=False)
        split_C49B8 = box_39B85.split(factor=0.5, align=False)
        split_C49B8.alert = False
        split_C49B8.enabled = True
        split_C49B8.active = True
        split_C49B8.use_property_split = False
        split_C49B8.use_property_decorate = False
        split_C49B8.scale_x = 1.0
        split_C49B8.scale_y = 1.0
        split_C49B8.alignment = 'Expand'.upper()
        split_C49B8.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        op = split_C49B8.operator('sna.mover_uv_trimsheet_l03_21da0', text='L03 - Plático Amarelo', icon_value=0, emboss=True, depress=False)
        op = split_C49B8.operator('sna.mover_uv_trimsheet_r03_ed672', text='R03', icon_value=0, emboss=True, depress=False)
        split_7125A = box_39B85.split(factor=0.5, align=False)
        split_7125A.alert = False
        split_7125A.enabled = True
        split_7125A.active = True
        split_7125A.use_property_split = False
        split_7125A.use_property_decorate = False
        split_7125A.scale_x = 1.0
        split_7125A.scale_y = 1.0
        split_7125A.alignment = 'Expand'.upper()
        split_7125A.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        op = split_7125A.operator('sna.mover_uv_trimsheet_l04_0d677', text='L04 - Platico Preto', icon_value=0, emboss=True, depress=False)
        op = split_7125A.operator('sna.mover_uv_trimsheet_r04_7972e', text='R04', icon_value=0, emboss=True, depress=False)
        split_05503 = box_39B85.split(factor=0.5, align=False)
        split_05503.alert = False
        split_05503.enabled = True
        split_05503.active = True
        split_05503.use_property_split = False
        split_05503.use_property_decorate = False
        split_05503.scale_x = 1.0
        split_05503.scale_y = 1.0
        split_05503.alignment = 'Expand'.upper()
        split_05503.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        op = split_05503.operator('sna.mover_uv_trimsheet_l05_e3a6a', text='L05 - Fundo Preto da Tomada', icon_value=0, emboss=True, depress=False)
        op = split_05503.operator('sna.mover_uv_trimsheet_r05_67edf', text='R05', icon_value=0, emboss=True, depress=False)
        split_39BD7 = box_39B85.split(factor=0.5, align=False)
        split_39BD7.alert = False
        split_39BD7.enabled = True
        split_39BD7.active = True
        split_39BD7.use_property_split = False
        split_39BD7.use_property_decorate = False
        split_39BD7.scale_x = 1.0
        split_39BD7.scale_y = 1.0
        split_39BD7.alignment = 'Expand'.upper()
        split_39BD7.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        op = split_39BD7.operator('sna.mover_uv_trimsheet_l06_3ab1e', text='L06 - Fio Vermelho', icon_value=0, emboss=True, depress=False)
        op = split_39BD7.operator('sna.mover_uv_trimsheet_r06_0f232', text='R06', icon_value=0, emboss=True, depress=False)
        split_ED8EA = box_39B85.split(factor=0.5, align=False)
        split_ED8EA.alert = False
        split_ED8EA.enabled = True
        split_ED8EA.active = True
        split_ED8EA.use_property_split = False
        split_ED8EA.use_property_decorate = False
        split_ED8EA.scale_x = 1.0
        split_ED8EA.scale_y = 1.0
        split_ED8EA.alignment = 'Expand'.upper()
        split_ED8EA.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        op = split_ED8EA.operator('sna.mover_uv_trimsheet_l07_297c5', text='L07 - Fio Verde', icon_value=0, emboss=True, depress=False)
        op = split_ED8EA.operator('sna.mover_uv_trimsheet_r07_7165c', text='R07', icon_value=0, emboss=True, depress=False)
        split_F1B71 = box_39B85.split(factor=0.5, align=False)
        split_F1B71.alert = False
        split_F1B71.enabled = True
        split_F1B71.active = True
        split_F1B71.use_property_split = False
        split_F1B71.use_property_decorate = False
        split_F1B71.scale_x = 1.0
        split_F1B71.scale_y = 1.0
        split_F1B71.alignment = 'Expand'.upper()
        split_F1B71.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        op = split_F1B71.operator('sna.mover_uv_trimsheet_l08_6b5a4', text='L08 - Metal', icon_value=0, emboss=True, depress=False)
        op = split_F1B71.operator('sna.mover_uv_trimsheet_r08_a4e15', text='R08', icon_value=0, emboss=True, depress=False)
        split_6C27E = box_39B85.split(factor=0.5, align=False)
        split_6C27E.alert = False
        split_6C27E.enabled = True
        split_6C27E.active = True
        split_6C27E.use_property_split = False
        split_6C27E.use_property_decorate = False
        split_6C27E.scale_x = 1.0
        split_6C27E.scale_y = 1.0
        split_6C27E.alignment = 'Expand'.upper()
        split_6C27E.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        op = split_6C27E.operator('sna.mover_uv_trimsheet_l09_17fba', text='L09 - Louça', icon_value=0, emboss=True, depress=False)
        op = split_6C27E.operator('sna.mover_uv_trimsheet_r09_3d487', text='R09', icon_value=0, emboss=True, depress=False)
        split_EF68E = box_39B85.split(factor=0.5, align=False)
        split_EF68E.alert = False
        split_EF68E.enabled = True
        split_EF68E.active = True
        split_EF68E.use_property_split = False
        split_EF68E.use_property_decorate = False
        split_EF68E.scale_x = 1.0
        split_EF68E.scale_y = 1.0
        split_EF68E.alignment = 'Expand'.upper()
        split_EF68E.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        op = split_EF68E.operator('sna.mover_uv_trimsheet_l10_0ee3c', text='L10 - Cobre', icon_value=0, emboss=True, depress=False)
        op = split_EF68E.operator('sna.mover_uv_trimsheet_r10_bfffa', text='R10', icon_value=0, emboss=True, depress=False)
        split_5B6D4 = box_39B85.split(factor=0.5, align=False)
        split_5B6D4.alert = False
        split_5B6D4.enabled = True
        split_5B6D4.active = True
        split_5B6D4.use_property_split = False
        split_5B6D4.use_property_decorate = False
        split_5B6D4.scale_x = 1.0
        split_5B6D4.scale_y = 1.0
        split_5B6D4.alignment = 'Expand'.upper()
        split_5B6D4.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        op = split_5B6D4.operator('sna.mover_uv_trimsheet_l11_e6f1e', text='L11 - Dourado', icon_value=0, emboss=True, depress=False)
        op = split_5B6D4.operator('sna.mover_uv_trimsheet_r11_c9e05', text='R11', icon_value=0, emboss=True, depress=False)
        split_58968 = box_39B85.split(factor=0.5, align=False)
        split_58968.alert = False
        split_58968.enabled = True
        split_58968.active = True
        split_58968.use_property_split = False
        split_58968.use_property_decorate = False
        split_58968.scale_x = 1.0
        split_58968.scale_y = 1.0
        split_58968.alignment = 'Expand'.upper()
        split_58968.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        op = split_58968.operator('sna.mover_uv_trimsheet_l12_0bee2', text='L12 - Metal Preto', icon_value=0, emboss=True, depress=False)
        op = split_58968.operator('sna.mover_uv_trimsheet_r12_46ff2', text='R12', icon_value=0, emboss=True, depress=False)
        split_AF287 = box_39B85.split(factor=0.5, align=False)
        split_AF287.alert = False
        split_AF287.enabled = True
        split_AF287.active = True
        split_AF287.use_property_split = False
        split_AF287.use_property_decorate = False
        split_AF287.scale_x = 1.0
        split_AF287.scale_y = 1.0
        split_AF287.alignment = 'Expand'.upper()
        split_AF287.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        op = split_AF287.operator('sna.mover_uv_trimsheet_l13_139b9', text='L13', icon_value=0, emboss=True, depress=False)
        op = split_AF287.operator('sna.mover_uv_trimsheet_r13_e3dce', text='R13', icon_value=0, emboss=True, depress=False)
        split_29F51 = box_39B85.split(factor=0.5, align=False)
        split_29F51.alert = False
        split_29F51.enabled = True
        split_29F51.active = True
        split_29F51.use_property_split = False
        split_29F51.use_property_decorate = False
        split_29F51.scale_x = 1.0
        split_29F51.scale_y = 1.0
        split_29F51.alignment = 'Expand'.upper()
        split_29F51.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        op = split_29F51.operator('sna.mover_uv_trimsheet_l14_04e08', text='L14', icon_value=0, emboss=True, depress=False)
        op = split_29F51.operator('sna.mover_uv_trimsheet_r14_8b053', text='R14', icon_value=0, emboss=True, depress=False)
        split_02F01 = box_39B85.split(factor=0.5, align=False)
        split_02F01.alert = False
        split_02F01.enabled = True
        split_02F01.active = True
        split_02F01.use_property_split = False
        split_02F01.use_property_decorate = False
        split_02F01.scale_x = 1.0
        split_02F01.scale_y = 1.0
        split_02F01.alignment = 'Expand'.upper()
        split_02F01.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        op = split_02F01.operator('sna.mover_uv_trimsheet_l15_91ec6', text='L15', icon_value=0, emboss=True, depress=False)
        op = split_02F01.operator('sna.mover_uv_trimsheet_r15_9755d', text='R15', icon_value=0, emboss=True, depress=False)
        split_66A2A = box_39B85.split(factor=0.5, align=False)
        split_66A2A.alert = False
        split_66A2A.enabled = True
        split_66A2A.active = True
        split_66A2A.use_property_split = False
        split_66A2A.use_property_decorate = False
        split_66A2A.scale_x = 1.0
        split_66A2A.scale_y = 1.0
        split_66A2A.alignment = 'Expand'.upper()
        split_66A2A.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        op = split_66A2A.operator('sna.mover_uv_trimsheet_l16_17adf', text='L16', icon_value=0, emboss=True, depress=False)
        op = split_66A2A.operator('sna.mover_uv_trimsheet_r16_92da8', text='R16', icon_value=0, emboss=True, depress=False)


class SNA_OT_Mover_Uv_Trimsheet_L01_B67E0(bpy.types.Operator):
    bl_idname = "sna.mover_uv_trimsheet_l01_b67e0"
    bl_label = "Mover_UV_Trimsheet_L01"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):

        def start():
            moveFacesSelecionadasUV(0.006, 0.955)
        #----------------------------------------------------------------------------------------------------

        def moveFacesSelecionadasUV(posicaoX, posicaoY):
            bpy.ops.uv.smart_project()
            #size
            scale_length = 0.03
            scale_width = 0.03
            original_type = bpy.context.area.ui_type
            bpy.context.area.ui_type = 'UV'
            #bpy.ops.uv.select_all(action='SELECT')
            bpy.context.space_data.pivot_point = 'CURSOR'
            bpy.ops.transform.resize(value=(scale_length, scale_width, 1))
            bpy.context.area.ui_type = original_type
            #move
            original_area = bpy.context.area.type
            view_layer = bpy.context.view_layer
            # switch to the UV editor to perform transforms etc
            bpy.context.area.ui_type = 'UV'
            # move the selection
            bpy.ops.transform.translate(value=(posicaoX, posicaoY, 0.0), constraint_axis=(False, False, False))
            # return to the original mode where the script was run
            bpy.context.area.type = original_area
        start()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Mover_Uv_Trimsheet_L03_21Da0(bpy.types.Operator):
    bl_idname = "sna.mover_uv_trimsheet_l03_21da0"
    bl_label = "Mover_UV_Trimsheet_L03"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):

        def start():
            moveFacesSelecionadasUV(0.006, 0.955 - 0.125)
        #----------------------------------------------------------------------------------------------------

        def moveFacesSelecionadasUV(posicaoX, posicaoY):
            bpy.ops.uv.smart_project()
            #size
            scale_length = 0.03
            scale_width = 0.03
            original_type = bpy.context.area.ui_type
            bpy.context.area.ui_type = 'UV'
            #bpy.ops.uv.select_all(action='SELECT')
            bpy.context.space_data.pivot_point = 'CURSOR'
            bpy.ops.transform.resize(value=(scale_length, scale_width, 1))
            bpy.context.area.ui_type = original_type
            #move
            original_area = bpy.context.area.type
            view_layer = bpy.context.view_layer
            # switch to the UV editor to perform transforms etc
            bpy.context.area.ui_type = 'UV'
            # move the selection
            bpy.ops.transform.translate(value=(posicaoX, posicaoY, 0.0), constraint_axis=(False, False, False))
            # return to the original mode where the script was run
            bpy.context.area.type = original_area
        start()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Mover_Uv_Trimsheet_L14_04E08(bpy.types.Operator):
    bl_idname = "sna.mover_uv_trimsheet_l14_04e08"
    bl_label = "Mover_UV_Trimsheet_L14"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):

        def start():
            moveFacesSelecionadasUV(0.006, 0.955 - 0.824)
        #----------------------------------------------------------------------------------------------------

        def moveFacesSelecionadasUV(posicaoX, posicaoY):
            bpy.ops.uv.smart_project()
            #size
            scale_length = 0.03
            scale_width = 0.03
            original_type = bpy.context.area.ui_type
            bpy.context.area.ui_type = 'UV'
            #bpy.ops.uv.select_all(action='SELECT')
            bpy.context.space_data.pivot_point = 'CURSOR'
            bpy.ops.transform.resize(value=(scale_length, scale_width, 1))
            bpy.context.area.ui_type = original_type
            #move
            original_area = bpy.context.area.type
            view_layer = bpy.context.view_layer
            # switch to the UV editor to perform transforms etc
            bpy.context.area.ui_type = 'UV'
            # move the selection
            bpy.ops.transform.translate(value=(posicaoX, posicaoY, 0.0), constraint_axis=(False, False, False))
            # return to the original mode where the script was run
            bpy.context.area.type = original_area
        start()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Mover_Uv_Trimsheet_L07_297C5(bpy.types.Operator):
    bl_idname = "sna.mover_uv_trimsheet_l07_297c5"
    bl_label = "Mover_UV_Trimsheet_L07"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):

        def start():
            moveFacesSelecionadasUV(0.006, 0.955 - 0.375)
        #----------------------------------------------------------------------------------------------------

        def moveFacesSelecionadasUV(posicaoX, posicaoY):
            bpy.ops.uv.smart_project()
            #size
            scale_length = 0.03
            scale_width = 0.03
            original_type = bpy.context.area.ui_type
            bpy.context.area.ui_type = 'UV'
            #bpy.ops.uv.select_all(action='SELECT')
            bpy.context.space_data.pivot_point = 'CURSOR'
            bpy.ops.transform.resize(value=(scale_length, scale_width, 1))
            bpy.context.area.ui_type = original_type
            #move
            original_area = bpy.context.area.type
            view_layer = bpy.context.view_layer
            # switch to the UV editor to perform transforms etc
            bpy.context.area.ui_type = 'UV'
            # move the selection
            bpy.ops.transform.translate(value=(posicaoX, posicaoY, 0.0), constraint_axis=(False, False, False))
            # return to the original mode where the script was run
            bpy.context.area.type = original_area
        start()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Mover_Uv_Trimsheet_L09_17Fba(bpy.types.Operator):
    bl_idname = "sna.mover_uv_trimsheet_l09_17fba"
    bl_label = "Mover_UV_Trimsheet_L09"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):

        def start():
            moveFacesSelecionadasUV(0.006, 0.955 - 0.5)
        #----------------------------------------------------------------------------------------------------

        def moveFacesSelecionadasUV(posicaoX, posicaoY):
            bpy.ops.uv.smart_project()
            #size
            scale_length = 0.03
            scale_width = 0.03
            original_type = bpy.context.area.ui_type
            bpy.context.area.ui_type = 'UV'
            #bpy.ops.uv.select_all(action='SELECT')
            bpy.context.space_data.pivot_point = 'CURSOR'
            bpy.ops.transform.resize(value=(scale_length, scale_width, 1))
            bpy.context.area.ui_type = original_type
            #move
            original_area = bpy.context.area.type
            view_layer = bpy.context.view_layer
            # switch to the UV editor to perform transforms etc
            bpy.context.area.ui_type = 'UV'
            # move the selection
            bpy.ops.transform.translate(value=(posicaoX, posicaoY, 0.0), constraint_axis=(False, False, False))
            # return to the original mode where the script was run
            bpy.context.area.type = original_area
        start()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Mover_Uv_Trimsheet_L15_91Ec6(bpy.types.Operator):
    bl_idname = "sna.mover_uv_trimsheet_l15_91ec6"
    bl_label = "Mover_UV_Trimsheet_L15"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):

        def start():
            moveFacesSelecionadasUV(0.006, 0.955 - 0.885)
        #----------------------------------------------------------------------------------------------------

        def moveFacesSelecionadasUV(posicaoX, posicaoY):
            bpy.ops.uv.smart_project()
            #size
            scale_length = 0.03
            scale_width = 0.03
            original_type = bpy.context.area.ui_type
            bpy.context.area.ui_type = 'UV'
            #bpy.ops.uv.select_all(action='SELECT')
            bpy.context.space_data.pivot_point = 'CURSOR'
            bpy.ops.transform.resize(value=(scale_length, scale_width, 1))
            bpy.context.area.ui_type = original_type
            #move
            original_area = bpy.context.area.type
            view_layer = bpy.context.view_layer
            # switch to the UV editor to perform transforms etc
            bpy.context.area.ui_type = 'UV'
            # move the selection
            bpy.ops.transform.translate(value=(posicaoX, posicaoY, 0.0), constraint_axis=(False, False, False))
            # return to the original mode where the script was run
            bpy.context.area.type = original_area
        start()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Mover_Uv_Trimsheet_L10_0Ee3C(bpy.types.Operator):
    bl_idname = "sna.mover_uv_trimsheet_l10_0ee3c"
    bl_label = "Mover_UV_Trimsheet_L10"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):

        def start():
            moveFacesSelecionadasUV(0.006, 0.955 - 0.565)
        #----------------------------------------------------------------------------------------------------

        def moveFacesSelecionadasUV(posicaoX, posicaoY):
            bpy.ops.uv.smart_project()
            #size
            scale_length = 0.03
            scale_width = 0.03
            original_type = bpy.context.area.ui_type
            bpy.context.area.ui_type = 'UV'
            #bpy.ops.uv.select_all(action='SELECT')
            bpy.context.space_data.pivot_point = 'CURSOR'
            bpy.ops.transform.resize(value=(scale_length, scale_width, 1))
            bpy.context.area.ui_type = original_type
            #move
            original_area = bpy.context.area.type
            view_layer = bpy.context.view_layer
            # switch to the UV editor to perform transforms etc
            bpy.context.area.ui_type = 'UV'
            # move the selection
            bpy.ops.transform.translate(value=(posicaoX, posicaoY, 0.0), constraint_axis=(False, False, False))
            # return to the original mode where the script was run
            bpy.context.area.type = original_area
        start()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Mover_Uv_Trimsheet_L05_E3A6A(bpy.types.Operator):
    bl_idname = "sna.mover_uv_trimsheet_l05_e3a6a"
    bl_label = "Mover_UV_Trimsheet_L05"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):

        def start():
            moveFacesSelecionadasUV(0.006, 0.955 - 0.25)
        #----------------------------------------------------------------------------------------------------

        def moveFacesSelecionadasUV(posicaoX, posicaoY):
            bpy.ops.uv.smart_project()
            #size
            scale_length = 0.03
            scale_width = 0.03
            original_type = bpy.context.area.ui_type
            bpy.context.area.ui_type = 'UV'
            #bpy.ops.uv.select_all(action='SELECT')
            bpy.context.space_data.pivot_point = 'CURSOR'
            bpy.ops.transform.resize(value=(scale_length, scale_width, 1))
            bpy.context.area.ui_type = original_type
            #move
            original_area = bpy.context.area.type
            view_layer = bpy.context.view_layer
            # switch to the UV editor to perform transforms etc
            bpy.context.area.ui_type = 'UV'
            # move the selection
            bpy.ops.transform.translate(value=(posicaoX, posicaoY, 0.0), constraint_axis=(False, False, False))
            # return to the original mode where the script was run
            bpy.context.area.type = original_area
        start()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Mover_Uv_Trimsheet_L11_E6F1E(bpy.types.Operator):
    bl_idname = "sna.mover_uv_trimsheet_l11_e6f1e"
    bl_label = "Mover_UV_Trimsheet_L11"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):

        def start():
            moveFacesSelecionadasUV(0.006, 0.955 - 0.625)
        #----------------------------------------------------------------------------------------------------

        def moveFacesSelecionadasUV(posicaoX, posicaoY):
            bpy.ops.uv.smart_project()
            #size
            scale_length = 0.03
            scale_width = 0.03
            original_type = bpy.context.area.ui_type
            bpy.context.area.ui_type = 'UV'
            #bpy.ops.uv.select_all(action='SELECT')
            bpy.context.space_data.pivot_point = 'CURSOR'
            bpy.ops.transform.resize(value=(scale_length, scale_width, 1))
            bpy.context.area.ui_type = original_type
            #move
            original_area = bpy.context.area.type
            view_layer = bpy.context.view_layer
            # switch to the UV editor to perform transforms etc
            bpy.context.area.ui_type = 'UV'
            # move the selection
            bpy.ops.transform.translate(value=(posicaoX, posicaoY, 0.0), constraint_axis=(False, False, False))
            # return to the original mode where the script was run
            bpy.context.area.type = original_area
        start()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Mover_Uv_Trimsheet_L12_0Bee2(bpy.types.Operator):
    bl_idname = "sna.mover_uv_trimsheet_l12_0bee2"
    bl_label = "Mover_UV_Trimsheet_L12"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):

        def start():
            moveFacesSelecionadasUV(0.006, 0.955 - 0.69)
        #----------------------------------------------------------------------------------------------------

        def moveFacesSelecionadasUV(posicaoX, posicaoY):
            bpy.ops.uv.smart_project()
            #size
            scale_length = 0.03
            scale_width = 0.03
            original_type = bpy.context.area.ui_type
            bpy.context.area.ui_type = 'UV'
            #bpy.ops.uv.select_all(action='SELECT')
            bpy.context.space_data.pivot_point = 'CURSOR'
            bpy.ops.transform.resize(value=(scale_length, scale_width, 1))
            bpy.context.area.ui_type = original_type
            #move
            original_area = bpy.context.area.type
            view_layer = bpy.context.view_layer
            # switch to the UV editor to perform transforms etc
            bpy.context.area.ui_type = 'UV'
            # move the selection
            bpy.ops.transform.translate(value=(posicaoX, posicaoY, 0.0), constraint_axis=(False, False, False))
            # return to the original mode where the script was run
            bpy.context.area.type = original_area
        start()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Mover_Uv_Trimsheet_L02_56D52(bpy.types.Operator):
    bl_idname = "sna.mover_uv_trimsheet_l02_56d52"
    bl_label = "Mover_UV_Trimsheet_L02"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):

        def start():
            moveFacesSelecionadasUV(0.006, 0.955 - 0.055)
        #----------------------------------------------------------------------------------------------------

        def moveFacesSelecionadasUV(posicaoX, posicaoY):
            bpy.ops.uv.smart_project()
            #size
            scale_length = 0.03
            scale_width = 0.03
            original_type = bpy.context.area.ui_type
            bpy.context.area.ui_type = 'UV'
            #bpy.ops.uv.select_all(action='SELECT')
            bpy.context.space_data.pivot_point = 'CURSOR'
            bpy.ops.transform.resize(value=(scale_length, scale_width, 1))
            bpy.context.area.ui_type = original_type
            #move
            original_area = bpy.context.area.type
            view_layer = bpy.context.view_layer
            # switch to the UV editor to perform transforms etc
            bpy.context.area.ui_type = 'UV'
            # move the selection
            bpy.ops.transform.translate(value=(posicaoX, posicaoY, 0.0), constraint_axis=(False, False, False))
            # return to the original mode where the script was run
            bpy.context.area.type = original_area
        start()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Mover_Uv_Trimsheet_L16_17Adf(bpy.types.Operator):
    bl_idname = "sna.mover_uv_trimsheet_l16_17adf"
    bl_label = "Mover_UV_Trimsheet_L16"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):

        def start():
            moveFacesSelecionadasUV(0.006, 0.955 - 0.941)
        #----------------------------------------------------------------------------------------------------

        def moveFacesSelecionadasUV(posicaoX, posicaoY):
            bpy.ops.uv.smart_project()
            #size
            scale_length = 0.03
            scale_width = 0.03
            original_type = bpy.context.area.ui_type
            bpy.context.area.ui_type = 'UV'
            #bpy.ops.uv.select_all(action='SELECT')
            bpy.context.space_data.pivot_point = 'CURSOR'
            bpy.ops.transform.resize(value=(scale_length, scale_width, 1))
            bpy.context.area.ui_type = original_type
            #move
            original_area = bpy.context.area.type
            view_layer = bpy.context.view_layer
            # switch to the UV editor to perform transforms etc
            bpy.context.area.ui_type = 'UV'
            # move the selection
            bpy.ops.transform.translate(value=(posicaoX, posicaoY, 0.0), constraint_axis=(False, False, False))
            # return to the original mode where the script was run
            bpy.context.area.type = original_area
        start()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Mover_Uv_Trimsheet_L04_0D677(bpy.types.Operator):
    bl_idname = "sna.mover_uv_trimsheet_l04_0d677"
    bl_label = "Mover_UV_Trimsheet_L04"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):

        def start():
            moveFacesSelecionadasUV(0.006, 0.955 - 0.19)
        #----------------------------------------------------------------------------------------------------

        def moveFacesSelecionadasUV(posicaoX, posicaoY):
            bpy.ops.uv.smart_project()
            #size
            scale_length = 0.03
            scale_width = 0.03
            original_type = bpy.context.area.ui_type
            bpy.context.area.ui_type = 'UV'
            #bpy.ops.uv.select_all(action='SELECT')
            bpy.context.space_data.pivot_point = 'CURSOR'
            bpy.ops.transform.resize(value=(scale_length, scale_width, 1))
            bpy.context.area.ui_type = original_type
            #move
            original_area = bpy.context.area.type
            view_layer = bpy.context.view_layer
            # switch to the UV editor to perform transforms etc
            bpy.context.area.ui_type = 'UV'
            # move the selection
            bpy.ops.transform.translate(value=(posicaoX, posicaoY, 0.0), constraint_axis=(False, False, False))
            # return to the original mode where the script was run
            bpy.context.area.type = original_area
        start()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Mover_Uv_Trimsheet_L06_3Ab1E(bpy.types.Operator):
    bl_idname = "sna.mover_uv_trimsheet_l06_3ab1e"
    bl_label = "Mover_UV_Trimsheet_L06"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):

        def start():
            moveFacesSelecionadasUV(0.006, 0.955 - 0.314)
        #----------------------------------------------------------------------------------------------------

        def moveFacesSelecionadasUV(posicaoX, posicaoY):
            bpy.ops.uv.smart_project()
            #size
            scale_length = 0.03
            scale_width = 0.03
            original_type = bpy.context.area.ui_type
            bpy.context.area.ui_type = 'UV'
            #bpy.ops.uv.select_all(action='SELECT')
            bpy.context.space_data.pivot_point = 'CURSOR'
            bpy.ops.transform.resize(value=(scale_length, scale_width, 1))
            bpy.context.area.ui_type = original_type
            #move
            original_area = bpy.context.area.type
            view_layer = bpy.context.view_layer
            # switch to the UV editor to perform transforms etc
            bpy.context.area.ui_type = 'UV'
            # move the selection
            bpy.ops.transform.translate(value=(posicaoX, posicaoY, 0.0), constraint_axis=(False, False, False))
            # return to the original mode where the script was run
            bpy.context.area.type = original_area
        start()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Mover_Uv_Trimsheet_L08_6B5A4(bpy.types.Operator):
    bl_idname = "sna.mover_uv_trimsheet_l08_6b5a4"
    bl_label = "Mover_UV_Trimsheet_L08"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):

        def start():
            moveFacesSelecionadasUV(0.006, 0.955 - 0.44)
        #----------------------------------------------------------------------------------------------------

        def moveFacesSelecionadasUV(posicaoX, posicaoY):
            bpy.ops.uv.smart_project()
            #size
            scale_length = 0.03
            scale_width = 0.03
            original_type = bpy.context.area.ui_type
            bpy.context.area.ui_type = 'UV'
            #bpy.ops.uv.select_all(action='SELECT')
            bpy.context.space_data.pivot_point = 'CURSOR'
            bpy.ops.transform.resize(value=(scale_length, scale_width, 1))
            bpy.context.area.ui_type = original_type
            #move
            original_area = bpy.context.area.type
            view_layer = bpy.context.view_layer
            # switch to the UV editor to perform transforms etc
            bpy.context.area.ui_type = 'UV'
            # move the selection
            bpy.ops.transform.translate(value=(posicaoX, posicaoY, 0.0), constraint_axis=(False, False, False))
            # return to the original mode where the script was run
            bpy.context.area.type = original_area
        start()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Mover_Uv_Trimsheet_L13_139B9(bpy.types.Operator):
    bl_idname = "sna.mover_uv_trimsheet_l13_139b9"
    bl_label = "Mover_UV_Trimsheet_L13"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):

        def start():
            moveFacesSelecionadasUV(0.006, 0.955 - 0.755)
        #----------------------------------------------------------------------------------------------------

        def moveFacesSelecionadasUV(posicaoX, posicaoY):
            bpy.ops.uv.smart_project()
            #size
            scale_length = 0.03
            scale_width = 0.03
            original_type = bpy.context.area.ui_type
            bpy.context.area.ui_type = 'UV'
            #bpy.ops.uv.select_all(action='SELECT')
            bpy.context.space_data.pivot_point = 'CURSOR'
            bpy.ops.transform.resize(value=(scale_length, scale_width, 1))
            bpy.context.area.ui_type = original_type
            #move
            original_area = bpy.context.area.type
            view_layer = bpy.context.view_layer
            # switch to the UV editor to perform transforms etc
            bpy.context.area.ui_type = 'UV'
            # move the selection
            bpy.ops.transform.translate(value=(posicaoX, posicaoY, 0.0), constraint_axis=(False, False, False))
            # return to the original mode where the script was run
            bpy.context.area.type = original_area
        start()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Mover_Uv_Trimsheet_R08_A4E15(bpy.types.Operator):
    bl_idname = "sna.mover_uv_trimsheet_r08_a4e15"
    bl_label = "Mover_UV_Trimsheet_R08"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):

        def start():
            moveFacesSelecionadasUV(0.965, 0.955 - 0.44)
        #----------------------------------------------------------------------------------------------------

        def moveFacesSelecionadasUV(posicaoX, posicaoY):
            bpy.ops.uv.smart_project()
            #size
            scale_length = 0.03
            scale_width = 0.03
            original_type = bpy.context.area.ui_type
            bpy.context.area.ui_type = 'UV'
            #bpy.ops.uv.select_all(action='SELECT')
            bpy.context.space_data.pivot_point = 'CURSOR'
            bpy.ops.transform.resize(value=(scale_length, scale_width, 1))
            bpy.context.area.ui_type = original_type
            #move
            original_area = bpy.context.area.type
            view_layer = bpy.context.view_layer
            # switch to the UV editor to perform transforms etc
            bpy.context.area.ui_type = 'UV'
            # move the selection
            bpy.ops.transform.translate(value=(posicaoX, posicaoY, 0.0), constraint_axis=(False, False, False))
            # return to the original mode where the script was run
            bpy.context.area.type = original_area
        start()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Mover_Uv_Trimsheet_R05_67Edf(bpy.types.Operator):
    bl_idname = "sna.mover_uv_trimsheet_r05_67edf"
    bl_label = "Mover_UV_Trimsheet_R05"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):

        def start():
            moveFacesSelecionadasUV(0.965, 0.955 - 0.25)
        #----------------------------------------------------------------------------------------------------

        def moveFacesSelecionadasUV(posicaoX, posicaoY):
            bpy.ops.uv.smart_project()
            #size
            scale_length = 0.03
            scale_width = 0.03
            original_type = bpy.context.area.ui_type
            bpy.context.area.ui_type = 'UV'
            #bpy.ops.uv.select_all(action='SELECT')
            bpy.context.space_data.pivot_point = 'CURSOR'
            bpy.ops.transform.resize(value=(scale_length, scale_width, 1))
            bpy.context.area.ui_type = original_type
            #move
            original_area = bpy.context.area.type
            view_layer = bpy.context.view_layer
            # switch to the UV editor to perform transforms etc
            bpy.context.area.ui_type = 'UV'
            # move the selection
            bpy.ops.transform.translate(value=(posicaoX, posicaoY, 0.0), constraint_axis=(False, False, False))
            # return to the original mode where the script was run
            bpy.context.area.type = original_area
        start()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Mover_Uv_Trimsheet_R07_7165C(bpy.types.Operator):
    bl_idname = "sna.mover_uv_trimsheet_r07_7165c"
    bl_label = "Mover_UV_Trimsheet_R07"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):

        def start():
            moveFacesSelecionadasUV(0.965, 0.955 - 0.375)
        #----------------------------------------------------------------------------------------------------

        def moveFacesSelecionadasUV(posicaoX, posicaoY):
            bpy.ops.uv.smart_project()
            #size
            scale_length = 0.03
            scale_width = 0.03
            original_type = bpy.context.area.ui_type
            bpy.context.area.ui_type = 'UV'
            #bpy.ops.uv.select_all(action='SELECT')
            bpy.context.space_data.pivot_point = 'CURSOR'
            bpy.ops.transform.resize(value=(scale_length, scale_width, 1))
            bpy.context.area.ui_type = original_type
            #move
            original_area = bpy.context.area.type
            view_layer = bpy.context.view_layer
            # switch to the UV editor to perform transforms etc
            bpy.context.area.ui_type = 'UV'
            # move the selection
            bpy.ops.transform.translate(value=(posicaoX, posicaoY, 0.0), constraint_axis=(False, False, False))
            # return to the original mode where the script was run
            bpy.context.area.type = original_area
        start()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Mover_Uv_Trimsheet_R02_8Ad95(bpy.types.Operator):
    bl_idname = "sna.mover_uv_trimsheet_r02_8ad95"
    bl_label = "Mover_UV_Trimsheet_R02"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):

        def start():
            moveFacesSelecionadasUV(0.965, 0.955 - 0.055)
        #----------------------------------------------------------------------------------------------------

        def moveFacesSelecionadasUV(posicaoX, posicaoY):
            bpy.ops.uv.smart_project()
            #size
            scale_length = 0.03
            scale_width = 0.03
            original_type = bpy.context.area.ui_type
            bpy.context.area.ui_type = 'UV'
            #bpy.ops.uv.select_all(action='SELECT')
            bpy.context.space_data.pivot_point = 'CURSOR'
            bpy.ops.transform.resize(value=(scale_length, scale_width, 1))
            bpy.context.area.ui_type = original_type
            #move
            original_area = bpy.context.area.type
            view_layer = bpy.context.view_layer
            # switch to the UV editor to perform transforms etc
            bpy.context.area.ui_type = 'UV'
            # move the selection
            bpy.ops.transform.translate(value=(posicaoX, posicaoY, 0.0), constraint_axis=(False, False, False))
            # return to the original mode where the script was run
            bpy.context.area.type = original_area
        start()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Mover_Uv_Trimsheet_R04_7972E(bpy.types.Operator):
    bl_idname = "sna.mover_uv_trimsheet_r04_7972e"
    bl_label = "Mover_UV_Trimsheet_R04"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):

        def start():
            moveFacesSelecionadasUV(0.965, 0.955 - 0.19)
        #----------------------------------------------------------------------------------------------------

        def moveFacesSelecionadasUV(posicaoX, posicaoY):
            bpy.ops.uv.smart_project()
            #size
            scale_length = 0.03
            scale_width = 0.03
            original_type = bpy.context.area.ui_type
            bpy.context.area.ui_type = 'UV'
            #bpy.ops.uv.select_all(action='SELECT')
            bpy.context.space_data.pivot_point = 'CURSOR'
            bpy.ops.transform.resize(value=(scale_length, scale_width, 1))
            bpy.context.area.ui_type = original_type
            #move
            original_area = bpy.context.area.type
            view_layer = bpy.context.view_layer
            # switch to the UV editor to perform transforms etc
            bpy.context.area.ui_type = 'UV'
            # move the selection
            bpy.ops.transform.translate(value=(posicaoX, posicaoY, 0.0), constraint_axis=(False, False, False))
            # return to the original mode where the script was run
            bpy.context.area.type = original_area
        start()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Mover_Uv_Trimsheet_R06_0F232(bpy.types.Operator):
    bl_idname = "sna.mover_uv_trimsheet_r06_0f232"
    bl_label = "Mover_UV_Trimsheet_R06"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):

        def start():
            moveFacesSelecionadasUV(0.965, 0.955 - 0.314)
        #----------------------------------------------------------------------------------------------------

        def moveFacesSelecionadasUV(posicaoX, posicaoY):
            bpy.ops.uv.smart_project()
            #size
            scale_length = 0.03
            scale_width = 0.03
            original_type = bpy.context.area.ui_type
            bpy.context.area.ui_type = 'UV'
            #bpy.ops.uv.select_all(action='SELECT')
            bpy.context.space_data.pivot_point = 'CURSOR'
            bpy.ops.transform.resize(value=(scale_length, scale_width, 1))
            bpy.context.area.ui_type = original_type
            #move
            original_area = bpy.context.area.type
            view_layer = bpy.context.view_layer
            # switch to the UV editor to perform transforms etc
            bpy.context.area.ui_type = 'UV'
            # move the selection
            bpy.ops.transform.translate(value=(posicaoX, posicaoY, 0.0), constraint_axis=(False, False, False))
            # return to the original mode where the script was run
            bpy.context.area.type = original_area
        start()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Mover_Uv_Trimsheet_R01_67Ada(bpy.types.Operator):
    bl_idname = "sna.mover_uv_trimsheet_r01_67ada"
    bl_label = "Mover_UV_Trimsheet_R01"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):

        def start():
            moveFacesSelecionadasUV(0.965, 0.955)
        #----------------------------------------------------------------------------------------------------

        def moveFacesSelecionadasUV(posicaoX, posicaoY):
            bpy.ops.uv.smart_project()
            #size
            scale_length = 0.03
            scale_width = 0.03
            original_type = bpy.context.area.ui_type
            bpy.context.area.ui_type = 'UV'
            #bpy.ops.uv.select_all(action='SELECT')
            bpy.context.space_data.pivot_point = 'CURSOR'
            bpy.ops.transform.resize(value=(scale_length, scale_width, 1))
            bpy.context.area.ui_type = original_type
            #move
            original_area = bpy.context.area.type
            view_layer = bpy.context.view_layer
            # switch to the UV editor to perform transforms etc
            bpy.context.area.ui_type = 'UV'
            # move the selection
            bpy.ops.transform.translate(value=(posicaoX, posicaoY, 0.0), constraint_axis=(False, False, False))
            # return to the original mode where the script was run
            bpy.context.area.type = original_area
        start()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Mover_Uv_Trimsheet_R03_Ed672(bpy.types.Operator):
    bl_idname = "sna.mover_uv_trimsheet_r03_ed672"
    bl_label = "Mover_UV_Trimsheet_R03"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):

        def start():
            moveFacesSelecionadasUV(0.965, 0.955 - 0.125)
        #----------------------------------------------------------------------------------------------------

        def moveFacesSelecionadasUV(posicaoX, posicaoY):
            bpy.ops.uv.smart_project()
            #size
            scale_length = 0.03
            scale_width = 0.03
            original_type = bpy.context.area.ui_type
            bpy.context.area.ui_type = 'UV'
            #bpy.ops.uv.select_all(action='SELECT')
            bpy.context.space_data.pivot_point = 'CURSOR'
            bpy.ops.transform.resize(value=(scale_length, scale_width, 1))
            bpy.context.area.ui_type = original_type
            #move
            original_area = bpy.context.area.type
            view_layer = bpy.context.view_layer
            # switch to the UV editor to perform transforms etc
            bpy.context.area.ui_type = 'UV'
            # move the selection
            bpy.ops.transform.translate(value=(posicaoX, posicaoY, 0.0), constraint_axis=(False, False, False))
            # return to the original mode where the script was run
            bpy.context.area.type = original_area
        start()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Q40_60632(bpy.types.Operator):
    bl_idname = "sna.q40_60632"
    bl_label = "Q40"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Mover_Uv_Trimsheet_R16_92Da8(bpy.types.Operator):
    bl_idname = "sna.mover_uv_trimsheet_r16_92da8"
    bl_label = "Mover_UV_Trimsheet_R16"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):

        def start():
            moveFacesSelecionadasUV(0.965, 0.955 - 0.941)
        #----------------------------------------------------------------------------------------------------

        def moveFacesSelecionadasUV(posicaoX, posicaoY):
            bpy.ops.uv.smart_project()
            #size
            scale_length = 0.03
            scale_width = 0.03
            original_type = bpy.context.area.ui_type
            bpy.context.area.ui_type = 'UV'
            #bpy.ops.uv.select_all(action='SELECT')
            bpy.context.space_data.pivot_point = 'CURSOR'
            bpy.ops.transform.resize(value=(scale_length, scale_width, 1))
            bpy.context.area.ui_type = original_type
            #move
            original_area = bpy.context.area.type
            view_layer = bpy.context.view_layer
            # switch to the UV editor to perform transforms etc
            bpy.context.area.ui_type = 'UV'
            # move the selection
            bpy.ops.transform.translate(value=(posicaoX, posicaoY, 0.0), constraint_axis=(False, False, False))
            # return to the original mode where the script was run
            bpy.context.area.type = original_area
        start()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Q39_F2Beb(bpy.types.Operator):
    bl_idname = "sna.q39_f2beb"
    bl_label = "Q39"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Mover_Uv_Trimsheet_R14_8B053(bpy.types.Operator):
    bl_idname = "sna.mover_uv_trimsheet_r14_8b053"
    bl_label = "Mover_UV_Trimsheet_R14"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):

        def start():
            moveFacesSelecionadasUV(0.965, 0.955 - 0.824)
        #----------------------------------------------------------------------------------------------------

        def moveFacesSelecionadasUV(posicaoX, posicaoY):
            bpy.ops.uv.smart_project()
            #size
            scale_length = 0.03
            scale_width = 0.03
            original_type = bpy.context.area.ui_type
            bpy.context.area.ui_type = 'UV'
            #bpy.ops.uv.select_all(action='SELECT')
            bpy.context.space_data.pivot_point = 'CURSOR'
            bpy.ops.transform.resize(value=(scale_length, scale_width, 1))
            bpy.context.area.ui_type = original_type
            #move
            original_area = bpy.context.area.type
            view_layer = bpy.context.view_layer
            # switch to the UV editor to perform transforms etc
            bpy.context.area.ui_type = 'UV'
            # move the selection
            bpy.ops.transform.translate(value=(posicaoX, posicaoY, 0.0), constraint_axis=(False, False, False))
            # return to the original mode where the script was run
            bpy.context.area.type = original_area
        start()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Mover_Uv_Trimsheet_R13_E3Dce(bpy.types.Operator):
    bl_idname = "sna.mover_uv_trimsheet_r13_e3dce"
    bl_label = "Mover_UV_Trimsheet_R13"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):

        def start():
            moveFacesSelecionadasUV(0.965, 0.955 - 0.755)
        #----------------------------------------------------------------------------------------------------

        def moveFacesSelecionadasUV(posicaoX, posicaoY):
            bpy.ops.uv.smart_project()
            #size
            scale_length = 0.03
            scale_width = 0.03
            original_type = bpy.context.area.ui_type
            bpy.context.area.ui_type = 'UV'
            #bpy.ops.uv.select_all(action='SELECT')
            bpy.context.space_data.pivot_point = 'CURSOR'
            bpy.ops.transform.resize(value=(scale_length, scale_width, 1))
            bpy.context.area.ui_type = original_type
            #move
            original_area = bpy.context.area.type
            view_layer = bpy.context.view_layer
            # switch to the UV editor to perform transforms etc
            bpy.context.area.ui_type = 'UV'
            # move the selection
            bpy.ops.transform.translate(value=(posicaoX, posicaoY, 0.0), constraint_axis=(False, False, False))
            # return to the original mode where the script was run
            bpy.context.area.type = original_area
        start()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Mover_Uv_Trimsheet_R09_3D487(bpy.types.Operator):
    bl_idname = "sna.mover_uv_trimsheet_r09_3d487"
    bl_label = "Mover_UV_Trimsheet_R09"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):

        def start():
            moveFacesSelecionadasUV(0.965, 0.955 - 0.5)
        #----------------------------------------------------------------------------------------------------

        def moveFacesSelecionadasUV(posicaoX, posicaoY):
            bpy.ops.uv.smart_project()
            #size
            scale_length = 0.03
            scale_width = 0.03
            original_type = bpy.context.area.ui_type
            bpy.context.area.ui_type = 'UV'
            #bpy.ops.uv.select_all(action='SELECT')
            bpy.context.space_data.pivot_point = 'CURSOR'
            bpy.ops.transform.resize(value=(scale_length, scale_width, 1))
            bpy.context.area.ui_type = original_type
            #move
            original_area = bpy.context.area.type
            view_layer = bpy.context.view_layer
            # switch to the UV editor to perform transforms etc
            bpy.context.area.ui_type = 'UV'
            # move the selection
            bpy.ops.transform.translate(value=(posicaoX, posicaoY, 0.0), constraint_axis=(False, False, False))
            # return to the original mode where the script was run
            bpy.context.area.type = original_area
        start()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Mover_Uv_Trimsheet_R11_C9E05(bpy.types.Operator):
    bl_idname = "sna.mover_uv_trimsheet_r11_c9e05"
    bl_label = "Mover_UV_Trimsheet_R11"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):

        def start():
            moveFacesSelecionadasUV(0.965, 0.955 - 0.625)
        #----------------------------------------------------------------------------------------------------

        def moveFacesSelecionadasUV(posicaoX, posicaoY):
            bpy.ops.uv.smart_project()
            #size
            scale_length = 0.03
            scale_width = 0.03
            original_type = bpy.context.area.ui_type
            bpy.context.area.ui_type = 'UV'
            #bpy.ops.uv.select_all(action='SELECT')
            bpy.context.space_data.pivot_point = 'CURSOR'
            bpy.ops.transform.resize(value=(scale_length, scale_width, 1))
            bpy.context.area.ui_type = original_type
            #move
            original_area = bpy.context.area.type
            view_layer = bpy.context.view_layer
            # switch to the UV editor to perform transforms etc
            bpy.context.area.ui_type = 'UV'
            # move the selection
            bpy.ops.transform.translate(value=(posicaoX, posicaoY, 0.0), constraint_axis=(False, False, False))
            # return to the original mode where the script was run
            bpy.context.area.type = original_area
        start()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Mover_Uv_Trimsheet_R10_Bfffa(bpy.types.Operator):
    bl_idname = "sna.mover_uv_trimsheet_r10_bfffa"
    bl_label = "Mover_UV_Trimsheet_R10"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):

        def start():
            moveFacesSelecionadasUV(0.965, 0.955 - 0.565)
        #----------------------------------------------------------------------------------------------------

        def moveFacesSelecionadasUV(posicaoX, posicaoY):
            bpy.ops.uv.smart_project()
            #size
            scale_length = 0.03
            scale_width = 0.03
            original_type = bpy.context.area.ui_type
            bpy.context.area.ui_type = 'UV'
            #bpy.ops.uv.select_all(action='SELECT')
            bpy.context.space_data.pivot_point = 'CURSOR'
            bpy.ops.transform.resize(value=(scale_length, scale_width, 1))
            bpy.context.area.ui_type = original_type
            #move
            original_area = bpy.context.area.type
            view_layer = bpy.context.view_layer
            # switch to the UV editor to perform transforms etc
            bpy.context.area.ui_type = 'UV'
            # move the selection
            bpy.ops.transform.translate(value=(posicaoX, posicaoY, 0.0), constraint_axis=(False, False, False))
            # return to the original mode where the script was run
            bpy.context.area.type = original_area
        start()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Q38_Ee472(bpy.types.Operator):
    bl_idname = "sna.q38_ee472"
    bl_label = "Q38"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Q37_4E0A7(bpy.types.Operator):
    bl_idname = "sna.q37_4e0a7"
    bl_label = "Q37"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Mover_Uv_Trimsheet_R12_46Ff2(bpy.types.Operator):
    bl_idname = "sna.mover_uv_trimsheet_r12_46ff2"
    bl_label = "Mover_UV_Trimsheet_R12"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):

        def start():
            moveFacesSelecionadasUV(0.965, 0.955 - 0.69)
        #----------------------------------------------------------------------------------------------------

        def moveFacesSelecionadasUV(posicaoX, posicaoY):
            bpy.ops.uv.smart_project()
            #size
            scale_length = 0.03
            scale_width = 0.03
            original_type = bpy.context.area.ui_type
            bpy.context.area.ui_type = 'UV'
            #bpy.ops.uv.select_all(action='SELECT')
            bpy.context.space_data.pivot_point = 'CURSOR'
            bpy.ops.transform.resize(value=(scale_length, scale_width, 1))
            bpy.context.area.ui_type = original_type
            #move
            original_area = bpy.context.area.type
            view_layer = bpy.context.view_layer
            # switch to the UV editor to perform transforms etc
            bpy.context.area.ui_type = 'UV'
            # move the selection
            bpy.ops.transform.translate(value=(posicaoX, posicaoY, 0.0), constraint_axis=(False, False, False))
            # return to the original mode where the script was run
            bpy.context.area.type = original_area
        start()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Mover_Uv_Trimsheet_R15_9755D(bpy.types.Operator):
    bl_idname = "sna.mover_uv_trimsheet_r15_9755d"
    bl_label = "Mover_UV_Trimsheet_R15"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):

        def start():
            moveFacesSelecionadasUV(0.965, 0.955 - 0.885)
        #----------------------------------------------------------------------------------------------------

        def moveFacesSelecionadasUV(posicaoX, posicaoY):
            bpy.ops.uv.smart_project()
            #size
            scale_length = 0.03
            scale_width = 0.03
            original_type = bpy.context.area.ui_type
            bpy.context.area.ui_type = 'UV'
            #bpy.ops.uv.select_all(action='SELECT')
            bpy.context.space_data.pivot_point = 'CURSOR'
            bpy.ops.transform.resize(value=(scale_length, scale_width, 1))
            bpy.context.area.ui_type = original_type
            #move
            original_area = bpy.context.area.type
            view_layer = bpy.context.view_layer
            # switch to the UV editor to perform transforms etc
            bpy.context.area.ui_type = 'UV'
            # move the selection
            bpy.ops.transform.translate(value=(posicaoX, posicaoY, 0.0), constraint_axis=(False, False, False))
            # return to the original mode where the script was run
            bpy.context.area.type = original_area
        start()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_PT_SAVE_TIME_1AD22(bpy.types.Panel):
    bl_label = 'Save TIme'
    bl_idname = 'SNA_PT_SAVE_TIME_1AD22'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_category = 'Save TIme'
    bl_order = 0
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not ((not 'OBJECT'==bpy.context.mode))

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout


class SNA_OT_Limpa_Arquivo_Bbe06(bpy.types.Operator):
    bl_idname = "sna.limpa_arquivo_bbe06"
    bl_label = "Limpa_Arquivo"
    bl_description = "Limpa o arquivo e remove materiasi nao usados dos Objetos Selecionados"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        ObjetosSelecionados = selected_objects()
        for obj in ObjetosSelecionados:
            if obj.type == 'MESH':        
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.material_slot_remove_unused()
        i = int(0)   
        while i < 20:    
            bpy.ops.outliner.orphans_purge(do_recursive=True)
            i = i + 1
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Reload_Imagem_Dc99C(bpy.types.Operator):
    bl_idname = "sna.reload_imagem_dc99c"
    bl_label = "Reload_Imagem"
    bl_description = "Reload_Imagem"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        #a = active_object()
        #m = a.active_material
        #nodes = get_nodes(m)
        #for n in nodes:
        #    if n.image is not None:
                #bpy.ops.node.nw_reload_images()
        #        bpy.ops.mesh.primitive_monkey_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        for image in bpy.data.images:
            image.reload()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_PT_SAVE_NODES_8FD37(bpy.types.Panel):
    bl_label = 'Save nodes?'
    bl_idname = 'SNA_PT_SAVE_NODES_8FD37'
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_context = ''
    bl_category = 'Save TIme'
    bl_order = 0
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        op = layout.operator('sna.reload_imagem_dc99c', text='Reload_Imagem', icon_value=0, emboss=True, depress=False)


class SNA_OT_Coloca_Chunk_A0C20(bpy.types.Operator):
    bl_idname = "sna.coloca_chunk_a0c20"
    bl_label = "Coloca_Chunk"
    bl_description = "Aops colocar o Chunk no primeiro objeto, ele renomeia todos selecionados"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        ObjetosSelecionados = selected_objects()
        unidade = int(0)
        dezena = int(0)
        cont = int(0)
        key = True
        for obj in ObjetosSelecionados:
            if obj.type == 'MESH':
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.view_layer.objects.active = obj
                if(key):
                    nome = obj.name
                    nome = nome.split('_')
                    key = False
                    for nomes in nome:
                        cont = cont + 1
                obj.name = obj.name + '_' + str(nome[cont - 1])
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Renomeia_Table_6111C(bpy.types.Operator):
    bl_idname = "sna.renomeia_table_6111c"
    bl_label = "Renomeia_Table"
    bl_description = "Mesa"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        #Renomeia Malha com Nome do Objeto
        ObjetosSelecionados = selected_objects()
        unidade = int(0)
        dezena = int(0)
        for obj in ObjetosSelecionados:
            if obj.type == 'MESH':
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.view_layer.objects.active = obj
                unidade = unidade + int(1)
                if(unidade > 9):
                    unidade = int(0)
                    dezena = dezena + int(1)
                bpy.context.view_layer.objects.active.name = 'Table_' + str(dezena) + str(unidade)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Renomeia_Wall_D0Dbc(bpy.types.Operator):
    bl_idname = "sna.renomeia_wall_d0dbc"
    bl_label = "Renomeia_Wall"
    bl_description = "Paredes"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        #Renomeia Malha com Nome do Objeto
        ObjetosSelecionados = selected_objects()
        unidade = int(0)
        dezena = int(0)
        for obj in ObjetosSelecionados:
            if obj.type == 'MESH':
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.view_layer.objects.active = obj
                unidade = unidade + int(1)
                if(unidade > 9):
                    unidade = int(0)
                    dezena = dezena + int(1)
                bpy.context.view_layer.objects.active.name = 'Wall_' + str(dezena) + str(unidade)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Renomeia_Window_15328(bpy.types.Operator):
    bl_idname = "sna.renomeia_window_15328"
    bl_label = "Renomeia_Window"
    bl_description = "Esquadrias"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        #Renomeia Malha com Nome do Objeto
        ObjetosSelecionados = selected_objects()
        unidade = int(0)
        dezena = int(0)
        for obj in ObjetosSelecionados:
            if obj.type == 'MESH':
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.view_layer.objects.active = obj
                unidade = unidade + int(1)
                if(unidade > 9):
                    unidade = int(0)
                    dezena = dezena + int(1)
                bpy.context.view_layer.objects.active.name = 'Window_' + str(dezena) + str(unidade)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Renomeia_Roof_64D62(bpy.types.Operator):
    bl_idname = "sna.renomeia_roof_64d62"
    bl_label = "Renomeia_Roof"
    bl_description = "Teto"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        #Renomeia Malha com Nome do Objeto
        ObjetosSelecionados = selected_objects()
        unidade = int(0)
        dezena = int(0)
        for obj in ObjetosSelecionados:
            if obj.type == 'MESH':
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.view_layer.objects.active = obj
                unidade = unidade + int(1)
                if(unidade > 9):
                    unidade = int(0)
                    dezena = dezena + int(1)
                bpy.context.view_layer.objects.active.name = 'Roof_' + str(dezena) + str(unidade)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Renomeia_Ceiling_B7712(bpy.types.Operator):
    bl_idname = "sna.renomeia_ceiling_b7712"
    bl_label = "Renomeia_Ceiling"
    bl_description = "Forro"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        #Renomeia Malha com Nome do Objeto
        ObjetosSelecionados = selected_objects()
        unidade = int(0)
        dezena = int(0)
        for obj in ObjetosSelecionados:
            if obj.type == 'MESH':
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.view_layer.objects.active = obj
                unidade = unidade + int(1)
                if(unidade > 9):
                    unidade = int(0)
                    dezena = dezena + int(1)
                bpy.context.view_layer.objects.active.name = ' Ceiling_' + str(dezena) + str(unidade)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Renomeia_Floor_Cb301(bpy.types.Operator):
    bl_idname = "sna.renomeia_floor_cb301"
    bl_label = "Renomeia_Floor"
    bl_description = "Piso"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        #Renomeia Malha com Nome do Objeto
        ObjetosSelecionados = selected_objects()
        unidade = int(0)
        dezena = int(0)
        for obj in ObjetosSelecionados:
            if obj.type == 'MESH':
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.view_layer.objects.active = obj
                unidade = unidade + int(1)
                if(unidade > 9):
                    unidade = int(0)
                    dezena = dezena + int(1)
                bpy.context.view_layer.objects.active.name = 'Floor_' + str(dezena) + str(unidade)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Renomeia_Sill_D7349(bpy.types.Operator):
    bl_idname = "sna.renomeia_sill_d7349"
    bl_label = "Renomeia_Sill"
    bl_description = "Baguete, soleira e filete"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        #Renomeia Malha com Nome do Objeto
        ObjetosSelecionados = selected_objects()
        unidade = int(0)
        dezena = int(0)
        for obj in ObjetosSelecionados:
            if obj.type == 'MESH':
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.view_layer.objects.active = obj
                unidade = unidade + int(1)
                if(unidade > 9):
                    unidade = int(0)
                    dezena = dezena + int(1)
                bpy.context.view_layer.objects.active.name = 'Sill_' + str(dezena) + str(unidade)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Renomeia_Baseboard_83Ae7(bpy.types.Operator):
    bl_idname = "sna.renomeia_baseboard_83ae7"
    bl_label = "Renomeia_Baseboard"
    bl_description = "Roda pé"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        #Renomeia Malha com Nome do Objeto
        ObjetosSelecionados = selected_objects()
        unidade = int(0)
        dezena = int(0)
        for obj in ObjetosSelecionados:
            if obj.type == 'MESH':
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.view_layer.objects.active = obj
                unidade = unidade + int(1)
                if(unidade > 9):
                    unidade = int(0)
                    dezena = dezena + int(1)
                bpy.context.view_layer.objects.active.name = 'Baseboard_' + str(dezena) + str(unidade)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Renomeia_Sink_0288A(bpy.types.Operator):
    bl_idname = "sna.renomeia_sink_0288a"
    bl_label = "Renomeia_Sink"
    bl_description = "Pia"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        #Renomeia Malha com Nome do Objeto
        ObjetosSelecionados = selected_objects()
        unidade = int(0)
        dezena = int(0)
        for obj in ObjetosSelecionados:
            if obj.type == 'MESH':
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.view_layer.objects.active = obj
                unidade = unidade + int(1)
                if(unidade > 9):
                    unidade = int(0)
                    dezena = dezena + int(1)
                bpy.context.view_layer.objects.active.name = 'Sink_' + str(dezena) + str(unidade)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Renomeia_Hydraulicwall_064Aa(bpy.types.Operator):
    bl_idname = "sna.renomeia_hydraulicwall_064aa"
    bl_label = "Renomeia_HydraulicWall"
    bl_description = "Parede Hidraulica"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        #Renomeia Malha com Nome do Objeto
        ObjetosSelecionados = selected_objects()
        unidade = int(0)
        dezena = int(0)
        for obj in ObjetosSelecionados:
            if obj.type == 'MESH':
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.view_layer.objects.active = obj
                unidade = unidade + int(1)
                if(unidade > 9):
                    unidade = int(0)
                    dezena = dezena + int(1)
                bpy.context.view_layer.objects.active.name = 'HydraulicWall_' + str(dezena) + str(unidade)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Renomeia_Shaft_Bc7F6(bpy.types.Operator):
    bl_idname = "sna.renomeia_shaft_bc7f6"
    bl_label = "Renomeia_Shaft"
    bl_description = "Shaft"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        #Renomeia Malha com Nome do Objeto
        ObjetosSelecionados = selected_objects()
        unidade = int(0)
        dezena = int(0)
        for obj in ObjetosSelecionados:
            if obj.type == 'MESH':
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.view_layer.objects.active = obj
                unidade = unidade + int(1)
                if(unidade > 9):
                    unidade = int(0)
                    dezena = dezena + int(1)
                bpy.context.view_layer.objects.active.name = 'Shaft_' + str(dezena) + str(unidade)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Renomeia_Wardrobe_70217(bpy.types.Operator):
    bl_idname = "sna.renomeia_wardrobe_70217"
    bl_label = "Renomeia_Wardrobe"
    bl_description = "Guarda Roupa"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        #Renomeia Malha com Nome do Objeto
        ObjetosSelecionados = selected_objects()
        unidade = int(0)
        dezena = int(0)
        for obj in ObjetosSelecionados:
            if obj.type == 'MESH':
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.view_layer.objects.active = obj
                unidade = unidade + int(1)
                if(unidade > 9):
                    unidade = int(0)
                    dezena = dezena + int(1)
                bpy.context.view_layer.objects.active.name = 'Wardrobe_' + str(dezena) + str(unidade)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Renomeia_Cabinet_3A3C4(bpy.types.Operator):
    bl_idname = "sna.renomeia_cabinet_3a3c4"
    bl_label = "Renomeia_Cabinet"
    bl_description = "Armario"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        #Renomeia Malha com Nome do Objeto
        ObjetosSelecionados = selected_objects()
        unidade = int(0)
        dezena = int(0)
        for obj in ObjetosSelecionados:
            if obj.type == 'MESH':
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.view_layer.objects.active = obj
                unidade = unidade + int(1)
                if(unidade > 9):
                    unidade = int(0)
                    dezena = dezena + int(1)
                bpy.context.view_layer.objects.active.name = 'Cabinet_' + str(dezena) + str(unidade)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Renomeia_Panel_A918E(bpy.types.Operator):
    bl_idname = "sna.renomeia_panel_a918e"
    bl_label = "Renomeia_Panel"
    bl_description = "Painel"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        #Renomeia Malha com Nome do Objeto
        ObjetosSelecionados = selected_objects()
        unidade = int(0)
        dezena = int(0)
        for obj in ObjetosSelecionados:
            if obj.type == 'MESH':
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.view_layer.objects.active = obj
                unidade = unidade + int(1)
                if(unidade > 9):
                    unidade = int(0)
                    dezena = dezena + int(1)
                bpy.context.view_layer.objects.active.name = 'Panel_' + str(dezena) + str(unidade)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Muda_Nome_Por_Objeto_285B3(bpy.types.Operator):
    bl_idname = "sna.muda_nome_por_objeto_285b3"
    bl_label = "Muda_nome_por_objeto"
    bl_description = "Material com o Nome do Objeto"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        #Cria Material com o Nome do Objeto
        ObjetosSelecionados = selected_objects()
        for obj in ObjetosSelecionados:
            if obj.type == 'MESH':       
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.view_layer.objects.active = obj 
                name = 'M' + '_' + str(obj.name)       
                materialExist = obj.active_material
                materialExist.name = name
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Material_Para_Trimsheet_B7602(bpy.types.Operator):
    bl_idname = "sna.material_para_trimsheet_b7602"
    bl_label = "Material_Para_TrimSheet"
    bl_description = "Cria um Material para TrimSheet e linka em todos os objetos"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        #Cria um Material para TrimSheet e linka em todos os objetos
        ObjetosSelecionados = selected_objects()
        m = create_material('M_FinishKit')
        m.use_nodes = True
        nodes = get_nodes(m)
        bsdf = get_node(nodes, 'Principled BSDF')
        #Mix = create_node(nodes , 'ShaderNodeMixRGB')
        #bpy.data.materials[m.name].node_tree.nodes["Mix"].blend_type = 'MULTIPLY'
        #Mix.location.x = -200
        #Mix.location.y = 220
        #create_node_link(Mix.outputs[0], bsdf.inputs[0])
        SeparateColor = create_node(nodes , 'ShaderNodeSeparateColor')
        SeparateColor.location.x = -400
        SeparateColor.location.y = 0
        create_node_link(SeparateColor.outputs[0], bsdf.inputs[6])
        create_node_link(SeparateColor.outputs[1], bsdf.inputs[9])
        create_node_link(SeparateColor.outputs[2], bsdf.inputs[19])
        NormalMap = create_node(nodes , 'ShaderNodeNormalMap')
        NormalMap.location.x = -200
        NormalMap.location.y = -260
        create_node_link(NormalMap.outputs[0], bsdf.inputs[22])
        for obj in ObjetosSelecionados:
            if obj.type == 'MESH':
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.view_layer.objects.active = obj
                bpy.context.object.data.materials.clear()
                add_material_to_object(obj, m)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Material_Por_Objeto_A0A37(bpy.types.Operator):
    bl_idname = "sna.material_por_objeto_a0a37"
    bl_label = "Material_Por_Objeto"
    bl_description = "Cria Material com o Nome do Objeto"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        #Cria Material com o Nome do Objeto
        ObjetosSelecionados = selected_objects()
        for obj in ObjetosSelecionados:
            if obj.type == 'MESH':
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.view_layer.objects.active = obj
                bpy.context.object.data.materials.clear()
                m = create_material('M_' + obj.name)
                m.use_nodes = True
                nodes = get_nodes(m)
                bsdf = get_node(nodes, 'Principled BSDF')
                #Mix = create_node(nodes , 'ShaderNodeMixRGB')
                #bpy.data.materials[m.name].node_tree.nodes["Mix"].blend_type = 'MULTIPLY'
                #Mix.location.x = -200
                #Mix.location.y = 220
                #create_node_link(Mix.outputs[0], bsdf.inputs[0])
                SeparateColor = create_node(nodes , 'ShaderNodeSeparateColor')
                SeparateColor.location.x = -400
                SeparateColor.location.y = 0
                create_node_link(SeparateColor.outputs[0], bsdf.inputs[6])
                create_node_link(SeparateColor.outputs[1], bsdf.inputs[9])
                #create_node_link(SeparateColor.outputs[2], Mix.inputs[2])
                NormalMap = create_node(nodes , 'ShaderNodeNormalMap')
                NormalMap.location.x = -200
                NormalMap.location.y = -260
                create_node_link(NormalMap.outputs[0], bsdf.inputs[22])
                add_material_to_object(obj, m)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Muda_Nome_Material_Mi_Dac18(bpy.types.Operator):
    bl_idname = "sna.muda_nome_material_mi_dac18"
    bl_label = "Muda_Nome_Material_MI"
    bl_description = "Renomeia materiais ja existentes para MI_Chunk_Nome"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        #Cria Material com o Nome do Objeto
        ObjetosSelecionados = selected_objects()
        for obj in ObjetosSelecionados:
            if obj.type == 'MESH':
                nomeSplit = obj.name.split('_')
                cont = int(0)
                for name in nomeSplit:
                    cont = cont + 1
                cont2 = int(0)
                name = ''    
                for montaName in nomeSplit:            
                    if (cont2 == 0):
                        name = 'MI' + '_' + str(nomeSplit[cont - 1])
                        cont2 = cont2 + 1                
                    else:                
                        name = name + '_' + str(nomeSplit[cont2 - 1])
                        cont2 = cont2 + 1
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.view_layer.objects.active = obj        
                materialExist = obj.active_material
                materialExist.name = name
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Material_Instanced_Por_Objeto_De044(bpy.types.Operator):
    bl_idname = "sna.material_instanced_por_objeto_de044"
    bl_label = "Material_Instanced_Por_Objeto"
    bl_description = "Cria material com MI_Chunk_Nome"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        #Cria Material com o Nome do Objeto
        ObjetosSelecionados = selected_objects()
        for obj in ObjetosSelecionados:
            if obj.type == 'MESH':
                nomeSplit = obj.name.split('_')
                cont = int(0)
                for name in nomeSplit:
                    cont = cont + 1
                cont2 = int(0)
                name = ''    
                for montaName in nomeSplit:            
                    if (cont2 == 0):
                        name = 'MI' + '_' + str(nomeSplit[cont - 1])
                        cont2 = cont2 + 1                
                    else:                
                        name = name + '_' + str(nomeSplit[cont2 - 1])
                        cont2 = cont2 + 1
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.view_layer.objects.active = obj
                bpy.context.object.data.materials.clear()
                m = create_material(name)        
                m.use_nodes = True
                nodes = get_nodes(m)
                bsdf = get_node(nodes, 'Principled BSDF')
                #Mix = create_node(nodes , 'ShaderNodeMixRGB')
                #bpy.data.materials[m.name].node_tree.nodes["Mix"].blend_type = 'MULTIPLY'
                #Mix.location.x = -200
                #Mix.location.y = 220
                #create_node_link(Mix.outputs[0], bsdf.inputs[0])
                SeparateColor = create_node(nodes , 'ShaderNodeSeparateColor')
                SeparateColor.location.x = -400
                SeparateColor.location.y = 0
                create_node_link(SeparateColor.outputs[0], bsdf.inputs[6])
                create_node_link(SeparateColor.outputs[1], bsdf.inputs[9])
                NormalMap = create_node(nodes , 'ShaderNodeNormalMap')
                NormalMap.location.x = -200
                NormalMap.location.y = -260
                create_node_link(NormalMap.outputs[0], bsdf.inputs[22])
                add_material_to_object(obj, m)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Acha_Material_Dfb8E(bpy.types.Operator):
    bl_idname = "sna.acha_material_dfb8e"
    bl_label = "Acha_Material"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        objetosSelecionados = selected_objects()
        for obj in objetosSelecionados:
            if obj.type == 'MESH':
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.view_layer.objects.active = obj
                materialDoObjeto = get_material(obj)
                nomeCorreto = bpy.context.active_object.active_material.name
                remove_material_from_object(obj, nomeCorreto)
                nomeCorreto = nomeCorreto.split('.')
                todosMateriais = get_all_materials()
                for m in todosMateriais:
                    if(nomeCorreto[0] == m.name):
                        add_material_to_object(obj, m)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Auto_Uv_Lm_02E0A(bpy.types.Operator):
    bl_idname = "sna.auto_uv_lm_02e0a"
    bl_label = "Auto_UV_LM"
    bl_description = "Deleta canais de UVs. Cria 'UV' e 'LM' e abre eles"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):

        def start():
            objetosSelecionados = selected_objects()
            deletaUVs(objetosSelecionados)
            criaCanalUV(objetosSelecionados, 'UV')    
            abreCanalUV(objetosSelecionados, 'UV')
            criaCanalUV(objetosSelecionados, 'LM')
            abreCanalUV(objetosSelecionados, 'LM')
        #----------------------------------------------------------------------------------------------------

        def deletaUVs(objetos):
            for obj in objetos:
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.view_layer.objects.active = obj
                objetoAtivo = bpy.context.active_object
                while objetoAtivo.data.uv_layers:
                    objetoAtivo.data.uv_layers.remove(obj.data.uv_layers[0])
        #----------------------------------------------------------------------------------------------------

        def criaCanalUV(objetos, nomeCanal):
            for obj in objetos:        
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.view_layer.objects.active = obj
                bpy.ops.mesh.uv_texture_add()   
                bpy.context.object.data.uv_layers["UVMap"].name = nomeCanal
        #----------------------------------------------------------------------------------------------------

        def abreCanalUV(objetos, nomeCanal):
            for obj in objetos:        
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.view_layer.objects.active = obj       
                if (nomeCanal == 'UV'):
                    packUV(obj, 4, 2, 1024)
                elif(nomeCanal == 'LM'):
                    packUV(obj, 8, 4, 512)
        #----------------------------------------------------------------------------------------------------

        def packUV(objeto, margin, padding, texSize):
            if bpy.context.object.mode != 'EDIT':
                set_edit_mode(objeto)
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.uv.select_all(action='SELECT')
            bpy.ops.uv.cube_project(cube_size=2)
            bpy.context.scene.uvp2_props.pixel_margin = margin
            bpy.context.scene.uvp2_props.pixel_padding = padding
            bpy.context.scene.uvp2_props.pixel_margin_tex_size = texSize
            bpy.ops.uv.average_islands_scale()
            bpy.ops.uvpackmaster2.uv_pack()       
            set_object_mode(objeto)
        start()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Transforma_Lm_Em_Uv_Ebaf2(bpy.types.Operator):
    bl_idname = "sna.transforma_lm_em_uv_ebaf2"
    bl_label = "Transforma_LM_em_UV"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):

        def start():
            objetosSelecionados = selected_objects()
            deletaCanalUV(objetosSelecionados, 'UV')
            nomeiaPrimeiroCanalDeUV(objetosSelecionados, 'UV')
            criaCanal(objetosSelecionados, 'LM')
            abreCanalUV(objetosSelecionados, 'LM')
        #----------------------------------------------------------------------------------------------------

        def deletaCanalUV(objetos, nomeCanal):
            for obj in objetos:        
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.view_layer.objects.active = obj
                uv_layers = obj.data.uv_layers
                key = False
                for uv_layer in uv_layers:
                    if uv_layer.name == nomeCanal:
                        uv_layer.active = True
                        key = True
                        break       
                if (key):
                    bpy.ops.mesh.uv_texture_remove()
        #----------------------------------------------------------------------------------------------------

        def nomeiaPrimeiroCanalDeUV(objetos, nomeCanal):
            for obj in objetos:        
                    bpy.ops.object.select_all(action='DESELECT')
                    bpy.context.view_layer.objects.active = obj
                    if len(bpy.context.object.data.uv_layers) > 0:
                        bpy.context.object.data.uv_layers[0].name = "UV"
        #----------------------------------------------------------------------------------------------------

        def criaCanal(objetos, nomeCanal):
            for obj in objetos:        
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.view_layer.objects.active = obj
                bpy.ops.mesh.uv_texture_add()   
                bpy.context.object.data.uv_layers["UVMap"].name = nomeCanal
        #----------------------------------------------------------------------------------------------------

        def abreCanalUV(objetos, nomeCanal):
            for obj in objetos:        
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.view_layer.objects.active = obj       
                if(nomeCanal == 'LM'):
                    packUV(obj, 8, 4, 512)
        #----------------------------------------------------------------------------------------------------            

        def packUV(objeto, margin, padding, texSize):
            if bpy.context.object.mode != 'EDIT':
                set_edit_mode(objeto)
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.uv.select_all(action='SELECT')
            bpy.ops.uv.cube_project(cube_size=2)
            bpy.context.scene.uvp2_props.pixel_margin = margin
            bpy.context.scene.uvp2_props.pixel_padding = padding
            bpy.context.scene.uvp2_props.pixel_margin_tex_size = texSize
            bpy.ops.uv.average_islands_scale()
            bpy.ops.uv.pack_islands()
            bpy.ops.uvpackmaster2.uv_pack()       
            set_object_mode(objeto)
        start()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Mostra_Objetos_Com_Uvs_Erradas_35A54(bpy.types.Operator):
    bl_idname = "sna.mostra_objetos_com_uvs_erradas_35a54"
    bl_label = "mostra_Objetos_Com_UVs_erradas"
    bl_description = "Mostra objetos que nao possuem 2 UVs ou nomeados errados"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):

        def start():
            select_all_objects()
            objetosSelecionados = selected_objects()
            mostraObjetosUVErrada(objetosSelecionados)
        #----------------------------------------------------------------------------------------------------

        def mostraObjetosUVErrada(objetos):
            for obj in objetos:        
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.view_layer.objects.active = obj
                key = False
                if len(bpy.context.object.data.uv_layers) == 2 and bpy.context.object.data.uv_layers[0].name == 'UV' and bpy.context.object.data.uv_layers[1].name == 'LM':
                    key = True
                if key:
                    hide(obj)
        start()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Seleciona_Canal_Uv_7Fe59(bpy.types.Operator):
    bl_idname = "sna.seleciona_canal_uv_7fe59"
    bl_label = "Seleciona_Canal_'UV'"
    bl_description = "Seleciona o canal De 'UV'"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):

        def start():
            objetosSelecionados = selected_objects()
            selecionaCanalUV(objetosSelecionados, 'UV')
        #----------------------------------------------------------------------------------------------------

        def selecionaCanalUV(objetos, nomeCanal):
            for obj in objetos:
                if obj.type == 'MESH':
                    uv_layers = obj.data.uv_layers        
                    for uv_layer in uv_layers:
                        if uv_layer.name == nomeCanal:
                            uv_layer.active = True
        start()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Seleciona_Canal_Lm_99223(bpy.types.Operator):
    bl_idname = "sna.seleciona_canal_lm_99223"
    bl_label = "Seleciona_Canal_'LM'"
    bl_description = "Seleciona o canal De 'LM'"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):

        def start():
            objetosSelecionados = selected_objects()
            selecionaCanalUV(objetosSelecionados, 'LM')
        #----------------------------------------------------------------------------------------------------

        def selecionaCanalUV(objetos, nomeCanal):
            for obj in objetos:
                if obj.type == 'MESH':
                    uv_layers = obj.data.uv_layers        
                    for uv_layer in uv_layers:
                        if uv_layer.name == nomeCanal:
                            uv_layer.active = True
        start()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Flipa_Uv_9A7B0(bpy.types.Operator):
    bl_idname = "sna.flipa_uv_9a7b0"
    bl_label = "Flipa_UV"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_PT_OBJECT_MANIPULATION_BF548(bpy.types.Panel):
    bl_label = 'Object Manipulation'
    bl_idname = 'SNA_PT_OBJECT_MANIPULATION_BF548'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_order = 0
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = 'SNA_PT_SAVE_TIME_1AD22'
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        op = layout.operator('sna.applyall_b0bb8', text='Apply All', icon_value=0, emboss=True, depress=False)
        op = layout.operator('sna.clear_parent_6a9dc', text='Clear_Parent', icon_value=0, emboss=True, depress=False)
        op = layout.operator('sna.limpa_arquivo_bbe06', text='Limpa_Arquivo', icon_value=0, emboss=True, depress=False)


class SNA_PT_MESH_MANIPULATION_C9978(bpy.types.Panel):
    bl_label = 'Mesh Manipulation'
    bl_idname = 'SNA_PT_MESH_MANIPULATION_C9978'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_order = 1
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = 'SNA_PT_SAVE_TIME_1AD22'
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        op = layout.operator('sna.limpa_mesh_8d290', text='Limpa_Mesh', icon_value=_icons['photo_2022-02-27_19-24-38.jpg'].icon_id, emboss=True, depress=False)
        op = layout.operator('sna.renomeia_malha_7f608', text='Renomeia_Malha', icon_value=0, emboss=True, depress=False)


class SNA_PT_RENAME_OBJECTS_0B636(bpy.types.Panel):
    bl_label = 'Rename Objects'
    bl_idname = 'SNA_PT_RENAME_OBJECTS_0B636'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_order = 4
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = 'SNA_PT_SAVE_TIME_1AD22'
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        split_2593F = layout.split(factor=0.5, align=False)
        split_2593F.alert = False
        split_2593F.enabled = True
        split_2593F.active = True
        split_2593F.use_property_split = False
        split_2593F.use_property_decorate = False
        split_2593F.scale_x = 1.0
        split_2593F.scale_y = 1.0
        split_2593F.alignment = 'Expand'.upper()
        split_2593F.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        op = split_2593F.operator('sna.renomeia_wall_d0dbc', text='Wall', icon_value=0, emboss=True, depress=False)
        op = split_2593F.operator('sna.renomeia_window_15328', text='Window', icon_value=0, emboss=True, depress=False)
        split_142DB = layout.split(factor=0.5, align=False)
        split_142DB.alert = False
        split_142DB.enabled = True
        split_142DB.active = True
        split_142DB.use_property_split = False
        split_142DB.use_property_decorate = False
        split_142DB.scale_x = 1.0
        split_142DB.scale_y = 1.0
        split_142DB.alignment = 'Expand'.upper()
        split_142DB.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        op = split_142DB.operator('sna.renomeia_roof_64d62', text='Roof', icon_value=0, emboss=True, depress=False)
        op = split_142DB.operator('sna.renomeia_ceiling_b7712', text='Ceiling', icon_value=0, emboss=True, depress=False)
        split_C272E = layout.split(factor=0.5, align=False)
        split_C272E.alert = False
        split_C272E.enabled = True
        split_C272E.active = True
        split_C272E.use_property_split = False
        split_C272E.use_property_decorate = False
        split_C272E.scale_x = 1.0
        split_C272E.scale_y = 1.0
        split_C272E.alignment = 'Expand'.upper()
        split_C272E.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        op = split_C272E.operator('sna.renomeia_floor_cb301', text='Floor', icon_value=0, emboss=True, depress=False)
        op = split_C272E.operator('sna.renomeia_sill_d7349', text='Sill', icon_value=0, emboss=True, depress=False)
        split_E87CF = layout.split(factor=0.5, align=False)
        split_E87CF.alert = False
        split_E87CF.enabled = True
        split_E87CF.active = True
        split_E87CF.use_property_split = False
        split_E87CF.use_property_decorate = False
        split_E87CF.scale_x = 1.0
        split_E87CF.scale_y = 1.0
        split_E87CF.alignment = 'Expand'.upper()
        split_E87CF.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        op = split_E87CF.operator('sna.renomeia_baseboard_83ae7', text='Baseboard', icon_value=0, emboss=True, depress=False)
        op = split_E87CF.operator('sna.renomeia_sink_0288a', text='Sink', icon_value=0, emboss=True, depress=False)
        split_02AF1 = layout.split(factor=0.5, align=False)
        split_02AF1.alert = False
        split_02AF1.enabled = True
        split_02AF1.active = True
        split_02AF1.use_property_split = False
        split_02AF1.use_property_decorate = False
        split_02AF1.scale_x = 1.0
        split_02AF1.scale_y = 1.0
        split_02AF1.alignment = 'Expand'.upper()
        split_02AF1.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        op = split_02AF1.operator('sna.renomeia_hydraulicwall_064aa', text='HydraulicWall', icon_value=0, emboss=True, depress=False)
        op = split_02AF1.operator('sna.renomeia_shaft_bc7f6', text='Shaft', icon_value=0, emboss=True, depress=False)
        split_462E3 = layout.split(factor=0.5, align=False)
        split_462E3.alert = False
        split_462E3.enabled = True
        split_462E3.active = True
        split_462E3.use_property_split = False
        split_462E3.use_property_decorate = False
        split_462E3.scale_x = 1.0
        split_462E3.scale_y = 1.0
        split_462E3.alignment = 'Expand'.upper()
        split_462E3.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        op = split_462E3.operator('sna.renomeia_wardrobe_70217', text='Wardrobe', icon_value=0, emboss=True, depress=False)
        op = split_462E3.operator('sna.renomeia_cabinet_3a3c4', text='Cabinet', icon_value=0, emboss=True, depress=False)
        split_5B1FD = layout.split(factor=0.5, align=False)
        split_5B1FD.alert = False
        split_5B1FD.enabled = True
        split_5B1FD.active = True
        split_5B1FD.use_property_split = False
        split_5B1FD.use_property_decorate = False
        split_5B1FD.scale_x = 1.0
        split_5B1FD.scale_y = 1.0
        split_5B1FD.alignment = 'Expand'.upper()
        split_5B1FD.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        op = split_5B1FD.operator('sna.renomeia_table_6111c', text='Table', icon_value=0, emboss=True, depress=False)
        op = split_5B1FD.operator('sna.renomeia_panel_a918e', text='Panel', icon_value=0, emboss=True, depress=False)
        op = layout.operator('sna.coloca_chunk_a0c20', text='Sufix_Chunk', icon_value=0, emboss=True, depress=False)


class SNA_PT_MATERIAL_1F875(bpy.types.Panel):
    bl_label = 'Material'
    bl_idname = 'SNA_PT_MATERIAL_1F875'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_order = 3
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = 'SNA_PT_SAVE_TIME_1AD22'
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        op = layout.operator('sna.auto_material_9714f', text='Auto_Material', icon_value=0, emboss=True, depress=False)
        op = layout.operator('sna.corrige_undefinednode_de0bc', text='corrige_UndefinedNode', icon_value=0, emboss=True, depress=False)
        layout.label(text='MI_Chunk_Name', icon_value=0)
        box_3DA8C = layout.box()
        box_3DA8C.alert = False
        box_3DA8C.enabled = True
        box_3DA8C.active = True
        box_3DA8C.use_property_split = False
        box_3DA8C.use_property_decorate = False
        box_3DA8C.alignment = 'Expand'.upper()
        box_3DA8C.scale_x = 1.0
        box_3DA8C.scale_y = 1.0
        box_3DA8C.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        op = box_3DA8C.operator('sna.material_instanced_por_objeto_de044', text='Material_Instanced_Por_Objeto', icon_value=0, emboss=True, depress=False)
        op = box_3DA8C.operator('sna.muda_nome_material_mi_dac18', text='Muda_Nome_Material_Instanced', icon_value=0, emboss=True, depress=False)
        layout.label(text='M_Name', icon_value=0)
        box_BA1F8 = layout.box()
        box_BA1F8.alert = False
        box_BA1F8.enabled = True
        box_BA1F8.active = True
        box_BA1F8.use_property_split = False
        box_BA1F8.use_property_decorate = False
        box_BA1F8.alignment = 'Expand'.upper()
        box_BA1F8.scale_x = 1.0
        box_BA1F8.scale_y = 1.0
        box_BA1F8.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        op = box_BA1F8.operator('sna.material_por_objeto_a0a37', text='Material_Por_Objeto', icon_value=0, emboss=True, depress=False)
        op = box_BA1F8.operator('sna.muda_nome_por_objeto_285b3', text='Muda_nome_por_objeto', icon_value=0, emboss=True, depress=False)
        layout.label(text='M_FinishKit', icon_value=0)
        box_CF34E = layout.box()
        box_CF34E.alert = False
        box_CF34E.enabled = True
        box_CF34E.active = True
        box_CF34E.use_property_split = False
        box_CF34E.use_property_decorate = False
        box_CF34E.alignment = 'Expand'.upper()
        box_CF34E.scale_x = 1.0
        box_CF34E.scale_y = 1.0
        box_CF34E.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        op = box_CF34E.operator('sna.material_para_trimsheet_b7602', text='Material_Para_TrimSheet', icon_value=0, emboss=True, depress=False)


class SNA_PT_UV_MANIPULATION_6FA05(bpy.types.Panel):
    bl_label = 'UV manipulation'
    bl_idname = 'SNA_PT_UV_MANIPULATION_6FA05'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_order = 2
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = 'SNA_PT_SAVE_TIME_1AD22'
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        op = layout.operator('sna.auto_uv_lm_02e0a', text='Auto_UV_LM', icon_value=0, emboss=True, depress=False)
        op = layout.operator('sna.transforma_lm_em_uv_ebaf2', text='Transforma_LM_em_UV', icon_value=0, emboss=True, depress=False)
        op = layout.operator('sna.mostra_objetos_com_uvs_erradas_35a54', text='mostra_Objetos_Com_UVs_erradas', icon_value=0, emboss=True, depress=False)
        op = layout.operator('sna.seleciona_canal_uv_7fe59', text="Seleciona_Canal_'UV'", icon_value=0, emboss=True, depress=False)
        op = layout.operator('sna.seleciona_canal_lm_99223', text="Seleciona_Canal_'LM'", icon_value=0, emboss=True, depress=False)
        op = layout.operator('sna.flipa_uv_9a7b0', text='Flipa_UV', icon_value=0, emboss=True, depress=False)


class SNA_PT_MAYA_TO_BLENDER_4B69C(bpy.types.Panel):
    bl_label = 'Maya to Blender'
    bl_idname = 'SNA_PT_MAYA_TO_BLENDER_4B69C'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_order = 5
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = 'SNA_PT_SAVE_TIME_1AD22'
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        op = layout.operator('sna.acha_material_dfb8e', text='Acha_Material', icon_value=0, emboss=True, depress=False)


def register():
    global _icons
    _icons = bpy.utils.previews.new()
    bpy.utils.register_class(SNA_OT_Auto_Material_9714F)
    bpy.utils.register_class(SNA_OT_Corrige_Undefinednode_De0Bc)
    bpy.utils.register_class(SNA_OT_Limpa_Mesh_8D290)
    bpy.utils.register_class(SNA_OT_Renomeia_Malha_7F608)
    bpy.utils.register_class(SNA_OT_Clear_Parent_6A9Dc)
    bpy.utils.register_class(SNA_OT_Applyall_B0Bb8)
    bpy.utils.register_class(SNA_PT_TRIMSHEET_UV_MANIPULATION_6912C)
    bpy.utils.register_class(SNA_OT_Mover_Uv_Trimsheet_L01_B67E0)
    bpy.utils.register_class(SNA_OT_Mover_Uv_Trimsheet_L03_21Da0)
    bpy.utils.register_class(SNA_OT_Mover_Uv_Trimsheet_L14_04E08)
    bpy.utils.register_class(SNA_OT_Mover_Uv_Trimsheet_L07_297C5)
    bpy.utils.register_class(SNA_OT_Mover_Uv_Trimsheet_L09_17Fba)
    bpy.utils.register_class(SNA_OT_Mover_Uv_Trimsheet_L15_91Ec6)
    bpy.utils.register_class(SNA_OT_Mover_Uv_Trimsheet_L10_0Ee3C)
    bpy.utils.register_class(SNA_OT_Mover_Uv_Trimsheet_L05_E3A6A)
    bpy.utils.register_class(SNA_OT_Mover_Uv_Trimsheet_L11_E6F1E)
    bpy.utils.register_class(SNA_OT_Mover_Uv_Trimsheet_L12_0Bee2)
    bpy.utils.register_class(SNA_OT_Mover_Uv_Trimsheet_L02_56D52)
    bpy.utils.register_class(SNA_OT_Mover_Uv_Trimsheet_L16_17Adf)
    bpy.utils.register_class(SNA_OT_Mover_Uv_Trimsheet_L04_0D677)
    bpy.utils.register_class(SNA_OT_Mover_Uv_Trimsheet_L06_3Ab1E)
    bpy.utils.register_class(SNA_OT_Mover_Uv_Trimsheet_L08_6B5A4)
    bpy.utils.register_class(SNA_OT_Mover_Uv_Trimsheet_L13_139B9)
    bpy.utils.register_class(SNA_OT_Mover_Uv_Trimsheet_R08_A4E15)
    bpy.utils.register_class(SNA_OT_Mover_Uv_Trimsheet_R05_67Edf)
    bpy.utils.register_class(SNA_OT_Mover_Uv_Trimsheet_R07_7165C)
    bpy.utils.register_class(SNA_OT_Mover_Uv_Trimsheet_R02_8Ad95)
    bpy.utils.register_class(SNA_OT_Mover_Uv_Trimsheet_R04_7972E)
    bpy.utils.register_class(SNA_OT_Mover_Uv_Trimsheet_R06_0F232)
    bpy.utils.register_class(SNA_OT_Mover_Uv_Trimsheet_R01_67Ada)
    bpy.utils.register_class(SNA_OT_Mover_Uv_Trimsheet_R03_Ed672)
    bpy.utils.register_class(SNA_OT_Q40_60632)
    bpy.utils.register_class(SNA_OT_Mover_Uv_Trimsheet_R16_92Da8)
    bpy.utils.register_class(SNA_OT_Q39_F2Beb)
    bpy.utils.register_class(SNA_OT_Mover_Uv_Trimsheet_R14_8B053)
    bpy.utils.register_class(SNA_OT_Mover_Uv_Trimsheet_R13_E3Dce)
    bpy.utils.register_class(SNA_OT_Mover_Uv_Trimsheet_R09_3D487)
    bpy.utils.register_class(SNA_OT_Mover_Uv_Trimsheet_R11_C9E05)
    bpy.utils.register_class(SNA_OT_Mover_Uv_Trimsheet_R10_Bfffa)
    bpy.utils.register_class(SNA_OT_Q38_Ee472)
    bpy.utils.register_class(SNA_OT_Q37_4E0A7)
    bpy.utils.register_class(SNA_OT_Mover_Uv_Trimsheet_R12_46Ff2)
    bpy.utils.register_class(SNA_OT_Mover_Uv_Trimsheet_R15_9755D)
    bpy.utils.register_class(SNA_PT_SAVE_TIME_1AD22)
    bpy.utils.register_class(SNA_OT_Limpa_Arquivo_Bbe06)
    bpy.utils.register_class(SNA_OT_Reload_Imagem_Dc99C)
    bpy.utils.register_class(SNA_PT_SAVE_NODES_8FD37)
    bpy.utils.register_class(SNA_OT_Coloca_Chunk_A0C20)
    bpy.utils.register_class(SNA_OT_Renomeia_Table_6111C)
    bpy.utils.register_class(SNA_OT_Renomeia_Wall_D0Dbc)
    bpy.utils.register_class(SNA_OT_Renomeia_Window_15328)
    bpy.utils.register_class(SNA_OT_Renomeia_Roof_64D62)
    bpy.utils.register_class(SNA_OT_Renomeia_Ceiling_B7712)
    bpy.utils.register_class(SNA_OT_Renomeia_Floor_Cb301)
    bpy.utils.register_class(SNA_OT_Renomeia_Sill_D7349)
    bpy.utils.register_class(SNA_OT_Renomeia_Baseboard_83Ae7)
    bpy.utils.register_class(SNA_OT_Renomeia_Sink_0288A)
    bpy.utils.register_class(SNA_OT_Renomeia_Hydraulicwall_064Aa)
    bpy.utils.register_class(SNA_OT_Renomeia_Shaft_Bc7F6)
    bpy.utils.register_class(SNA_OT_Renomeia_Wardrobe_70217)
    bpy.utils.register_class(SNA_OT_Renomeia_Cabinet_3A3C4)
    bpy.utils.register_class(SNA_OT_Renomeia_Panel_A918E)
    bpy.utils.register_class(SNA_OT_Muda_Nome_Por_Objeto_285B3)
    bpy.utils.register_class(SNA_OT_Material_Para_Trimsheet_B7602)
    bpy.utils.register_class(SNA_OT_Material_Por_Objeto_A0A37)
    bpy.utils.register_class(SNA_OT_Muda_Nome_Material_Mi_Dac18)
    bpy.utils.register_class(SNA_OT_Material_Instanced_Por_Objeto_De044)
    bpy.utils.register_class(SNA_OT_Acha_Material_Dfb8E)
    bpy.utils.register_class(SNA_OT_Auto_Uv_Lm_02E0A)
    bpy.utils.register_class(SNA_OT_Transforma_Lm_Em_Uv_Ebaf2)
    bpy.utils.register_class(SNA_OT_Mostra_Objetos_Com_Uvs_Erradas_35A54)
    bpy.utils.register_class(SNA_OT_Seleciona_Canal_Uv_7Fe59)
    bpy.utils.register_class(SNA_OT_Seleciona_Canal_Lm_99223)
    bpy.utils.register_class(SNA_OT_Flipa_Uv_9A7B0)
    bpy.utils.register_class(SNA_PT_OBJECT_MANIPULATION_BF548)
    bpy.utils.register_class(SNA_PT_MESH_MANIPULATION_C9978)
    if not 'photo_2022-02-27_19-24-38.jpg' in _icons: _icons.load('photo_2022-02-27_19-24-38.jpg', os.path.join(os.path.dirname(__file__), 'icons', 'photo_2022-02-27_19-24-38.jpg'), "IMAGE")
    bpy.utils.register_class(SNA_PT_RENAME_OBJECTS_0B636)
    bpy.utils.register_class(SNA_PT_MATERIAL_1F875)
    bpy.utils.register_class(SNA_PT_UV_MANIPULATION_6FA05)
    bpy.utils.register_class(SNA_PT_MAYA_TO_BLENDER_4B69C)


def unregister():
    global _icons
    bpy.utils.previews.remove(_icons)
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    for km, kmi in addon_keymaps.values():
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    bpy.utils.unregister_class(SNA_OT_Auto_Material_9714F)
    bpy.utils.unregister_class(SNA_OT_Corrige_Undefinednode_De0Bc)
    bpy.utils.unregister_class(SNA_OT_Limpa_Mesh_8D290)
    bpy.utils.unregister_class(SNA_OT_Renomeia_Malha_7F608)
    bpy.utils.unregister_class(SNA_OT_Clear_Parent_6A9Dc)
    bpy.utils.unregister_class(SNA_OT_Applyall_B0Bb8)
    bpy.utils.unregister_class(SNA_PT_TRIMSHEET_UV_MANIPULATION_6912C)
    bpy.utils.unregister_class(SNA_OT_Mover_Uv_Trimsheet_L01_B67E0)
    bpy.utils.unregister_class(SNA_OT_Mover_Uv_Trimsheet_L03_21Da0)
    bpy.utils.unregister_class(SNA_OT_Mover_Uv_Trimsheet_L14_04E08)
    bpy.utils.unregister_class(SNA_OT_Mover_Uv_Trimsheet_L07_297C5)
    bpy.utils.unregister_class(SNA_OT_Mover_Uv_Trimsheet_L09_17Fba)
    bpy.utils.unregister_class(SNA_OT_Mover_Uv_Trimsheet_L15_91Ec6)
    bpy.utils.unregister_class(SNA_OT_Mover_Uv_Trimsheet_L10_0Ee3C)
    bpy.utils.unregister_class(SNA_OT_Mover_Uv_Trimsheet_L05_E3A6A)
    bpy.utils.unregister_class(SNA_OT_Mover_Uv_Trimsheet_L11_E6F1E)
    bpy.utils.unregister_class(SNA_OT_Mover_Uv_Trimsheet_L12_0Bee2)
    bpy.utils.unregister_class(SNA_OT_Mover_Uv_Trimsheet_L02_56D52)
    bpy.utils.unregister_class(SNA_OT_Mover_Uv_Trimsheet_L16_17Adf)
    bpy.utils.unregister_class(SNA_OT_Mover_Uv_Trimsheet_L04_0D677)
    bpy.utils.unregister_class(SNA_OT_Mover_Uv_Trimsheet_L06_3Ab1E)
    bpy.utils.unregister_class(SNA_OT_Mover_Uv_Trimsheet_L08_6B5A4)
    bpy.utils.unregister_class(SNA_OT_Mover_Uv_Trimsheet_L13_139B9)
    bpy.utils.unregister_class(SNA_OT_Mover_Uv_Trimsheet_R08_A4E15)
    bpy.utils.unregister_class(SNA_OT_Mover_Uv_Trimsheet_R05_67Edf)
    bpy.utils.unregister_class(SNA_OT_Mover_Uv_Trimsheet_R07_7165C)
    bpy.utils.unregister_class(SNA_OT_Mover_Uv_Trimsheet_R02_8Ad95)
    bpy.utils.unregister_class(SNA_OT_Mover_Uv_Trimsheet_R04_7972E)
    bpy.utils.unregister_class(SNA_OT_Mover_Uv_Trimsheet_R06_0F232)
    bpy.utils.unregister_class(SNA_OT_Mover_Uv_Trimsheet_R01_67Ada)
    bpy.utils.unregister_class(SNA_OT_Mover_Uv_Trimsheet_R03_Ed672)
    bpy.utils.unregister_class(SNA_OT_Q40_60632)
    bpy.utils.unregister_class(SNA_OT_Mover_Uv_Trimsheet_R16_92Da8)
    bpy.utils.unregister_class(SNA_OT_Q39_F2Beb)
    bpy.utils.unregister_class(SNA_OT_Mover_Uv_Trimsheet_R14_8B053)
    bpy.utils.unregister_class(SNA_OT_Mover_Uv_Trimsheet_R13_E3Dce)
    bpy.utils.unregister_class(SNA_OT_Mover_Uv_Trimsheet_R09_3D487)
    bpy.utils.unregister_class(SNA_OT_Mover_Uv_Trimsheet_R11_C9E05)
    bpy.utils.unregister_class(SNA_OT_Mover_Uv_Trimsheet_R10_Bfffa)
    bpy.utils.unregister_class(SNA_OT_Q38_Ee472)
    bpy.utils.unregister_class(SNA_OT_Q37_4E0A7)
    bpy.utils.unregister_class(SNA_OT_Mover_Uv_Trimsheet_R12_46Ff2)
    bpy.utils.unregister_class(SNA_OT_Mover_Uv_Trimsheet_R15_9755D)
    bpy.utils.unregister_class(SNA_PT_SAVE_TIME_1AD22)
    bpy.utils.unregister_class(SNA_OT_Limpa_Arquivo_Bbe06)
    bpy.utils.unregister_class(SNA_OT_Reload_Imagem_Dc99C)
    bpy.utils.unregister_class(SNA_PT_SAVE_NODES_8FD37)
    bpy.utils.unregister_class(SNA_OT_Coloca_Chunk_A0C20)
    bpy.utils.unregister_class(SNA_OT_Renomeia_Table_6111C)
    bpy.utils.unregister_class(SNA_OT_Renomeia_Wall_D0Dbc)
    bpy.utils.unregister_class(SNA_OT_Renomeia_Window_15328)
    bpy.utils.unregister_class(SNA_OT_Renomeia_Roof_64D62)
    bpy.utils.unregister_class(SNA_OT_Renomeia_Ceiling_B7712)
    bpy.utils.unregister_class(SNA_OT_Renomeia_Floor_Cb301)
    bpy.utils.unregister_class(SNA_OT_Renomeia_Sill_D7349)
    bpy.utils.unregister_class(SNA_OT_Renomeia_Baseboard_83Ae7)
    bpy.utils.unregister_class(SNA_OT_Renomeia_Sink_0288A)
    bpy.utils.unregister_class(SNA_OT_Renomeia_Hydraulicwall_064Aa)
    bpy.utils.unregister_class(SNA_OT_Renomeia_Shaft_Bc7F6)
    bpy.utils.unregister_class(SNA_OT_Renomeia_Wardrobe_70217)
    bpy.utils.unregister_class(SNA_OT_Renomeia_Cabinet_3A3C4)
    bpy.utils.unregister_class(SNA_OT_Renomeia_Panel_A918E)
    bpy.utils.unregister_class(SNA_OT_Muda_Nome_Por_Objeto_285B3)
    bpy.utils.unregister_class(SNA_OT_Material_Para_Trimsheet_B7602)
    bpy.utils.unregister_class(SNA_OT_Material_Por_Objeto_A0A37)
    bpy.utils.unregister_class(SNA_OT_Muda_Nome_Material_Mi_Dac18)
    bpy.utils.unregister_class(SNA_OT_Material_Instanced_Por_Objeto_De044)
    bpy.utils.unregister_class(SNA_OT_Acha_Material_Dfb8E)
    bpy.utils.unregister_class(SNA_OT_Auto_Uv_Lm_02E0A)
    bpy.utils.unregister_class(SNA_OT_Transforma_Lm_Em_Uv_Ebaf2)
    bpy.utils.unregister_class(SNA_OT_Mostra_Objetos_Com_Uvs_Erradas_35A54)
    bpy.utils.unregister_class(SNA_OT_Seleciona_Canal_Uv_7Fe59)
    bpy.utils.unregister_class(SNA_OT_Seleciona_Canal_Lm_99223)
    bpy.utils.unregister_class(SNA_OT_Flipa_Uv_9A7B0)
    bpy.utils.unregister_class(SNA_PT_OBJECT_MANIPULATION_BF548)
    bpy.utils.unregister_class(SNA_PT_MESH_MANIPULATION_C9978)
    bpy.utils.unregister_class(SNA_PT_RENAME_OBJECTS_0B636)
    bpy.utils.unregister_class(SNA_PT_MATERIAL_1F875)
    bpy.utils.unregister_class(SNA_PT_UV_MANIPULATION_6FA05)
    bpy.utils.unregister_class(SNA_PT_MAYA_TO_BLENDER_4B69C)
