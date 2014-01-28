from django.shortcuts import render
from django.views.generic.base import View
# Create your views here.
from nurses.db import Session
from admin.models import Nurse
from admin.forms import NurseForm

class ListNurses(View):
    
    def get(self, request, *args, **kwargs):
        nurses = Session().query(Nurse).all()
        form = NurseForm()
        return render(request, "admin/nurses_list.html",
                      {"nurses": nurses,
                       "form": form,
                       "angular_app": "NursesApp"
                   })
        

