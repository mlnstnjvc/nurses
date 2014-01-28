from sqlalchemy import (Boolean, Date, DateTime, Integer,
                        String, Unicode, UnicodeText)
from tastypie import fields
from tastypie.bundle import Bundle
from tastypie.exceptions import NotFound
from tastypie.resources import Resource
from nurses.db import Session
from django.core.urlresolvers import NoReverseMatch

FIELD_MAP = {
    Boolean: fields.BooleanField,
    Date: fields.DateField,
    DateTime: fields.DateTimeField,
    Integer: fields.IntegerField,
    String: fields.CharField,
    Unicode: fields.CharField,
    UnicodeText: fields.CharField,
}


class SQLAlchemyResource(Resource):

    def __init__(self, api_name=None):
        super(SQLAlchemyResource, self).__init__(api_name)
        for col in self._meta.object_class.__table__.columns:
            if col.name not in self._meta.excludes:
                kwargs = {
                    'attribute': col.name,
                    'null': col.nullable,
                }
                self.fields[col.name] = FIELD_MAP.get(col.type.__class__,
                    fields.CharField)(**kwargs)

    def get_resource_uri(self, bundle_or_obj=None):
        kwargs = {
            'resource_name': self._meta.resource_name,
        }

        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.id

        if self._meta.api_name is not None:
            kwargs['api_name'] = self._meta.api_name

        try:
            return self._build_reverse_url("api_dispatch_detail", kwargs=kwargs)
        except NoReverseMatch:
            return ''

    def get_object_list(self, request):
        sess = Session()
        results = []
        for obj in sess.query(self._meta.object_class).all():
            results.append(obj)
        return results

    def obj_get_list(self, request=None, **kwargs):
        return self.get_object_list(request)

    def obj_get(self, request=None, **kwargs):
        sess = Session()
        obj = sess.query(self._meta.object_class).get(kwargs['pk'])
        if not obj:
            raise NotFound('%s not found' % self._meta.resource_name)
        return obj

    def _obj_update(self, obj, data):
        for k in data:
            if hasattr(obj, k):
                setattr(obj, k, data[k])

    def obj_create(self, bundle, request=None, **kwargs):
        sess = Session()
        bundle.obj = self._meta.object_class()
        self._obj_update(bundle.obj, bundle.data)
        sess.add(bundle.obj)
        sess.commit()
        return bundle

   
    def obj_update(self, bundle, request=None, **kwargs):
        sess = Session()
        obj = sess.query(self._meta.object_class).get(kwargs['pk'])
        self._obj_update(obj, bundle.data)
        sess.commit()
        return bundle
    
    #def obj_delete_list(self, request=None, **kwargs):
    #    pass # TODO

    def obj_delete(self, request=None, **kwargs):
        sess = Session()
        obj = sess.query(self._meta.object_class).get(kwargs['pk'])
        sess.delete(obj)
        sess.commit()
