from nanohttp import json, context, HTTPStatus, HTTPNotFound, RestController, \
    int_or_notfound
from restfulpy.orm import DBSession, commit
from restfulpy.authorization import authorize

from ..models import Business, Member
from ..validators import business_validator


class BusinessController(RestController):

    @json(prevent_empty_form=True)
    @business_validator
    @commit
    def register(self):
        title = context.form.get('title')
        address = context.form.get('address')
        area = context.form.get('area')
        member_id = context.form.get('memberId')

        business = DBSession.query(Business) \
                .filter(Business.title == title) \
                .one_or_none()

        if DBSession.query(Business.title) \
        .filter(Business.title == title) \
        .count():
            raise HTTPStatus('602 Title Is Already Registered')

        business = Business(
            title=title,
            address=address,
            area=area,
            member_id=member_id,
        )
        DBSession.add(business)
        return business

    @json
    @authorize
    @Business.expose
    def list(self):
        query = DBSession.query(Business)
        return query

    @json(prevent_form='709 Form Not Allowed')
    @authorize
    def get(self, id):
        int_or_notfound(id)
        business = DBSession.query(Business).get(id)
        if business is None:
            HTTPNotFound()

        return business

