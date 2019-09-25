from nanohttp import Controller, json
from restfulpy.controllers import RootController

import inception
from .foo import FooController
from .token import TokenController
from .member import MemberController
from .business import BusinessController


class ApiV1(Controller):
    foos = FooController()
    tokens = TokenController()
    members = MemberController()
    businesses = BusinessController()

    @json
    def version(self):
        return {
            'version': inception.__version__
        }


class Root(RootController):
    apiv1 = ApiV1()

