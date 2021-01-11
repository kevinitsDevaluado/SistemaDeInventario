from datetime import datetime

from django.db import models
from django.forms import model_to_dict

from config.settings import MEDIA_URL, STATIC_URL
from core.erp.choices import gender_choices
from core.erp.validators import vcedula,validacionCantidad,validacionNacimiento
from core.models import BaseModel

#TABLA CATEGORIA
class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['id']

#TABLA PROVEEDOR
class Suppliers(models.Model):
    ruc = models.CharField(max_length=10, verbose_name='Cédula',validators=[vcedula])
    names = models.CharField(max_length=150, verbose_name='Nombres')
    direccion = models.CharField(max_length=150, verbose_name='Direccion')


    def __str__(self):
        return self.ruc

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['id']
#TABLA MATERIA PRIMA
class RawMaterial(models.Model):
    nombre = models.CharField(max_length=15, verbose_name='Nombre')
    descripcion = models.CharField(max_length=150, verbose_name='Descripcion')
    cant = models.IntegerField(default=00000, null=True, blank=True,verbose_name='Cantidad')
    prov = models.ForeignKey(Suppliers, on_delete=models.CASCADE, verbose_name='Proveedor')
    date_ven = models.DateField(default=datetime.now, verbose_name='Fecha de Vencimiento')
    date_add = models.DateField(default=datetime.now, verbose_name='Fecha de Creación')
    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        item['prov'] = self.prov.toJSON()
        item['date_ven'] = self.date_birthday.strftime('%Y-%m-%d')
        item['date_add'] = self.date_birthday.strftime('%Y-%m-%d')
        return item

    class Meta:
        verbose_name = 'Materia Prima'
        verbose_name_plural = 'Materia Prima'
        ordering = ['id']
#TABLA PRODUCTO
class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    cat = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Categoría')
    image = models.ImageField(upload_to='product/%Y/%m/%d', null=False, blank=True, verbose_name='Imagen')
    cant = models.IntegerField(default=00000, null=True, blank=True)
    pvp = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Precio de venta',validators=[validacionCantidad])

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        item['cat'] = self.cat.toJSON()
        item['image'] = self.get_image()
        item['pvp'] = format(self.pvp, '.2f')
        return item

    def get_image(self):
        if self.image:
            return '{}{}'.format(MEDIA_URL, self.image)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['id']
        
        #fields = []
        #fields = ['cat','name','image','cant','pvp']
        #order_with_respect_to = 'cat'
#TABLA CARGAR PRODUCTO
class CargarProducto(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cant = models.IntegerField(default=00000,validators=[validacionCantidad],null=True, blank=True)
    fechaIngreso = models.DateField(default=datetime.now, verbose_name='Fecha de Ingreso',null=True, blank=True)
    observacion = models.CharField(max_length=150, null=True, blank=True, verbose_name='Observacion')
    
    def __str__(self):
        return self.product.names  
    
    def toJSON(self):
        item = model_to_dict(self)
        item['product'] = self.product.toJSON()
        #item['gender'] = {'id': self.gender, 'name': self.get_gender_display()}
        item['fechaIngreso'] = self.fechaIngreso.strftime('%Y-%m-%d')
        #item['full_name'] = self.get_full_name()
        return item 

#TABLA CLIENTE
class Client(models.Model):
    names = models.CharField(max_length=150, verbose_name='Nombres')
    surnames = models.CharField(max_length=150, verbose_name='Apellidos')
    dni = models.CharField(max_length=10, unique=True, verbose_name='Cédula',validators=[vcedula])
    date_birthday = models.DateField(default=datetime.now, verbose_name='Fecha de nacimiento' )
    address = models.CharField(max_length=150, null=True, blank=True, verbose_name='Dirección')
    gender = models.CharField(max_length=10, choices=gender_choices, default='male', verbose_name='Sexo')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return '{} {} / {}'.format(self.names, self.surnames, self.dni)

    def toJSON(self):
        item = model_to_dict(self)
        item['gender'] = {'id': self.gender, 'name': self.get_gender_display()}
        item['date_birthday'] = self.date_birthday.strftime('%Y-%m-%d')
        item['full_name'] = self.get_full_name()
        return item

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['id']

#TABLA FACTURA
class Sale(models.Model):
    cli = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_joined = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.cli.names

    def toJSON(self):
        item = model_to_dict(self)
        item['cli'] = self.cli.toJSON()
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['total'] = format(self.total, '.2f')
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['det'] = [i.toJSON() for i in self.detsale_set.all()]
        return item

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['id']

#TABLA FACTURA
class DetSale(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    prod = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant = models.IntegerField(default=0,validators=[validacionCantidad])
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.prod.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['sale'])
        item['prod'] = self.prod.toJSON()
        item['price'] = format(self.price, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalle de Ventas'
        ordering = ['id']
