from nanohttp import json, context, HTTPStatus, HTTPNotFound, RestController
from restfulpy.orm import DBSession, commit

from ..models import Member


class TokenController(RestController):

    @json(prevent_empty_form=True)
    @Foo.validate(strict=True)
    @commit
    def create(self):
        email = context.form.get('email')
        password = context.form.get('password')

        member = DBSession.query(Member) \
            .filter(Member.email == email) \
            .one_or_none()
        if member is None:
            raise HTTPStatus('400 Invalid email or password')



        if DBSession.query(Foo).filter(Foo.title == title).count():
            raise HTTPStatus('604 Title Is Already Registered')

        foo = Foo()
        foo.update_from_request()
        DBSession.add(foo)
        return foo

