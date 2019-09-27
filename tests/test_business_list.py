from bddrest.authoring import response, status, when, given

from inception.models import Business, Member
from .helpers import LocalApplicationTestCase


class TestBusiness(LocalApplicationTestCase):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        cls.member = Member(
            name='mehdi',
            family='nazari',
            email='mehdi.new@gmail.com',
            password='123abc',
            role='member',
        )
        session.add(cls.member)
        session.commit()

        cls.business = Business(
            title='Business title',
            phone='09352117155',
            address='business address',
            area='business area',
            member_id=1,
        )
        session.add(cls.business)
        session.commit()

    def test_list(self):
        self.login(self.member.email)

        form = dict(
            title='new business',
            phone='09352117155',
            address='business address',
            area='business area',
            memberId=1,
        )

        with self.given(
            'List all businesses',
            f'/apiv1/businesses',
            'LIST',
            form=form,
        ):
            assert response.status == 200

