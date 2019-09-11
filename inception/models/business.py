from restfulpy.orm import DeclarativeBase, Field, relationship
from sqlalchemy import Integer, Unicode, ForeignKey


class Business(DeclarativeBase):
    __tablename__ = 'business'

    id = Field(Integer, primary_key=True)
    title = Field(Unicode(50),
                  required=True,
                  not_none=True,
                  min_length=3,
                  max_length=50,
                  unique=True,
                  )
    address = Field(Unicode(250))
    phone = Field(BigInteger, nullable=True, required=False)
    area = Field(Unicode(50))

    #TODO: map fields

    member = relationship(
        'member',
        uselist=False,
        back_populates='business',
        protected=True,
    )

