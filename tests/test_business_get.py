from bddrest.authoring import response, when, status, given

from inception.models import Member, Business
from .helpers import LocalApplicationTestCase


class TestBusiness(LocalApplicationTestCase):

    @classmethod
    def mockup(cls):
        cls.member = Member(
            name='member name',
            family='member family',
            email='already@example.com',
            _password='123abc',
            description='description',
            role='member',
        )
        session = cls.create_session()
        session.add(cls.member)
        session.commit()

        cls.business = Business(
            title='business title',
            area='business area',
            address='business address',
            phone='09352117155',
            member_id=1,
        )
        session.add(cls.business)
        session.commit()

    def test_get(self):
        self.login(self.member.email)

        form = dict(
            title='new business',
            phone='09352117155',
            address='business address',
            area='business area',
            memberId=1,
        )
        with self.given(
            'Get a business',
            f'/apiv1/businesses/id: {self.member.id}',
            f'GET',
        ):
            assert status == 200

