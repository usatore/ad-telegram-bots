from sqlalchemy import Column, Integer, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship, validates

from app.database import Base

class Company(Base):
    __tablename__ = "company"

    id = Column(Integer, primary_key=True, nullable=False)
    telegram_id = Column(Integer, nullable=False)
    money_balance = Column(Integer, default=0)

    campaigns = relationship('Campaign', back_populates='company')


class Campaign(Base):
    __tablename__ = "campaign"

    id = Column(Integer, primary_key=True, nullable=False)
    company_id = Column(Integer, ForeignKey('company.id'))
    description = Column(JSON, nullable=False)
    view_price = Column(Integer, nullable=False)
    approved = Column(Boolean, default=False, nullable=False)

    company = relationship('Company', back_populates='campaigns')
    integrations = relationship('Integration', back_populates='campaign')




class Blogger(Base):
    __tablename__ = "blogger"

    id = Column(Integer, primary_key=True, nullable=False)
    telegram_id = Column(Integer, nullable=False)
    money_balance = Column(Integer, default=0)

    integrations = relationship('Integration', back_populates='blogger')



class Integration(Base):
    __tablename__ = "integration"

    id = Column(Integer, primary_key=True, nullable=False)
    blogger_id = Column(Integer, ForeignKey('blogger.id'), nullable=False)
    campaign_id = Column(Integer, ForeignKey('campaign.id'), nullable=False)
    links = Column(JSON, default=list)
    views_count = Column(Integer, default=0, nullable=False)
    approved = Column(Boolean, default=False, nullable=False)

    blogger = relationship('Blogger', back_populates='integrations')
    campaign = relationship('Campaign', back_populates='integrations')

    '''
    @validates('links')
    def validate_links(self, key, value):
        if value is not None and not isinstance(value, list):
            raise ValueError('links must be a list')
        return value
    '''



