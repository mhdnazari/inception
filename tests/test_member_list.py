from bddrest.authoring import response, status, when, Update, Remove, given

from inception.models import Member
from .helpers import LocalApplicationTestCase


class TestMember(LocalApplicationTestCase):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        cls.member = Member(
            name = 'Member Name',
            family = 'Member Family',
            email = 'member@example.com',
            password = 'abc123',
        )
        session.add(cls.member)
        session.commit()

    def test_member_list(self):
        self.login(self.member.email)

        form = dict(
            name='new name',
            family='new family',
            email='already@example.com',
            password='123abc',
        )

        with self.given(
            'List all members',
            '/apiv1/members',
            'LIST',
            form=form,
        ):
            assert response.status == 200

