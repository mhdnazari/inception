from bddrest.authoring import response, status, when, given, Update, Remove

from inception.models import Member
from .helpers import LocalApplicationTestCase

class TestMember(LocalApplicationTestCase):
    @classmethod
    def mockup(cls):
        cls.member = Member(
            name='member name',
            family='member family',
            email='already.added@example.com',
            _password='123abc',
        )
        session = cls.create_session()
        session.add(cls.member)
        session.commit()

    def test_register(self):
        form = dict(
            name='new name',
            family='new family',
            email='already@example.com',
            password='123abc',
        )

        with self.given(
            'Register a member',
            '/apiv1/members',
            'REGISTER',
            form=form,
        ):
            assert response.status == 200

            when('Invalid email format', form=Update(email='us@.com'))
            assert status == '701 Invalid Email Format'

            when(
                'Email address already is registered',
                 form=Update(email='already.added@example.com')
            )
            assert status == '601 Email Address Is Already Registered'

            when('Request without email parameter', form=Remove('email'))
            assert status == '722 Email Not In Form'

            when('Request without name parameter', form=Remove('name'))
            assert status == '723 Name Not In Form'

            when('Request without family', form=Remove('family'))
            assert 'Family Not In form'

