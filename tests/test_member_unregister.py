from bddrest.authoring import response, given, when, status

from inception.models import Member
from .helpers import LocalApplicationTestCase


class TestMember(LocalApplicationTestCase):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        cls.member = Member(
            email='already.addted@example.com',
            name='Member name',
            family='Member family',
            password='123abc',
            description='Member description',
            role='member',
        )
        session.add(cls.member)
        session.commit()

    def test_member_unregister(self):
        self.login(self.member.email)

        with self.given(
            'Unregister a member',
            f'/apiv1/members/id: {self.member.id}',
            'UNREGISTER',
        ):
            assert status == 200
            assert response.json['id'] == self.member.id

            when(
                'Member not found',
                url_parameters=given | dict(id=0)
            )
            status == 404

            when(
                'Member not found',
                url_parameters=given | dict(id='Alphabetical')
            )
            status == 404

