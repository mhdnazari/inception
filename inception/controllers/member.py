from nanohttp import json, context, HTTPStatus, HTTPNotFound, RestController, \
    int_or_notfound
from restfulpy.orm import DBSession, commit
from restfulpy.authorization import authorize

from ..models import Member
from ..validators import member_validator


class MemberController(RestController):

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

    @json
    @authorize
    @Member.expose
    def list(self):
        query = DBSession.query(Member)
        return query

    @json(prevent_form='709 Form Not Allowed')
    @authorize
    def get(self, id):
        id = int_or_notfound(id)
        member = DBSession.query(Member).get(id)
        if member is None:
            raise HTTPNotFound()

        return member

    @json
    @authorize
    @commit
    def unregister(self, id):
        id = int_or_notfound(id)
        member = DBSession.query(Member).get(id)
        if member is None:
            raise HTTPNotFound()

        DBSession.delete(member)
        return member

    @json
    @authorize
    @member_validator
    @commit
    def update(self, id):
        id = int_or_notfound(id)
        member = DBSession.query(Member).get(id)
        if member is None:
            raise HTTPNotFound()

        member.update_from_request()
        return member

