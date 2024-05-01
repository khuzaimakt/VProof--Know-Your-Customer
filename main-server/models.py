from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Table
from sqlalchemy.orm import relationship
from database import Base


class Role(Base):
    __tablename__ = 'roles'
    rid = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
# Association table for the many-to-many relationship between User and Meeting
Interviewers = Table('interviewers', Base.metadata,
    Column('uid', Integer, ForeignKey('users.uid'), primary_key=True),
    Column('mid', Integer, ForeignKey('meetings.mid'), primary_key=True)
)

# Association table for the many-to-many relationship between Candidate and Meeting
Interviewees = Table('interviewees', Base.metadata,
    Column('cdid', Integer, ForeignKey('candidates.cdid'), primary_key=True),
    Column('mid', Integer, ForeignKey('meetings.mid'), primary_key=True)
)
class User(Base):
    __tablename__ = 'users'
    uid = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_verified = Column(Boolean, default=False)
    signup_date = Column(DateTime)
    rid = Column(Integer, ForeignKey('roles.rid'))
    # Foreign key to reference the Company
    cid = Column(Integer, ForeignKey('companies.cid'))
    role = relationship("Role")

    # Relationship to reference the Company model
    company = relationship("Company", back_populates="employees")
    # Relationship to the Meeting model through the Interviewers association table
    meetings = relationship(
        "Meeting",
        secondary=Interviewers,
        back_populates="interviewers"
    )

class Company(Base):
    __tablename__ = 'companies'
    cid = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    # Relationship with User
    employees = relationship("User", back_populates="company")

class Candidate(Base):
    __tablename__ = 'candidates'
    cdid = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    nic_front = Column(String)
    nic_back = Column(String)
    dl_front = Column(String)
    dl_back = Column(String)
    passport = Column(String)
    selfie = Column(String)
    unique_identifier = Column(String)
    unique_id = Column(String)
    is_verified = Column(String)
    country = Column(String)
    last_update = Column(DateTime)
    is_not_matching_pics = Column(Boolean)
    is_document_tempered = Column(Boolean)
    is_spoof_picture = Column(Boolean)
    sid = Column(Integer, ForeignKey('statuses.sid'))
    status = relationship("Status")
    meetings = relationship(
        "Meeting",
        secondary=Interviewees,
        back_populates="interviewees"
    )

class Meeting(Base):
    __tablename__ = 'meetings'
    mid = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    scheduled_time = Column(DateTime)
    password = Column(String)
    creation_time = Column(DateTime)
    duration = Column(Integer)
    host_id = Column(Integer, ForeignKey('users.uid'))

    host = relationship("User")
    # Relationships to User and Candidate models through the association tables
    interviewers = relationship(
        "User",
        secondary=Interviewers,
        back_populates="meetings"
    )
    interviewees = relationship(
        "Candidate",
        secondary=Interviewees,
        back_populates="meetings"
    )


class Status(Base):
    __tablename__ = 'statuses'
    sid = Column(Integer, primary_key=True, index=True)
    title = Column(String)
