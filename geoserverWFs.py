import sys

try:
    from osgeo import ogr, osr, gdal
except:
    sys.exit('ERROR: cannot find GDAL/OGR modules')

# Set the driver (optional)
wfs_drv = ogr.GetDriverByName('WFS')

# Speeds up querying WFS capabilities for services with alot of layers
gdal.SetConfigOption('OGR_WFS_LOAD_MULTIPLE_LAYER_DEFN', 'NO')

# Set config for paging. Works on WFS 2.0 services and WFS 1.0 and 1.1 with some other services.
gdal.SetConfigOption('OGR_WFS_PAGING_ALLOWED', 'YES')
gdal.SetConfigOption('OGR_WFS_PAGE_SIZE', '10000')

# Open the webservice
url = 'http://localhost:8088/geoserver/'
wfs_ds = wfs_drv.Open('WFS:' + url)
if not wfs_ds:
    sys.exit('ERROR: can not open WFS datasource')
else:
    pass

# iterate over available layers
for i in range(wfs_ds.GetLayerCount()):
    layer = wfs_ds.GetLayerByIndex(i)
    srs = layer.GetSpatialRef()
    print ('Layer: %s, Features: %s, SR: %s...' % (layer.GetName(), layer.GetFeatureCount(), srs.ExportToWkt()[0:50]))

    # iterate over features
    feat = layer.GetNextFeature()
    while feat is not None:
        feat = layer.GetNextFeature()
        # do something more..
    feat = None

# Get a specific layer
layer = wfs_ds.GetLayerByName("largelayer")
if not layer:
    sys.exit('ERROR: can not find layer in service')
else:
    pass