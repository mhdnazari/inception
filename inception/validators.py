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
        max_length=(50, '706 Password Length Is More Than 50'),
        min_length=(5, '707 Password Length Is More Than 50'),
    ),
    name=dict(
        required='723 Name Not In Form',
    ),
)

business_validator = validate(
    title=dict(
        required='724 Title Not In Form',
        max_length=(50, '708 Title Length Is More Than 50'),
        min_length=(5, '709 Title Length Is Less Than 5'),
        pattern=(
            r'^[a-zA-Z]{1}[0-9-a-z-A-Z ,.\'-]{2,49}$',
            '708 Invalid Title Format'
        ),
    ),
    phone=dict(
        required='725 Phone Not In Form',
        max_length=(12, '710 Phone Length Is More Than 12'),
        min_length=(10, '711 Phone Length Is Less Than 11'),
    ),
)

