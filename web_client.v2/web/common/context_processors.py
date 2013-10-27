from django.core.context_processors import csrf

def add_csrf_token(request):
    return csrf(request)
