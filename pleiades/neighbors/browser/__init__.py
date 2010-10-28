import logging
import math
from shapely.geometry import asShape

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import Batch
from Products.ZCatalog.CatalogBrains import AbstractCatalogBrain, NoBrainer

from zgeo.geographer.interfaces import IGeoreferenced

log = logging.getLogger('pleiades.beighbors')

Re = 6371000.0 # radius of earth in meters, spherical approx
F = 180.0/(math.pi*Re)

class NeighborsView(BrowserView):
    """HTML representation of neighbors
    """

    __call__ = ViewPageTemplateFile('neighbors.pt')

    def distance(self, b):
        try:
            g = IGeoreferenced(self.context)
            geom = asShape({'type': g.type, 'coordinates': g.coordinates})
            y0 = geom.centroid.y
            other = asShape(b.zgeo_geometry)
            d = geom.distance(other)
            return int(math.cos(math.pi*y0/180.0)*d/F/1000)
        except:
            log.warn("Failed to find distance between %s and %s" % (
                self.context, b.getPath()))
            raise

    def center(self, b):
        try:
            centroid = asShape(b.zgeo_geometry).centroid
            return "%f,%f" % (centroid.x, centroid.y)
        except:
            log.warn("Failed to find center of %s" % (
                b.getPath()))
            raise

    def nearest(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        class NeighborBrain(AbstractCatalogBrain, NoBrainer):
            pass
        cschema = catalog._catalog.schema
        scopy = cschema.copy()
        scopy['data_record_id_']=len(cschema.keys())
        scopy['data_record_score_']=len(cschema.keys())+1
        scopy['data_record_normalized_score_']=len(cschema.keys())+2
        scopy['distance']=len(cschema.keys())+3
        scopy['center']=len(cschema.keys())+4
        NeighborBrain.__record_schema__ = scopy
        try:
            g = IGeoreferenced(self.context)
        except:
            return []
        def gen():
            for brain in catalog(
                geolocation={'query': (g.bounds, 10), 'range': 'nearest'}, 
                portal_type={'query': ['Place']},
                sort_index='geolocation'
                ):
                if brain.getId == self.context.getId():
                    # skip self
                    continue
                neighbor = NeighborBrain().__of__(catalog)
                for k in brain.__record_schema__.keys():
                    neighbor[k] = brain[k]
                neighbor['distance'] = self.distance(brain)
                neighbor['center'] = self.center(brain)
                yield neighbor
        b_size = 20
        b_start = self.request.get('b_start', 0)
        batch = Batch(list(gen()), b_size, int(b_start), orphan=0)
        return batch

