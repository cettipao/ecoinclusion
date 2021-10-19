from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib import messages


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def cooperative_verified_required(view_func):
    def wrapper_func(request, *args, **kwargs):

        cooperative = request.user.cooperativa
        if not request.user.cooperativa.verificado:
            messages.warning(request,
                        "Esta cuenta no esta Verificada como Coperativa o Empresa.  <a style=\"color:white;text-decoration: underline\" class=\"modal-trigger\" href=\"#cuentaNoVerificadaModal\">Leer Mas.</a>")
            
    
        return view_func(request, *args, **kwargs)

    
    
        logout(request)
        messages.error(request,"Se necesita una cooperativa para acceder a este sitio.")
        return redirect('register')
    return wrapper_func

def orderInteranual(lista):
    if datetime.now().month == 1:
        return [
            lista[1],
            lista[2],
            lista[3],
            lista[4],
            lista[5],
            lista[6],
            lista[7],
            lista[8],
            lista[9],
            lista[10],
            lista[11],
            lista[0],
        ]
    elif datetime.now().month == 2:
        return [
            lista[2],
            lista[3],
            lista[4],
            lista[5],
            lista[6],
            lista[7],
            lista[8],
            lista[9],
            lista[10],
            lista[11],
            lista[0],
            lista[1],
        ]
    elif datetime.now().month == 3:
        return [
            lista[3],
            lista[4],
            lista[5],
            lista[6],
            lista[7],
            lista[8],
            lista[9],
            lista[10],
            lista[11],
            lista[0],
            lista[1],
            lista[2],
        ]
    elif datetime.now().month == 4:
        return [
            lista[4],
            lista[5],
            lista[6],
            lista[7],
            lista[8],
            lista[9],
            lista[10],
            lista[11],
            lista[0],
            lista[1],
            lista[2],
            lista[3],
        ]
    elif datetime.now().month == 5:
        return [
            lista[5],
            lista[6],
            lista[7],
            lista[8],
            lista[9],
            lista[10],
            lista[11],
            lista[0],
            lista[1],
            lista[2],
            lista[3],
            lista[4],
        ]
    elif datetime.now().month == 6:
        return [
            lista[6],
            lista[7],
            lista[8],
            lista[9],
            lista[10],
            lista[11],
            lista[0],
            lista[1],
            lista[2],
            lista[3],
            lista[4],
            lista[5],
        ]
    elif datetime.now().month == 7:
        return [
            lista[7],
            lista[8],
            lista[9],
            lista[10],
            lista[11],
            lista[0],
            lista[1],
            lista[2],
            lista[3],
            lista[4],
            lista[5],
            lista[6],
        ]
    elif datetime.now().month == 8:
        return [
            lista[8],
            lista[9],
            lista[10],
            lista[11],
            lista[0],
            lista[1],
            lista[2],
            lista[3],
            lista[4],
            lista[5],
            lista[6],
            lista[7],
        ]
    elif datetime.now().month == 9:
        return [
            lista[9],
            lista[10],
            lista[11],
            lista[0],
            lista[1],
            lista[2],
            lista[3],
            lista[4],
            lista[5],
            lista[6],
            lista[7],
            lista[8],
        ]
    elif datetime.now().month == 10:
        return [
            lista[10],
            lista[11],
            lista[0],
            lista[1],
            lista[2],
            lista[3],
            lista[4],
            lista[5],
            lista[6],
            lista[7],
            lista[8],
            lista[9],
        ]
    elif datetime.now().month == 11:
        return [
            lista[11],
            lista[0],
            lista[1],
            lista[2],
            lista[3],
            lista[4],
            lista[5],
            lista[6],
            lista[7],
            lista[8],
            lista[9],
            lista[10],
        ]
    elif datetime.now().month == 12:
        return [
            lista[0],
            lista[1],
            lista[2],
            lista[3],
            lista[4],
            lista[5],
            lista[6],
            lista[7],
            lista[8],
            lista[9],
            lista[10],
            lista[11],
        ]
