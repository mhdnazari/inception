from os.path import join, dirname

from restfulpy.application import Application

from .controllers.root import Root


__version__ = '0.1.0-dev'


class Inception(Application):
    __configuration__ = '''
    db:
      url: postgresql://postgres:postgres@localhost/inception_dev
      test_url: postgresql://postgres:postgres@localhost/inception_test
      administrative_url: postgresql://postgres:postgres@localhost/postgres
    '''

    def __init__(self, application_name='inception', root=Root()):
        super().__init__(
            application_name,
            root=root,
            root_path=join(dirname(__file__), '..'),
            version=__version__,
        )


inception = Inception()

