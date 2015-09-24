import datetime as dt
import os

from vwadaptor.database import (
    Column,
    db,
    Model,
    ReferenceCol,
    relationship,
    SurrogatePK
)

from vwadaptor.constants import PROGRESS_STATES
from sqlalchemy.ext.hybrid import hybrid_property


class ModelRun(SurrogatePK, Model):

    __tablename__ = 'modelruns'
    
    title = Column(db.String(80), unique=True, nullable=False)
    model_name = Column(db.String(30), nullable=False)
    resources = relationship('ModelResource', backref='modelrun', lazy='dynamic')
    user_id = Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
    #'not_started','queued', 'running','finished','error'
    progress_state = Column( db.Enum(*tuple(PROGRESS_STATES.values())), default=PROGRESS_STATES['NOT_STARTED'])
    progress_value = Column(db.Float(10), nullable=True,default=0.0)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    def __init__(self,**kwargs):
        db.Model.__init__(self, **kwargs)
    def __repr__(self):
        return '<ModelRun({id}:{name})>'.format(id=self.id,name=self.title)


class ModelResource(SurrogatePK, Model):
    __tablename__ = 'modelresources'
    resource_type = Column(db.String(80), nullable=False)
    #resource_url = Column(db.String(200), nullable=True)
    resource_location = Column(db.String(80), nullable=True, unique=True)
    resource_size = Column(db.Integer)
    modelrun_id = Column(db.Integer, db.ForeignKey('modelruns.id'))
    created_at = Column(db.DateTime, nullable=True, default=dt.datetime.utcnow)
    @hybrid_property
    def resource_name(self):
        return os.path.basename(self.resource_location)

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)

    def __repr__(self):
        return '<ModelResource({type}--{name})>'.format(type=self.file_type,name=self.file_location)