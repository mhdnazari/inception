class Inception(Application):
    __authenticator__ = Authenticator()
    __configuration__ = '''

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

    '''

inception = Inception()

