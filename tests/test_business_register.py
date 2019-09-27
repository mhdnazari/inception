from bddrest.authoring import response, status, when, given, Update, Remove

from inception.models import Business
from .helpers import LocalApplicationTestCase
from inception.models import Member, Business


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
            address='Business address',
            area='Business area',
            phone=9352117155,
            member_id =1,
        )
        session.add(cls.business)
        session.commit()

    def test_register(self):
        form = dict(
            title='new business',
            address='new address',
            area='new area',
            phone=989352117155,
            memberId=1,
        )

        with self.given(
            'Register a business',
            f'/apiv1/businesses',
            'REGISTER',
            form=form,
        ):
            assert response.status == 200

            when(
                'Title address already is registered',
                 form=Update(title='Business title')
            )
            assert status == '602 Title Is Already Registered'

            when('Request without title parameter', form=Remove('title'))
            assert status == '724 Title Not In Form'

            when('The title format is invalid', form=Update(title='123abc '))
            assert status == '708 Invalid Title Format'

            when('Request without phone parameter', form=Remove('phone'))
            assert status == '725 Phone Not In Form'

           # when('The phone format is invalid', form=Update(phone=9352117155))
           # assert status == '712 Invalid Phone Format'

