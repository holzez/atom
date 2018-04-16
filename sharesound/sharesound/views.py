from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect

def home(request):
    if request.user.is_authenticated:
        return redirect('subs_list', permanent=False)
    else:
        return redirect('posts_list', permanent=False)
