import datetime as dt

from vwadaptor.extensions import bcrypt
from vwadaptor.database import (
    Column,
    db,
    Model,
    ReferenceCol,
    relationship,
    SurrogatePK
)
from flask.ext.login import UserMixin



class User(SurrogatePK, Model, UserMixin):

    __tablename__ = 'users'
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(80), unique=True, nullable=False)
    #: The hashed password
    password = Column(db.String(128), nullable=True)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    first_name = Column(db.String(30), nullable=True)
    last_name = Column(db.String(30), nullable=True)
    active = Column(db.Boolean(), default=False)
    is_admin = Column(db.Boolean(), default=False)

    modelruns = relationship('ModelRun', backref='user', lazy='dynamic')

    def __init__(self,**kwargs):
        db.Model.__init__(self, **kwargs)
        if 'password' in kwargs:
            self.set_password(kwargs['password'])
        else:
            self.password = None

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        return bcrypt.check_password_hash(self.password, value)