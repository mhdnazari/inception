from nanohttp import json, context, HTTPStatus, HTTPNotFound, RestController, \
    HTTPStatus
from restfulpy.orm import DBSession, commit

from ..models import Member


class TokenController(RestController):

    @json(prevent_empty_form=True)
    @email_validator
    def create(self):
        email = context.form.get('email')
        password = context.form.get('password')
        if email and password is None:
            raise HTTPIncorrectEmailOrPassword()

        principal = context.application.__authenticator__.\
            login((email, password))

        if principal is None:
            raise HTTPStatus('400 Invalid Email Or Password')

        return dict(token=principal.dump())

