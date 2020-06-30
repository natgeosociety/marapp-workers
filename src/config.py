import logging
from enum import Enum, unique

from marapp_metrics.metrics.biodiversity_intactness import BiodiversityIntactnessMetric
from marapp_metrics.metrics.human_footprint import HumanFootprint
from marapp_metrics.metrics.human_impact import HumanInfluenceEnsembleMetric
from marapp_metrics.metrics.land_cover import LandUseLandCover
from marapp_metrics.metrics.modis_fire import ModisFire
from marapp_metrics.metrics.protected_areas import ProtectedAreas
from marapp_metrics.metrics.terrestrial_carbon import TerrestrialCarbon
from marapp_metrics.metrics.tree_loss import TreeLoss
from marapp_metrics.metrics.modis_evi import ModisEvi

# https://github.com/googleapis/google-api-python-client/issues/299
logging.getLogger("googleapiclient.discovery_cache").setLevel(logging.CRITICAL)


class MetricHandlerException(Exception):
    pass


@unique
class MetricHandler(Enum):
    """Resolve the metric handler from the `metrics` library."""

    BIODIVERSITY_INTACTNESS = BiodiversityIntactnessMetric
    HUMAN_FOOTPRINT = HumanFootprint
    HUMAN_IMPACT = HumanInfluenceEnsembleMetric
    LAND_USE = LandUseLandCover
    MODIS_FIRE = ModisFire
    MODIS_EVI = ModisEvi
    PROTECTED_AREAS = ProtectedAreas
    TERRESTRIAL_CARBON = TerrestrialCarbon
    TREE_LOSS = TreeLoss

    @classmethod
    def slugs(cls):
        return [h.slug for h in cls.handlers()]

    @classmethod
    def has_slug(cls, slug_name):
        return any(h.slug == slug_name for h in cls.handlers())

    @classmethod
    def handlers(cls):
        return (e.value for e in cls)

    @classmethod
    def get_handler(cls, slug_name):
        return next((h for h in cls.handlers() if h.slug == slug_name), None)
