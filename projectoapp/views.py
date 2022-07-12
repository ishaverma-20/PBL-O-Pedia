from http.client import BAD_REQUEST
from itertools import count
from xml.dom import ValidationErr
from django.http import Http404, HttpResponseServerError
from django.shortcuts import redirect, render, get_object_or_404
from .apps import projectModelMgr, employeeModleMgr,studentMdlMgr,projectRevMdlMgr, contactMdlMgr
from django.conf import settings
from .forms.projectForm import ProjectForm, ProjectReviewForm

import re

def index(request):

    context = {
        'total_projects': len(projectModelMgr.all()),
        'total_students': len(studentMdlMgr.all())
    }

    return render(request, "projectoapp/base.html", context)


def project_search(request):
    prj_name = request.GET.get("prj_name", "")
    projList = proj_search(prj_name) if prj_name and prj_name.strip() else None
    context = {
        "project_list": projList,
        "total_projects": len(projList) if projList else 0
    }
    return render(request, "projectoapp/search_results.html", context)


def project_list(request):

    prj_list = proj_search()
    context = {
        "total_projects":  len(prj_list),
        "project_list": prj_list
    }
    return render(request, "projectoapp/project_list.html", context)


def proj_search(name='*') -> list[dict[str, object]]:

    projects = projectModelMgr.all()
    employees = employeeModleMgr.all()
    serachAll = name == '*'
    prj_list = []

    for id, project in projects.items():
        if serachAll or re.match(name, project.name, re.IGNORECASE):
            coordinator = employees.get(project.coordinatior_id)
            prj_list.append({'project': project, 'coordinator': coordinator})

    return prj_list


def project_action(request, Id):

    if not (project := projectModelMgr.get(Id)):
        raise Http404("Given project id:%s  not found....", Id)

    operation = request.GET.get("op", "")
    if operation == "review":
        return project_detail(request, project, True)

    elif operation == "modify":
        return project_modify(request, project)
    else:
        return project_detail(request, project)


def project_detail(request, project, doReview=False):

    Id = project.id
    projectRvws = projectRevMdlMgr.all()
    projectStudents = studentMdlMgr.all()
    reviews = [projectRvw for id, projectRvw in projectRvws.items()
                                                                  if projectRvw.project_id == Id]
    students = [projectStudent for id, projectStudent in projectStudents.items(
    ) if projectStudent.project_id == Id]
    coordinator = employeeModleMgr.get(project.coordinatior_id)
    project_rating = None
    if len(reviews):
        project_rating = sum(int(review.rating) for review in reviews)
        project_rating = project_rating/len(reviews)
    else:
        reviews = None

    context = {
           "project": project,
           "project_rating": project_rating,
            "coordinator": coordinator,
            "reviews": reviews,
            "students": students
        }
    pageUrl = "projectoapp/project_detail.html"

    if doReview:
        pageUrl = "projectoapp/project_review.html"
        form = ProjectReviewForm()
        form.setProject_Id(Id)
        context['form'] = form
        context['op']='review'

    return render(request, pageUrl, context)


def project_modify(request, project):
    projFormObj = project.get_dictObj()
    projectForm = ProjectForm(initial=projFormObj)

    context = {
        "form": projectForm,
    }
    return render(request,"projectoapp/project_opr.html",context)

def project_update(request, Id):

    if request.method != "POST":
        raise Http404("Invalid operation")

    opreation= request.GET.get("op", "")

    if opreation not in ['review', 'proj']:
        raise Http404("Invalid operation")

    formObj = ProjectReviewForm(request.POST) if  opreation == 'review' else ProjectForm(request.POST)

    if formObj.is_valid():
        formObj.Save()
    else:
        print(formObj.errors)
        return HttpResponseServerError(f"Failed while validating information:{formObj.errors}" )

    return redirect(project_action, Id=Id)


def project_create(request):
    pass


def project_delete(request, Id):
    pass

def project_contact(request):

    prj_contact = [ contact for id, contact in contactMdlMgr.all().items() ]
    context = {
        "contact_list":  prj_contact
    }
    return render(request, "projectoapp/contact.html", context)