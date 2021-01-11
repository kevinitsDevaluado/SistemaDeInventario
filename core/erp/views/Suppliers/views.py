from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.erp.forms import SuppliersForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Suppliers


class SuppliersListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Suppliers
    template_name = 'Suppliers/list.html'
    permission_required = 'erp.view_suppliers'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                position = 1
                for i in Suppliers.objects.all():
                    item = i.toJSON()
                    item['position'] = position
                    data.append(item)
                    position += 1
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Proveedores'
        context['create_url'] = reverse_lazy('erp:suppliers_create')
        context['list_url'] = reverse_lazy('erp:suppliers_list')
        context['entity'] = 'Proveedores'
        return context


class SuppliersCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Suppliers
    form_class = SuppliersForm
    template_name = 'Suppliers/create.html'
    success_url = reverse_lazy('erp:suppliers_list')
    permission_required = 'erp.add_suppliers'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación un Proveedor|'
        context['entity'] = 'Proveedor'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class SuppliersUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Suppliers
    form_class = SuppliersForm
    template_name = 'Suppliers/create.html'
    success_url = reverse_lazy('erp:suppliers_list')
    permission_required = 'erp.change_suppliers'
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
        context['title'] = 'Edición un Proveedor'
        context['entity'] = 'Proveedor'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class SuppliersDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Suppliers
    template_name = 'Suppliers/delete.html'
    success_url = reverse_lazy('erp:suppliers_list')
    permission_required = 'erp.delete_category'
    url_redirect = success_url

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
        context['title'] = 'Eliminación de un Proveedor'
        context['entity'] = 'Proveedor'
        context['list_url'] = self.success_url
        return context
