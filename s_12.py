import arcpy

arcpy.env.workspace = arcpy.GetParameterAsText(0)
arcpy.env.overwriteOutput = True
amenities = ['school', 'hospital', 'place_of_worship']
country = "El Salvador"
try:
    arcpy.CreateFileGDB_management(arcpy.env.workspace, 'S_12.gdb')
    arcpy.AddMessage("Create new FileGDB " + 'S_12.gdb')
    # Make a feature layer
    arcpy.MakeFeatureLayer_management('CentralAmerica.shp', 'SelectCountryLayer', '"NAME" ' + "'" + country + "'")
    arcpy.MakeFeatureLayer_management('OSMpoints.shp', 'SelectOSMpointsLayer', )
    arcpy.AddMessage("Create feature layer SelectCountryLayer, SelectOSMpointsLayer" )

    # Apply a selection
    arcpy.SelectLayerByLocation_management("SelectCountryLayer", "CONTAINS", "SelectOSMpointsLayer")
except:
    print arcpy.GetMessages()

for i in amenities:
    arcpy.SelectLayerByAttribute_management("SelectOSMpointsLayer", "ADD_TO_SELECTION", '"amenity" = ' + "'" + i + "'")
    # Copy the features to a new feature class and clean up
    arcpy.AddMessage("Create selection")
    arcpy.AddMessage("Create new feature layer FC" + i)
    arcpy.CopyFeatures_management("SelectOSMpointsLayer", arcpy.env.workspace + r'\S_12.gdb.' + '\\FC' + i)
    arcpy.AddField_management('S_12.gdb.' + '\\FC' + i, 'source', "TEXT")
    arcpy.AddMessage("Create new field 'source' in FC" + i)
    arcpy.AddField_management('S_12.gdb.' + '\\FC' + i, 'GID', "DOUBLE")
    arcpy.AddMessage("Create new field 'GID' in FC" + i)
    with arcpy.da.UpdateCursor('S_12.gdb.' + '\\FC' + i, ('source', 'GID', 'id')) as cursor:
        for row in cursor:
            row[0] = 'OpenStreetMap'
            row[1] = row[2]
            cursor.updateRow(row)
    arcpy.AddMessage("Update field in FC" + i)

# Clean up feature layers
arcpy.Delete_management("SelectOSMpointsLayer")
arcpy.Delete_management("SelectCountryLayer")
arcpy.AddMessage("Delete temporary layer")