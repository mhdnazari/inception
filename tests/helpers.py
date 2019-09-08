from restfulpy.testing import ApplicableTestCase

from inception import Inception
from inception.models import Member


class LocalApplicationTestCase(ApplicableTestCase):
    __application_factory__ = Inception

    def login(self, email):
        session = self.create_session()
        member = session.query(Member).filter(Member.email == email).one()
        principal = member.create_jwt_principal()
        token = principal.dump()
        self._authentication_token = token.decode('utf-8')

