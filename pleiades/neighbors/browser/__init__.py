from plone.memoize.instance import memoize
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import Batch

from Products.PleiadesEntity.geo import NotLocatedError
from zgeo.geographer.interfaces import IGeoreferenced


class NeighborsView(BrowserView):
    """HTML representation of neighbors
    """

    __call__ = ViewPageTemplateFile('neighbors.pt')
    
    def nearest(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        try:
            g = IGeoreferenced(self.context)
        except NotLocatedError:
            raise StopIteration
        def gen():
            for brain in catalog(
                geolocation={'query': (g.bounds, 20000.0), 'range': 'distance'}, 
                portal_type={'query': ['Place']}):
                if brain.getId == self.context.getId():
                    # skip self
                    continue
                yield brain
        b_size = 20
        b_start = self.request.get('b_start', 0)
        batch = Batch(list(gen()), b_size, int(b_start), orphan=0)
        return batch



