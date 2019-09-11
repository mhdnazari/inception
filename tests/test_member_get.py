from bddrest.authoring import response, given, status, when

from inception.models import Member
from .helpers import LocalApplicationTestCase


class TestMember(LocalApplicationTestCase):

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

    def test_get(self):
        self.login(self.member.email)

        with self.given(
            f'Get a member',
            f'/apiv1/members/id: {self.member.id}',
            f'GET',
        ):
            assert status == 200
            assert response.json['id'] == self.member.id
            assert response.json['name'] == self.member.name
            assert response.json['family'] == self.member.family

            when(
                'Intended member with string type not found',
                url_parameters=dict(id='Alphabetical')
            )
            assert status == 404

            when(
                'Intended member with string type not found',
                url_parameters=dict(id=0)
            )
            assert status == 404

            when(
                'Form parameter is sent with request',
                form=dict(parameter='Invalid form parameter')
            )
            assert status == '709 Form Not Allowed'

            when('Request is not authorized',authorization=None)
            assert status == 401

