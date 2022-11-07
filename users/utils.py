
from django.db.models import Q
from .models import Profile, Skill


def searchProfiles(request):

    search_query = ''
    if request.GET.get('text'):
        search_query = request.GET.get('text')

    skills = Skill.objects.distinct().filter(name__icontains=search_query)

    profiles = Profile.objects.filter(
    Q(name__icontains=search_query) |
    Q(short_intro__icontains=search_query) |
    Q(skill__in = skills))

    return search_query , profiles
