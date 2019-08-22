from nanohttp import json, context, HTTPStatus, HTTPNotFound, RestController
from restfulpy.orm import DBSession, commit

from ..models import Member
from ..validators import member_validator


class MemberController(RestController):
    __model__ = Member

    @json(prevent_empty_form=True)
    @member_validator
    @commit
    def register(self):
        email = context.form.get('email')
        password = context.form.get('password')
        name = context.form.get('name')
        family = context.form.get('family')

        member = DBSession.query(Member) \
            .filter(Member.email == email) \
            .one_or_none()

        if DBSession.query(Member.email).filter(Member.email == email).count():
            raise HTTPStatus('601 Email Address Is Already Registered')

        member = Member(
            email=email,
            name=name,
            password=password,
            family=family,
        )
        DBSession.add(member)
        return member

