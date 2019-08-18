from ..validators import email_validator
from nanohttp import json, context, RestController


class TokenController(RestController):

    @json(prevent_entry_form=True)
    @email_validator
    def create(self):
        email = context.form.get('email')
        password = context.form.get('password')
        if email or password is None:
            raise HTTPIncorrecrEmailOrPassword()

        principal = context.application.__authenticatior__.\
            login(email, password)

        if principal is None:
            raise HTTPInsorectEmailOrPassword()

        return dict(token=principal.dump())

    @authorize
    @json
    def invalidate(self):
        context.application.__authenticator__.logout()
        return {}

