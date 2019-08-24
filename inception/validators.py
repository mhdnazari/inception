import re

from nanohttp import validate


EMAIL_PATTERN = re.compile(
    r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
)

login_validator = validate(
    email=dict(
        required='722 Email Not In Form',
        pattern=(EMAIL_PATTERN, '701 Invalid Email Format'),
    ),
    password=dict(
        required='723 Password Is Not In Form',
        max_length=(50, '706 Title Length Is More Than 50'),
        min_length=(5, '707 Title Length Is More Than 50'),
    ),
)


member_validator = validate(
    email=dict(
        required='722 Email Not In Form',
        pattern=(EMAIL_PATTERN, '701 Invalid Email Format'),
    ),
    password=dict(
        required='723 Password Is Not In Form',
        max_length=(50, '706 Title Length Is More Than 50'),
        min_length=(5, '707 Title Length Is More Than 50'),
    ),
    name=dict(
        required='723 Name Not In Form',
    ),
)


