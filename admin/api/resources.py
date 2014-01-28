from lib.tastyalchemy.tastyalchemy import SQLAlchemyResource as Resource
from admin.models import Nurse
from nurses.db import Session

class NurseResource(Resource):
    class Meta:
        resource_name = "nurse"
        object_class = Nurse
        allowed_methods = ['get', 'post', 'put', 'delete']
        queryset = Session().query(Nurse).all()
