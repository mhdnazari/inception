from bddrest.authoring import response, status, when, Update, Remove, given

from inception.models import Member
from .helpers import LocalApplicationTestCase


class TestLogin(LocalApplicationTestCase):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        cls.member = Member(
            email='already.added@example.com',
            name='user_name',
            family='family',
            password='123abc',
        )
        session.add(cls.member)
        session.commit()

    def test_create_token(self):
        email = self.member.email
        password = '123abc'

        with self.given(
            'Create a login token',
            '/apiv1/tokens',
            'CREATE',
            form=dict(email=email, password=password)
        ):
            assert status == 200
            assert 'token' in response.json

            when('Invalid password', form=Update(password='123ab'))
            assert status == '603 Incorrect Email Or Password'

            when('Not exist email', form=Update(email='user@example.com'))
            assert status == '603 Incorrect Email Or Password'

            when('Invalid email format', form=Update(email='user.com'))
            assert status == '701 Invalid Email Format'

            when('Trying to pass with empty form', form={})
            assert status == '400 Empty Form'

            when('Email is empty', form=Remove('email'))
            assert status == '722 Email Not In Form'

            when('Passeord is empty', form=Remove('password'))
            assert status == '723 Password Is Not In Form'

            when(
                'Password length is more than 50',
                form=Update(password=(50 + 1) * 'a')
            )
            assert status == '706 Title Length Is More Than 50'


