# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.cache import cache_page
from django.http import HttpResponseRedirect
import settings
from common.forms import RegisterPersonForm
from django.core.context_processors import csrf
from api import Api

@cache_page(settings.caching_settings['static_page_cache_time'])
def index(request):
    return render_to_response('common/index.html', {})


def register_person(request):
    print('sdf')
    if request.method == 'POST':
        print('ee')
        form = RegisterPersonForm(request.POST)
        api = Api()
        if form.is_valid() and api.register_person(form):
            print('valid')
            return HttpResponseRedirect('/thanks?from=reg_person')
    else:
        print('saf')
        form = RegisterPersonForm() # An unbound form

    c = {'form': form}
    c.update(csrf(request))
    return render_to_response('common/forms/register_person.html', c)

@cache_page(settings.caching_settings['static_page_cache_time'])
def thanks(request):
    ref = request.GET['from']
    ref2msg = {'reg_person': 'Пользователь успешно зарегистрирован.'}
    return render_to_response('common/thanks.html', {'message': ref2msg[ref]})
