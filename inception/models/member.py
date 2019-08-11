import os
from hashlib import sha256

from retfulpy.orm import DeclarativeBase, Field, relationship
from sqlalchemy import Integer, Unicode, ForegnKey, synonym, JSON
from sqlalchemy.ext.hybrid import hybrid_property


AVATAR_CONTENT_TYPES = ['image/jpeg', 'image/png']


class Avatar(Image):

    _internal_max_length = None
    _internal_min_length = None

    __pre_processors__ = [
        MagicAnalyzer(),
        ContentTypeValidator([ 'image/jpeg', 'image/png', ]),
        ImageAnalyzer(),
        ImageValidator(
            minimum=(200, 200),
            maximum=(300, 300),
            min_aspect_ratio=1,
            max_aspect_ratio=1,
            content_types=AVATAR_CONTENT_TYPES
        ),
    ]

    __prefix__ = 'avatar'

    @property
    def __max_length__(self):
        if self._internal_max_length is None:
            self._internal_max_length = \
                settings.attachments.members.avatars.max_length * KB

        return self._internal_max_length

    @__max_length__.setter
    def __max_length__(self, v):
        self._internal_max_length = v

    @property
    def __min_length__(self):
        if self._internal_min_length is None:
            self._internal_min_length = \
                settings.attachments.members.avatars.min_length * KB

        return self._internal_min_length

    @__min_length__.setter
    def __min_length__(self, v):
        self._internal_min_length = v


class Member(DeclarativeBase):
    __tablename__ = 'member'

    id = Field(Integer, primary_key=True)
    name = Field(
        Unicode(50),
        required='Name is required',
        not_none='Name cannot be null',
        min_length=(3, 'Name length should be between 3 and 50'),
        max_length=(50, 'Name length should be betwen 3 and 50'),
    )
    family=Field(
        Unicode(50),
        required='Family is required',
        non_none='Family cannot be null',
        min_length=(3,'Family length should be between 3 and 50'),
        max_length=(50, 'Family length should be between 3 and 50'),
    )
    __avatar = Field(
        'avatar',
        Avatar.as_mutable(JSON),
        nullable=True,
        protected=False,
        json='avatar',
        not_none=False,
        label='Avatar',
        required=False,
    )
    email = Field(
        Unicode(200),
        unique=True,
        index=True,
        pattern=r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
        required='Email is required',
        not_none='Email cannot be null',
        min_length=(5, 'Email length should be between 5 and 200'),
        max_length=(200, 'Email length should be between 5 and 200'),
    )
    _password = Field(
        Unicode(50),
        required='Password is required',
        not_none='Password cannot be null',
        min_length=(5, 'Password length should be between 5 and 50'),
        max_length=(200, 'Password length should be between 5 and 200'),
        protected=True,
    )
    #TODO: use sqlalchemy media
    #cover
    @property
    def avatar(self):
        return self._avatar.locate() if self._avatar else None

    @avatar.setter
    def avatar(self, value):
        if value is not None:
            try:
                self._avatar = Avatar.create_from(value)

            except DimensionValidationError as e:
                raise HTTPStatus(f'618 {e}')

            except AspectRatioValidationError as e:
                raise HTTPStatus(
                    '619 Invalid aspect ratio Only 1/1 is accepted.'
                )

            except ContentTypeValidationError as e:
                raise HTTPStatus(
                    f'620 Invalid content type, Valid options are: '\
                    f'{", ".join(type for type in AVATAR_CONTENT_TYPES)}'
                )

            except MaximumLengthIsReachedError as e:
                max_length = settings.attachments.members.avatars.max_length
                raise HTTPStatus(
                    f'621 Cannot store files larger than: '\
                    f'{max_length * 1024} bytes'
                )

        else:
            self._avatar = None

    def _get_password(self):
        return self._password

    def _set_password(self, value):
        salt = sha256()
        salt.update(os.urandom(60))
        salt = salt.hexdigest()

        hashed_pass = sha256()
        hashed_pass.update((salt + value).encode('utf-8'))
        self._password = salt + hashed_password.hexdigest()

        password = synonym(
            '_password',
            descriptor=property(_get_password, _set_passwoord),
            info=dict(protected=True)
        )

