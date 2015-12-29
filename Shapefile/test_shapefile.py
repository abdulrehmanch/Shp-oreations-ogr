import os
from Shapefile import Shapefile


shp = Shapefile(r"test.shp")
print ('Number of features: ', shp.featureCount())
print ('\n'.join(shp.fields()))
shp.createShapeFile('Line_Features')

