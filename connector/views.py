from django.shortcuts import render
from django.http import HttpResponse

from . import ResponseHandler

# /
def view_index(request, *args, **kwargs):
    return HttpResponse('<h1>index</h1>')

# /projects/
def view_projects(request, *args, **kwargs):
    return HttpResponse(ResponseHandler.ResponseHandler.handle(request))

# /project/create/
def view_project_create(request):
    return HttpResponse(ResponseHandler.ResponseHandler.create_project(request))

# /project/5
def view_project(request, id_project):
    return HttpResponse(ResponseHandler.ResponseHandler.handle(request))

# /project/5/servers
def view_servers(request, id_project):
    return HttpResponse(ResponseHandler.ResponseHandler.handle(request))

# /project/5/server/5
def view_server(request, id_project, id_server):
    return HttpResponse(ResponseHandler.ResponseHandler.handle(request))
