from restfulpy.orm import DeclarativeBase, Field, relationship
from sqlalchemy import Integer, Unicode, BigInteger, ForeignKey


class Business(DeclarativeBase):
    __tablename__ = 'business'

    id = Field(Integer, primary_key=True)
    title = Field(
        Unicode(50),
        required=True,
        not_none=True,
        pattern=r'^[a-zA-Z][\w]{5,19}$',
        min_length=3,
        max_length=50,
        unique=True,
    )
    address = Field(Unicode(250))
    phone = Field(Unicode(11), nullable=True, required=False)
    area = Field(Unicode(50))
    member_id = Field(
        Integer,
        ForeignKey('member.id'),
        protected=True,
        not_none=True,
        nullable=False,
    )

    #TODO: map fields

    member = relationship(
        'Member',
        back_populates='businesses',
        protected=True,
    )

