from restfulpy.testing import ApplicableTestCase

from inception import Inception


class LocalApplicationTestCase(ApplicableTestCase):
    __application_factory__ = Inception

