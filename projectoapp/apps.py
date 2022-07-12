from django.apps import AppConfig
from .models import Contact, Project, ProjectReview, Student, ProjectStatus, Employee
from .modelMgr import FileModelMgr
from django.conf import settings

projectModelMgr = FileModelMgr(Project, settings.DATA_FILE_PATH['Project'])
projectModelMgr.load()
employeeModleMgr = FileModelMgr(Employee, settings.DATA_FILE_PATH['Employee'])
employeeModleMgr.load()
projectRevMdlMgr = FileModelMgr(ProjectReview, settings.DATA_FILE_PATH['ProjectReview'])
projectRevMdlMgr.load()
studentMdlMgr = FileModelMgr(Student, settings.DATA_FILE_PATH['Student'])
studentMdlMgr.load()
contactMdlMgr = FileModelMgr(Contact, settings.DATA_FILE_PATH['Contact'])
contactMdlMgr.load()

class ProjectoappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'projectoapp'
