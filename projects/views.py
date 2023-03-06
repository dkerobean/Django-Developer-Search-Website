from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Project,Tag
from .forms import ProjectForm, ReviewForm
from django.contrib.auth.decorators import login_required
from .utils import searchProjects
from django.contrib import messages



def projects(request):

    search_query, projects = searchProjects(request)


    context = {
        'projects':projects,
        'search_query':search_query
    }
    return render(request,'projects/projects.html',context )


def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = projectObj
        review.owner = request.user.profile
        review.save()
        messages.success(request, 'Review submitted successfully')

        projectObj.getVoteCount
        return redirect('project', pk=projectObj.id)


    tag = projectObj.tag.all()
    context = {
    'project':projectObj,
    'tags':tag,
    'form':form
    }

    return render(request, 'projects/single-projects.html',context)


@login_required(login_url="login")
def createForm(request):
    profile = request.user.profile
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            messages.success(request, 'Project Created Successfully')
            return redirect('account')

    context = {
    'form':form
    }
    return render(request, 'projects/project_form.html', context)


@login_required(login_url="login")
def updateForm(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES,  instance=project)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {
    'form':form
    }
    return render(request, 'projects/project_form.html', context)


@login_required(login_url="login")
def deleteForm(request,pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    
    context = {
        'object':project,
    }
    return render(request, 'projects/delete_file.html',context)


