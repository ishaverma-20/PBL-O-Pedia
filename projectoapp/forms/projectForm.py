from email.policy import default
from multiprocessing import Value
import datetime
from random import choices
from xmlrpc.client import DateTime
from django import forms
from django.core.exceptions import ValidationError
from ..apps import projectRevMdlMgr,projectModelMgr,employeeModleMgr
from ..models import ProjectReview, Project,ProjectStatus

def validate_email_domain(value):
    if len(value.split("@")) != 2 :
        raise ValidationError("The email address must have single @ character")


class ProjectReviewForm(forms.Form):
    project_id = forms.CharField()
    review_com = forms.CharField()
    rating= forms.ChoiceField(choices = (('1',1),('2',2),('3',3),('4',4),('5',5)))
    user_name= forms.CharField()
    
    def setProject_Id(self,id):
        self['project_id'].value = id
    
    def clean(self):
        cleaned_data = super().clean()
        
    def Save(self):
 
        projectRvw = ProjectReview({'id':None,'project_id':self.cleaned_data['project_id'], 'user_name':self.cleaned_data['user_name'],
                     'creation_date':datetime.date.today().strftime("%d/%m/%Y"),'review_com':self.cleaned_data['review_com'],
                     'rating':self.cleaned_data['rating']})
        projectRevMdlMgr.add(projectRvw)


def create_prj_coordinator_list():
    return [(id, employee.name) for id, employee in employeeModleMgr.all().items() ]

def get_prj_coordinator_list():
    if not get_prj_coordinator_list.prj_coordinator_list:
        get_prj_coordinator_list.prj_coordinator_list = create_prj_coordinator_list() 
    return get_prj_coordinator_list.prj_coordinator_list

get_prj_coordinator_list.prj_coordinator_list=None

class ProjectForm(forms.Form):
    id = forms.CharField()
    name = forms.CharField(required=True)
    domain = forms.CharField(required=True)
    div = forms.CharField(required=True)
    coordinatior_id = forms.ChoiceField(required=True)
    status=  forms.ChoiceField(choices = [(status.value,status.name) for status in ProjectStatus], required=True)

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['coordinatior_id'] = forms.ChoiceField(choices=get_prj_coordinator_list(),required=True)
    
    def set_Coordinator(self,choiceField):
        #chfield = self.fields['coordinatior_id']
        #self.fields['coordinatior_id'] = forms.ChoiceField(choices=choiceField,initial=chfield.initial,required=True)
   #     chfield.field.choices = choiceField
        pass
        
    def clean(self):
        cleaned_data = super().clean()
        
    def Save(self):
        projectObj = Project(self.cleaned_data)
        projectModelMgr.update(projectObj)
        
        