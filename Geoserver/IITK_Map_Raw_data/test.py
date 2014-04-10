import mapnik
import pdb
from shapely.geometry import *
from shapely.wkt import loads,dumps

class TestDatasource(mapnik.PythonDatasource):
    def __init__(self, geom):
        super(TestDatasource, self).__init__()
        self.geom=loads(geom)

    def features(self, query):
        return mapnik.PythonDatasource.wkb_features(
            keys = ('label',), 
            features = (
                ( self.geom.wkb, { 'label': 'foo-bar'} ), 
                ( self.geom.wkb, { 'label': 'buzz-quux'} ), 
            )
        )

if __name__ == '__main__':
	m = mapnik.Map(1280,1024)
	m.background = mapnik.Color('white')
	s = mapnik.Style()
	r = mapnik.Rule()
	r.symbols.append(mapnik.LineSymbolizer())
	t = mapnik.TextSymbolizer(mapnik.Expression("[label]"),"DejaVu Sans Book",10,mapnik.Color('black'))
	t.displacement = (5,5)
	r.symbols.append(t)
	line_symbolizer = mapnik.LineSymbolizer(mapnik.Color('rgb(50%,50%,50%)'),0.1)
	r.symbols.append(line_symbolizer)
	s.rules.append(r)
	m.append_style('point_style',s)
	geom="LINESTRING(427.719000201 848.282,427.719 482.5)"
	#~ pdb.set_trace()
	ds = mapnik.Python(factory='TestDatasource',geom=geom)
	layer = mapnik.Layer('python')
	layer.datasource = ds
	layer.styles.append('point_style')
	m.layers.append(layer)
	m.zoom_all()
	mapnik.render_to_file(m,'map.png', 'png')

#~ import mapnik
#~ m = mapnik.Map(600,300)
#~ m.background = mapnik.Color('steelblue')
#~ s = mapnik.Style()
#~ r = mapnik.Rule()
#~ polygon_symbolizer = mapnik.PolygonSymbolizer(mapnik.Color('#f2eff9'))
#~ r.symbols.append(polygon_symbolizer)
#~ line_symbolizer = mapnik.LineSymbolizer(mapnik.Color('rgb(50%,50%,50%)'),0.1)
#~ r.symbols.append(line_symbolizer)
#~ s.rules.append(r)
#~ m.append_style('My Style',s)
#~ ds = mapnik.Shapefile(file='Roads.shp')
#~ layer = mapnik.Layer('world')
#~ layer.datasource = ds
#~ layer.styles.append('My Style')
#~ m.layers.append(layer)
#~ m.zoom_all()
#~ mapnik.render_to_file(m,'world.png', 'png')
#~ print "rendered image to 'world.png'"
