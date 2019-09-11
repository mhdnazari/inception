import os
import uuid
from hashlib import sha256

from restfulpy.principal import JWTPrincipal, JWTRefreshToken
from restfulpy.orm import DeclarativeBase, Field, relationship
from sqlalchemy import Integer, Unicode, ForeignKey, JSON
from sqlalchemy.orm import synonym
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_media import Image, MagicAnalyzer, ContentTypeValidator, \
    ImageValidator, ImageAnalyzer

from ..validators import member_validator


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
        required=True,
        not_none=True,
        min_length=3,
        max_length=50,
    )
    family=Field(
        Unicode(50),
        required=True,
        not_none=True,
        min_length=3,
        max_length=50,
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
        pattern=r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)',
        not_none=True,
        required=True,
        min_length=5,
        max_length=200,
    )
    _password = Field(
        'password',
        Unicode(128),
        required=True,
        not_none=True,
        min_length=5,
        max_length=200,
        protected=True,
    )
    description = Field(Unicode(500))
    role = Field(Unicode(50))

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
        self._password = salt + hashed_pass.hexdigest()

    def validate_password(self, password):
        hashed_pass = sha256()
        hashed_pass.update((self.password[:64] + password).encode('utf-8'))

        return self.password[64:] == hashed_pass.hexdigest()

    password = synonym(
        '_password',
        descriptor=property(_get_password, _set_password),
        info=dict(protected=True)
    )

    def create_jwt_principal(self):
        return JWTPrincipal({
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'family': self.family,
            'role': [self.role],
            'sessionId': str(uuid.uuid4()),
            'description': self.description,
        })

    def create_refresh_principal(self):
        return JWTRefreshToken(dict(id=self.id))

