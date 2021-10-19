from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib import messages

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func



def cooperative_verified_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        try:
            cooperative = request.user.cooperativa 
            if not request.user.cooperativa.verificado:
                messages.warning(request,
                            "Esta cuenta no esta Verificada como Coperativa o Empresa.  <a style=\"color:white;text-decoration: underline\" class=\"modal-trigger\" href=\"#cuentaNoVerificadaModal\">Leer Mas.</a>")
                
        
            return view_func(request, *args, **kwargs)
        except:
        
        
            logout(request)
            messages.error(request,"Se necesita una cooperativa para acceder a este sitio.")
            return redirect('register')

    return wrapper_func