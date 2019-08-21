import functools
from os.path import join, dirname

from nanohttp import settings
from restfulpy.application import Application
from sqlalchemy_media import StoreManager, FileSystemStore

from .controllers.root import Root
from .authentication import Authenticator

__version__ = '0.1.0-dev'


class Inception(Application):
    __authenticator__ = Authenticator()
    __configuration__ = '''
    db:
      url: postgresql://postgres:postgres@localhost/inception_dev
      test_url: postgresql://postgres:postgres@localhost/inception_test
      administrative_url: postgresql://postgres:postgres@localhost/postgres

    storage:
      local_directory: %(root_path)s/../data/assets
      base_url: http://localhost:8083/assets
    attachments:
      applications:
        icons:
          max_length: 50 # KB
          min_length: 1  # KB
    members:
        avatars:
          max_length: 50 # KB
          min_length: 1  # KB
    '''

    @classmethod
    def initialize_orm(cls, engine=None):
        StoreManager.register(
            'fs',
            functools.partial(
                FileSystemStore,
                settings.storage.local_directory,
                base_url=settings.storage.base_url,
            ),
            default=True
        )
        super().initialize_orm(cls, engine)


    def __init__(self, application_name='inception', root=Root()):
        super().__init__(
            application_name,
            root=root,
            root_path=join(dirname(__file__), '..'),
            version=__version__,
        )


inception = Inception()

