import bpy

def checkIfCollectionExists(collectionName):
    # Iterate through all collections
    for collection in bpy.data.collections:
        if collectionName == collection.name:
            print("collection already exists")
            return True
    return False

def createCollection(collectionName):
    if(checkIfCollectionExists(collectionName)==False): 
        bpy.ops.collection.create(name  = collectionName)
        bpy.context.scene.collection.children.link(bpy.data.collections[collectionName])
        
def DeleteAllViewLayers():
    for layer in bpy.context.scene.view_layers:
        if layer.name != 'Master':
            bpy.context.scene.view_layers.remove(layer)
            
def CheckIfViewLayerExists(viewLayerName):
    for layer in bpy.context.scene.view_layers:
            if layer.name == viewLayerName:
                #bpy.context.scene.view_layers.remove(layer)
                print("view layer already exists")
                return True
    return False
        
def CreateViewLayers(viewLayerName):
    if CheckIfViewLayerExists(viewLayerName) == False:
        newViewLayer = bpy.context.scene.view_layers.new(viewLayerName)
        
def SetCollectionIndirect(viewLayerName, collectionName, exclude =True):
    bpy.context.scene.view_layers[viewLayerName].layer_collection.children[collectionName].indirect_only = True
                    
def SetCollectionHoldout(viewLayerName, collectionName, exclude =True):
    # Iterate through all view layers
    for viewLayer in bpy.context.scene.view_layers:
        if viewLayer.name == viewLayerName:
            #Iterate over the collections on each view layer as pointer with layer_collection
            for layer_collection in viewLayer.layer_collection.children:
                #exclude means if all the remaining collections will be affected or only the selected
                if layer_collection.name == collectionName:
                    layer_collection.holdout = exclude
                else:
                    layer_collection.holdout = not exclude
                    
def SetCollectionInvisible(viewLayerName, collectionName):
    bpy.context.scene.view_layers[viewLayerName].layer_collection.children[collectionName].exclude = True
        
bpy.context.scene.render.engine = 'CYCLES'
outliner_area = next(a for a in bpy.context.screen.areas if a.type == "OUTLINER")

space = outliner_area.spaces[0]
space.show_restrict_column_holdout = True  # Holdout
space.show_restrict_column_indirect_only = True  # Indirect only

Master_vl = "Master"
FG_Geo_vl = "FG_Geo"
MG_Geo_vl = "MG_Geo"
BG_Geo_vl = "BG_Geo" 
FG_Vol_vl = "FG_Vol"
MG_Vol_vl = "MG_Vol"
BG_Vol_vl = "BG_Vol"

Camera_col = "Camera"
Lights_col = "Lights"
Instances_col = "Instances"
FG_Geo_col = "FG_Geo"
MG_Geo_col = "MG_Geo"
BG_Geo_col = "BG_Geo" 
Volume_col = "Volume"

createCollection(Camera_col)
createCollection(Lights_col)
createCollection(Instances_col)    
createCollection(FG_Geo_col)
createCollection(MG_Geo_col)
createCollection(BG_Geo_col)
createCollection(Volume_col)

CreateViewLayers(Master_vl)
DeleteAllViewLayers()
CreateViewLayers(FG_Geo_vl)
CreateViewLayers(MG_Geo_vl)
CreateViewLayers(BG_Geo_vl)

CreateViewLayers(FG_Vol_vl)
CreateViewLayers(MG_Vol_vl)
CreateViewLayers(BG_Vol_vl)


SetCollectionIndirect(FG_Geo_vl, MG_Geo_col)# INDIRECT
SetCollectionIndirect(FG_Geo_vl, BG_Geo_col)# INDIRECT
SetCollectionInvisible(FG_Geo_vl, Volume_col)# DISABLED
SetCollectionInvisible(FG_Geo_vl, Instances_col)# DISABLED

SetCollectionIndirect(MG_Geo_vl, FG_Geo_col)# INDIRECT
SetCollectionIndirect(MG_Geo_vl, BG_Geo_col)# INDIRECT
SetCollectionInvisible(MG_Geo_vl, Volume_col)# DISABLED
SetCollectionInvisible(MG_Geo_vl, Instances_col)# DISABLED

SetCollectionIndirect(BG_Geo_vl, FG_Geo_col)# INDIRECT
SetCollectionIndirect(BG_Geo_vl, MG_Geo_col)# INDIRECT
SetCollectionInvisible(BG_Geo_vl, Volume_col)# DISABLED
SetCollectionInvisible(BG_Geo_vl, Instances_col)# DISABLED

SetCollectionHoldout(FG_Vol_vl, FG_Geo_col)# HOLDOUT
SetCollectionIndirect(FG_Vol_vl, MG_Geo_col)# INDIRECT
SetCollectionIndirect(FG_Vol_vl, BG_Geo_col)# INDIRECT
SetCollectionInvisible(FG_Vol_vl, Instances_col)# DISABLED

SetCollectionIndirect(MG_Vol_vl, FG_Geo_col)# INDIRECT
SetCollectionHoldout(MG_Vol_vl, MG_Geo_col)# HOLDOUT
SetCollectionIndirect(MG_Vol_vl, BG_Geo_col)# INDIRECT
SetCollectionInvisible(MG_Vol_vl, Instances_col)# DISABLED

SetCollectionIndirect(BG_Vol_vl, FG_Geo_col)# INDIRECTl
SetCollectionIndirect(BG_Vol_vl, MG_Geo_col)# INDIRECT
SetCollectionHoldout(BG_Vol_vl, BG_Geo_col)# HOLDOUT
SetCollectionInvisible(BG_Vol_vl, Instances_col)# DISABLED