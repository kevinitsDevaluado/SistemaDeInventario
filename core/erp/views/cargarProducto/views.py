from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.http import JsonResponse
import json
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.erp.forms import ProductForm, CargarProductoForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import CargarProducto, Product


class CargarProductoListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = CargarProducto
    template_name = 'cargarProducto/list.html'
    #permission_required = 'view_product', 'change_product', 'delete_product', 'add_product'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in CargarProducto.objects.all():
                    data.append(i.toJSON())
                print(data) 
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de las Cargas del Producto'
        context['create_url'] = reverse_lazy('erp:cargarProducto_create')
        context['list_url'] = reverse_lazy('erp:cargarProducto_list')
        context['entity'] = 'Cargar Productos'
        return context


class CargarProductoCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = CargarProducto
    form_class = CargarProductoForm
    template_name = 'cargarProducto/create.html'
    success_url = reverse_lazy('erp:cargarProducto_list')
    permission_required = 'add_product'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                
                #AQUI GUARDAMOS EL FORMULARIO CON LA AYUDA DEL METODO SAVE() QUE ESTA EL FORM
                form = self.get_form()
                data = form.save()

                
                #AQUI TRAEMOS LA INFORMACION CON LA AYUDA DEL GET -- DEL FORMULARIO DE PRODUCTOCARGAR
                id_producto = request.POST.get('product')
                cantidad = request.POST.get('cant')
                #CON LA VARIABLE P1 TRAEMOS EL PRODUCTO QUE VAMOS A CARGAR CON LA AYUDA DEL GET
                p1 = Product.objects.get(id=id_producto)
                #REALIZAMOS LA OPERACION CORRESPONDIETE A SUMAR PRIMERO TRAEMOS LA CANTIDAD ACTUAL DEL PRODUCTO PARA
                #LUEGO SUMARLO CON LA CANTIDAD QUE INGRESAMOS EL PRODUCOT
                cantidad_actual = p1.cant #0
                sum = int(cantidad_actual)+int(cantidad)
                p1.cant = sum
                #UNA VES REALIZADO TODAS LAS OPERACIONES GUARDAMOS
                p1.save()

                return HttpResponse(json.dumps("cantidad_actual: "+str(p1.cant)+", cantidad_form: "+str(cantidad_actual)+"sum: "+str(sum)), content_type="application/json")
              
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
    
        except Exception as e:
            data['error'] = str(e)
        print(data)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cargar Producto'
        context['entity'] = 'Cargar Productos'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

class CargarProductoUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = CargarProducto
    form_class = ProductForm
    template_name = 'cargarProduct/create.html'
    success_url = reverse_lazy('erp:cargarProducto_list')
    permission_required = 'change_product'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de un Producto'
        context['entity'] = 'Productos'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class CargarProductoDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = CargarProducto
    template_name = 'cargarProducto/delete.html'
    success_url = reverse_lazy('erp:cargarProducto_list')
    permission_required = 'delete_product'
    url_redirect = success_url

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de la Carga del producto'
        context['entity'] = 'Carga de Productos'
        context['list_url'] = self.success_url
        return context
