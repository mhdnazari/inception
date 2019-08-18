from bddrest.authoring import response, status, when, Update

from inception.models import Member
from inception.tests.helpers import LocalApplicationTestCase


class TestLogin(LocalApplicationTestCase):

    @classmethod
    def mockup(cls):
        member = Member(
            email='already.added@example.com',
            name='user_name',
            family='family',
            password='123abc',
        )
        session = cls.create_session()
        session.add(member)
        session.commit()

    def test_create_token(self):
        email = 'already.added@example.com'
        password = '123abc'

        with self.given(
            'Create a login token',
            '/apiv1/tokens',
            'Create',
            form=dict(email=email, password=password)
        ):
            import pudb; pudb.set_trace()  # XXX BREAKPOINT
            assert status == 200
            assert 'token' in response.json

            when('Invalid password', form=Update(password='123ab'))
            assert status == '603 Incorrect Email Or Password'

            when('Not exist email', form.Update(email='user@example.com'))
            assert status == '603 Incorrect Email Or Password'

            when('Invalid email format', form.Update(email='user.com'))
            assert status == '701 Invalid Email Format'

            when('Trying too password with empty form', form={})
            assert status == '400 Empty Form'

