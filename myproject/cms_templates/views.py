from django.shortcuts import render
from django.http import HttpResponse
from cms_templates.models import Pages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout

from django.template.loader import get_template
from django.template import Context

# Create your views here.

def barra(request):
    resp = "Las direcciones disponibles son: "
    lista_pages = Pages.objects.all()
    for page in lista_pages:
        resp += "<br>-/" + page.name + " --> " + page.page

    plantilla = get_template("miplantilla.html")
    contexto = Context({'title': "ESTO ES UNA PLANTILLA DE EJEMPLO", 'content': resp})

    return HttpResponse(plantilla.render(contexto))

@csrf_exempt
def process(request, req):
    if request.method == "GET":
        try:
            page = Pages.objects.get(name=req)
            resp = "La página solicitada es /" + page.name + " -> " + page.page
        except Pages.DoesNotExist:
            resp = "La página introducida no está en la base de datos. Créala:"
            resp += "<form action='/" + req + "' method='POST'>"
            resp += "Nombre: <input type='text' name='nombre'>"
            resp += "<br>Página: <input type='text' name='page'>"
            resp += "<input type='submit' value='Enviar'></form>"
    elif request.method == "POST":
        if request.user.is_authenticated():
            nombre = request.POST['nombre']
            page = request.POST['page']
            pagina = Pages(name=nombre, page=page)
            pagina.save()
            resp = "Has creado la página " + nombre + " con id " + str(pagina.id)
        else:
            resp = "Necesitas <a href='/admin/login'>hacer login</a>"
    elif request.method == "PUT":
        try:
            page = Pages.objects.get(name=req)
            resp = "Ya existe una página con ese nombre"
        except Pages.DoesNotExist:
            page = request.body
            pagina = Pages(name=req, page=page)
            pagina.save()
            resp = "Has creado la página " + req
    else:
        resp = "Error. Method not supported."

    resp += "<br/><br/>Eres " + request.user.username + ' <a href="/logout">haz logout</a>.'
    return HttpResponse(resp)

def milogout(request):
    logout(request)
    from django.shortcuts import redirect
    return redirect('/')
