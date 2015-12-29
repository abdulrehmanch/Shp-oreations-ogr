#!C:\Python34
# -*- coding: utf-8 -*-
# readShapeFile


import os
from osgeo import ogr

class Shapefile:
    def __init__(self, source_path = ''):

        self.daShapefile = source_path
        try:
            self.driver = ogr.GetDriverByName('ESRI Shapefile')
            self.dataSource = self.driver.Open(self.daShapefile, 1) # 0 means read-only. 1 means writeable.
        except:
            pass

    def featureCount(self):
        layer = self.dataSource.GetLayerByIndex(0)
        # layer = dataSource.GetLayer()
        featureCount = layer.GetFeatureCount()
        #print ("Number of features in %s: %d" % (os.path.basename(daShapefile),featureCount))

        lyrDefn = layer.GetLayerDefn()
        fcount = lyrDefn.GetFieldCount()
        #print ('Field count %s' % fcount)

        return featureCount
#-------------------------------------------------------------------------------
    def fields(self):
        # Getting fields..........................................
        layer = self.dataSource.GetLayerByIndex(0)
        lyrDefn = layer.GetLayerDefn()
        fcount = lyrDefn.GetFieldCount()
        Fields = []
        for i in range( fcount ):
            fieldName =  lyrDefn.GetFieldDefn(i).GetName()
            fieldTypeCode = lyrDefn.GetFieldDefn(i).GetType()
            fieldType = lyrDefn.GetFieldDefn(i).GetFieldTypeName(fieldTypeCode)
            fieldWidth = lyrDefn.GetFieldDefn(i).GetWidth()
            GetPrecision = lyrDefn.GetFieldDefn(i).GetPrecision()
            Fields.append(fieldName)
            #fields_value ['Field Name'] =  fieldName
        return Fields


            # print fieldName + " - " + fieldType+ " " + str(fieldWidth) + " " + str(GetPrecision)
            # print fieldName
#------------------------------------------------------------------------------
    def iterrating(self):
        # iterrating feature and DeleteFeature........................
        FeatureCount = self.featureCount()
        layer = self.dataSource.GetLayerByIndex(0)

        for i in range (FeatureCount):
            feature = layer[i]
            # print feature.GetField("DISTANCE")
            geom = feature.GetGeometryRef()
            geometry =  geom.Centroid().ExportToWkt()
            # print (geometry)
            if feature.GetField("DISTANCE") == 6.361:
                layer.DeleteFeature(i)
            if feature.GetField("DISTANCE") == 7.361:
                newGeom = feature
        return newGeom
        # After Altering shape file run this statement
        dataSource.ExecuteSQL("REPACK P_SA_Do_Nothing2010_84");

#-------------------------------------------------------------------------------
    def createShapeFile(self, name):
        # Creating new shape file.....................................
        # From old shp file
        newGeom = self.iterrating() # test function to iter over features
        layer = self.dataSource.GetLayerByIndex(0)

        outShapefile = "%s.shp" % (name)
        outDriver = ogr.GetDriverByName("ESRI Shapefile")

        # Remove output shapefile if it already exists
        if os.path.exists(outShapefile):
            outDriver.DeleteDataSource(outShapefile)


        # Create the output shapefile
        outDataSource = outDriver.CreateDataSource(outShapefile)
        outLayer = outDataSource.CreateLayer(name, geom_type=ogr.wkbLineString)


        # # Add an ID field
        # idField = ogr.FieldDefn("id", ogr.OFTInteger)
        # outLayer.CreateField(idField)

        # Add input Layer Fields to the output Layer
        inLayerDefn = layer.GetLayerDefn()
        for i in range(0, inLayerDefn.GetFieldCount()):
            fieldDefn = inLayerDefn.GetFieldDefn(i)
            outLayer.CreateField(fieldDefn)

        #  spatial referance/ write prj file from exciting
        spatialRef = layer.GetSpatialRef()
        spatialRef.MorphToESRI()
        outLayerPrj = outShapefile[:-3] +'prj'
        file = open(outLayerPrj, 'w')
        file.write(spatialRef.ExportToWkt())
        file.close()

        # Create the feature and set values
        # featureDefn = layer.GetLayerDefn()
        # feature = ogr.Feature(featureDefn)
        # feature.SetGeometry(line)
        # feature.SetField("id", 1)

        outLayer.CreateFeature(newGeom) # newGeomline is line geometry from exsciting shp

        # Close DataSource
        outDataSource.Destroy()
        self.dataSource.Destroy()
        print ('Sahpefile "%s" has been created on following path "%s"' % (outShapefile, os.path.abspath(outShapefile))  )



#==================================================
#ReadShapeFile.readshp(r"P_SA_Do_Nothing2010_84.shp")