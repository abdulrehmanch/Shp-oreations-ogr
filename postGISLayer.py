from osgeo import ogr
import sys

databaseServer = "localhost"
databaseName = "db_consumer_survey_wasa_multan"
databaseUser = "postgres"
databasePW = "123"
connString = "PG: host=%s dbname=%s user=%s password=%s" %(databaseServer,databaseName,databaseUser,databasePW)


def GetPGLayerFields( lyr_name ):
    conn = ogr.Open(connString)

    lyr = conn.GetLayer( lyr_name )
    if lyr is None:
        print >> sys.stderr, '[ ERROR ]: layer name = "%s" could not be found in database "%s"' % ( lyr_name, databaseName )
        sys.exit( 1 )




##Feature count
    featureCount = lyr.GetFeatureCount()
    print (featureCount)

##    itterate over featues
    for i in range(featureCount):
        geom = lyr.GetFeature(i)
##        print geom

## Column names
    lyrDefn = lyr.GetLayerDefn()
    for i in range( lyrDefn.GetFieldCount() ):
        print (lyrDefn.GetFieldDefn( i ).GetName())

    conn.Destroy()

lyr_name = 'tbl_domestic_geom'
GetPGLayerFields( lyr_name )




