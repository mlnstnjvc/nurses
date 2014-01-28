from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
from parameters.models import Parameter
from nurses.db import Session
from .forms import ParamForm
from django.shortcuts import render

from django.views.generic.base import View


def param(request, id_par):
    print(id_par)
    return HttpResponse("hello {par}".format(par=id_par))

class ListParams(View):
    def get(self, request, *args, **kwargs):
        session = Session()
        params = session.query(Parameter).all()
        return render(request, "parameters/list.html", {"params": params})

class CreateParam(View):
    form_cls = ParamForm
    title = "Create Parameter"
    def get(self, request, *args, **kwargs):
        form = self.form_cls()
        context = dict(
            form = form,
            title = self.title)
        return render(request, "parameters/create.html", context)
    
    def post(self, request, *args, **kwargs):
        
        form = self.form_cls(request.POST)

        if form.is_valid():
            param = Parameter(id_par = form.cleaned_data['id'],
                              number = form.cleaned_data['value'],
                              text = form.cleaned_data['text'],
                              id_scenario = "dummy")

            session = Session()
            session.add(param)
            session.commit()

            return HttpResponseRedirect("/params/list")

        context = dict(
            form = form,
            title = self.title)
        return render(request, "parameters/create.html", context)
            

class EditParam(View):
    form_cls = ParamForm
    title = "Edit parameter"
    def get(self, request, id_par, *args, **kwargs):
        session = Session()
        param = session.query(Parameter).filter_by(id_par=id_par).first()
        form = self.form_cls(dict(
            id = param.id_par,
            value = param.number,
            text = param.text))
        context = dict(
            title = self.title,
            form = form,
            param = param)
        
        return render(request, "parameters/create.html", context)

    def post(self, request, id_par, *args, **kwargs):
        """
        
        Arguments:
        - `request`:
        - `id_par`:
        - `*args`:
        - `**kwargs`:
        """
        
        session = Session()
        param = session.query(Parameter).filter_by(id_par=id_par).first()
        form = self.form_cls(request.POST)
        if form.is_valid():
            
            data = form.cleaned_data
            param.id_par = data['id']
            param.number = data['value']
            param.text = data['text']

            session.commit()
            
        context = dict(
            form = form,
            title = self.title,
            param = param)

        return render(request, "parameters/create.html", context)
        
        

        

