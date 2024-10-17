from sqlalchemy import Column,Integer,String,ForeignKey,Float,Boolean
from infra.sqlalchemy.config.database import Base
from sqlalchemy.orm import relationship

class Register_user(Base):
    __tablename__ = 'register_user'

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(50))
    email = Column(String(120))
    password = Column(String(300))

    donations_given = relationship('Donations',foreign_keys='Donations.donor_id',back_populates='donor')
    donations_received =relationship('Donations',foreign_keys='Donations.receiver_id',back_populates='receiver')


class Donations(Base):
    __tablename__ = 'donations'

    id = Column(Integer,primary_key=True,index=True)
    item_name = Column(String(100))
    quantity = Column(Float)
    description = Column(String(200))
    status = Column(String(100))
    donor_id = Column(Integer, ForeignKey('register_user.id'))
    receiver_id = Column(Integer, ForeignKey('register_user.id'))

    donor= relationship('Register_user',foreign_keys=[donor_id], back_populates='donations_given')
    receiver = relationship('Register_user',foreign_keys=[receiver_id],back_populates='donations_received')
