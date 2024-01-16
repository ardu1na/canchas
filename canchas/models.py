from datetime import date
from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    date_created = models.DateField(auto_now_add=True)
    deleted = models.BooleanField(default=False, editable=False)
    date_deleted = models.DateTimeField(null=True, blank=True, editable=False)
    
    def delete(self, *args, **kwargs):
        self.deleted = True
        self.date_deleted = date.today
        self.save() 
        print (f' item {self.id} has been send to trash')

    class Meta:
        abstract = True


class Foto(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    archivo = models.ImageField()

    def __str__ (self):
        return self.titulo



class Contacto(models.Model):
    whatsapp_number = models.CharField(max_length=200, null=True, blank=True)
    phone_number = models.CharField(max_length=200, null=True, blank=True)
    fiscal = models.TextField(null=True, blank=True)
    bancario = models.TextField(null=True, blank=True)
    direccion = models.CharField(max_length=300, null=True, blank=True)

class Persona (models.Model):
    CANCHA_ADMIN = 'CANCHA ADMIN'
    CANCHA_EMPLEADO = 'CANCHA EMPLEADO'
    CANCHA_CLIENTE = 'CANCHA CLIENTE'

    ROL_CHOICES = (
        (CANCHA_ADMIN, ('CANCHA ADMIN')),
        (CANCHA_EMPLEADO, ('CANCHA EMPLEADO')),
        (CANCHA_CLIENTE, ('CANCHA CLIENTE')),
    )

    rol = models.CharField(choices=ROL_CHOICES, max_length=40)
    contacto = models.OneToOneField(Contacto, related_name="persona", on_delete=models.DO_NOTHING, null=True, blank=True)
    user = models.OneToOneField(User, related_name="persona", on_delete=models.DO_NOTHING, null=True, blank=True)

class Empresa(models.Model):
    nombre = models.CharField(max_length=200)
    ubicacion = models.CharField(max_length=400, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    admin = models.OneToOneField(Persona, on_delete=models.DO_NOTHING, null=True, blank=True)
    fotos = models.ManyToManyField(Foto, null=True, blank=True)
    

    def __str__ (self):
        return self.nombre
"""
class CategoriaEmpleado(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__ (self):
        return self.nombre
    
class Empleado(models.Model):
    persona = models.OneToOneField(Persona, on_delete=models.DO_NOTHING)
    cancha = models.ForeignKey('Empresa', related_name="empleados", on_delete=models.DO_NOTHING)    
    categoria = models.ForeignKey(CategoriaEmpleado, on_delete=models.DO_NOTHING, related_name="empleados")
    dni = models.PositiveIntegerField(null=True, blank=True)

class FrancoLaboral(models.Model):
    fecha = models.DateField()

class Vacacion(models.Model):
    empleado = models.ForeignKey(Empleado, related_name="vacaciones", on_delete=models.DO_NOTHING)
    fecha_inicio = models.DateField()
    fecha_final = models.DateField()
    observaciones = models.TextField(blank=True, null=True)

class Salario(models.Model):
    empleado = models.ForeignKey(Empleado, related_name="vacaciones", on_delete=models.DO_NOTHING)
    #monto #periodo """

class CategoriaGasto(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__ (self):
        return self.nombre
    
class Gasto(BaseModel):
    empresa = models.ForeignKey(Empresa, on_delete=models.DO_NOTHING, related_name="gastos")
    concepto = models.CharField(max_length=400)
    categoria = models.ForeignKey(CategoriaGasto, on_delete=models.DO_NOTHING, related_name="gastos")
    monto = models.DecimalField(decimal_places=2, max_digits=15)
    observaciones = models.TextField(null=True, blank=True)

    def __str__ (self):
        return f'${self.monto} en concepto de {self.concepto} | {self.date_created}'


class CategoriaProveedor(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__ (self):
        return self.nombre
    
class Proveedor(models.Model):
    contacto = models.OneToOneField(Contacto, on_delete=models.DO_NOTHING, related_name="proveedor")
    empresa = models.CharField(max_length=400)
    categoria = models.ForeignKey(CategoriaProveedor, on_delete=models.DO_NOTHING, related_name="proveedores")
    observaciones = models.TextField(null=True, blank=True)

class CategoriaIngreso(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__ (self):
        return self.nombre  
      
class Ingreso(BaseModel):
    concepto = models.CharField(max_length=400, null=True, blank=True)
    categoria = models.ForeignKey(CategoriaIngreso, on_delete=models.DO_NOTHING, related_name="ingresos")
    monto = models.DecimalField(decimal_places=2, max_digits=15)
    observaciones = models.TextField(null=True, blank=True)

    def __str__ (self):
        return f'${self.monto}  {self.categoria} | {self.date_created}'
    

class CategoriaProducto(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__ (self):
        return self.nombre    

class VentaProducto(BaseModel):
    producto =  models.ForeignKey('Producto', on_delete=models.DO_NOTHING, related_name="productos")
    cantidad = models.PositiveSmallIntegerField(default=1)
    ingreso = models.OneToOneField(Ingreso, on_delete=models.DO_NOTHING)
    reserva = models.ForeignKey('Reserva', related_name="ventas", on_delete=models.DO_NOTHING, blank=True, null=True)
    persona = models.ForeignKey(Persona, related_name="ventas", on_delete=models.DO_NOTHING, blank=True, null=True)

class Producto(models.Model):
    categoria = models.ForeignKey(CategoriaProducto, on_delete=models.DO_NOTHING, related_name="productos")
    stock = models.PositiveSmallIntegerField(default=0)
    nombre = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=15, decimal_places=2)
    proovedor = models.ForeignKey(Proveedor, related_name="productos", on_delete=models.DO_NOTHING)


class CategoriaCancha(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__ (self):
        return self.nombre
    
class Cancha(models.Model):
    empresa = models.ForeignKey(Empresa, related_name="canchas", on_delete=models.DO_NOTHING)
    nombre = models.CharField(max_length=200)
    categoria = models.ForeignKey(CategoriaCancha, on_delete=models.DO_NOTHING, related_name="canchas")
    caractersticas = models.TextField(null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    fotos = models.ManyToManyField(Foto, null=True, blank=True)

    def __str__(self):
        return f'CANCHA {self.categoria} :  {self.nombre}'
    
class PagoReserva(BaseModel):
    reserva = models.ForeignKey('Reserva', related_name="pagos", on_delete=models.DO_NOTHING)
    ingreso = models.OneToOneField(Ingreso, on_delete=models.DO_NOTHING)


class Reserva(BaseModel):
    cancha = models.ForeignKey(Cancha, related_name="reservas", on_delete=models.DO_NOTHING)
    personas = models.ManyToManyField(Persona, related_name="canchas", null=True, blank=True)
    a_nombre_de = models.ForeignKey(Persona, related_name="reservas", on_delete=models.DO_NOTHING, null=True, blank=True)

    hora_inicio = models.DateTimeField()
    hora_finalizacion = models.DateTimeField()
    
    observaciones = models.TextField(blank=True, null=True)

    total = models.DecimalField(decimal_places=2, max_digits=15, default=0)
    pagado = models.BooleanField(default=False)