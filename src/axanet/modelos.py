"""
Modelos de Datos para el Sistema Axanet
======================================

Este módulo contiene las clases que representan los datos principales
del sistema: Cliente y Servicio. Estas clases manejan la validación
de datos y la conversión entre diferentes formatos.

Las clases son simples pero demuestran conceptos importantes:
- Validación de datos de entrada
- Normalización de nombres para uso como claves
- Serialización de datos para archivos
- Manejo de fechas y timestamps
"""

from datetime import datetime
from typing import List
import re

from .excepciones import ErrorValidacion


class Servicio:
    """
    Representa un servicio solicitado por un cliente.
    
    Un servicio contiene:
    - Descripción del trabajo solicitado
    - Fecha y hora cuando fue solicitado
    """
    
    def __init__(self, descripcion: str, fecha_solicitud: str):
        """
        Crea un nuevo servicio.
        
        Args:
            descripcion: Descripción del servicio solicitado
            fecha_solicitud: Fecha del servicio (opcional, se usa la fecha actual)
        """
        self.descripcion = descripcion.strip()
        
        # Si no se proporciona fecha, usar la fecha actual
        if fecha_solicitud:
            self.fecha_solicitud = fecha_solicitud
        else:
            # Crear timestamp en formato legible
            ahora = datetime.now()
            self.fecha_solicitud = ahora.strftime("%Y-%m-%d %H:%M:%S")
    
    def __str__(self):
        """Representación en texto del servicio."""
        return f"{self.descripcion} ({self.fecha_solicitud})"


class Cliente:
    """
    Representa un cliente del sistema Axanet.
    
    Un cliente contiene:
    - Información personal (nombre, teléfono, email)
    - ID único generado automáticamente
    - Fecha de registro
    - Lista de servicios solicitados
    """
    
    def __init__(self, nombre: str, telefono: str, email: str):
        """
        Crea un nuevo cliente con validación de datos.
        
        Args:
            nombre: Nombre completo del cliente
            telefono: Número de teléfono
            email: Dirección de correo electrónico
        """
        # Guardar datos básicos (se validarán después)
        self.nombre = nombre.strip()
        self.telefono = telefono.strip()
        self.email = email.strip()
        
        # Inicializar otros campos
        self.servicios: List[Servicio] = []
        self.id_cliente = ""  # Se genera después
        
        # Generar fecha de registro
        ahora = datetime.now()
        self.fecha_registro = ahora.strftime("%Y-%m-%d")
        
        # Validar todos los datos
        self.validar_datos()
    
    @property
    def nombre_normalizado(self) -> str:
        """
        Genera un nombre normalizado para usar como clave en la tabla hash.
        
        Convierte "Ana García López" → "ana_garcia_lopez"
        Esto es importante para:
        - Evitar problemas con caracteres especiales en nombres de archivos
        - Crear claves consistentes para la tabla hash
        - Permitir búsquedas case-insensitive
        
        Returns:
            Nombre normalizado sin espacios ni caracteres especiales
        """
        # Convertir a minúsculas y reemplazar espacios con guiones bajos
        normalizado = self.nombre.lower()
        
        # Reemplazar caracteres especiales comunes
        reemplazos = {
            'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
            'ñ': 'n', 'ç': 'c', ' ': '_'
        }
        
        for original, reemplazo in reemplazos.items():
            normalizado = normalizado.replace(original, reemplazo)
        
        # Eliminar caracteres que no sean letras, números o guiones bajos
        normalizado = re.sub(r'[^a-z0-9_]', '', normalizado)
        
        return normalizado
    
    def validar_datos(self):
        """
        Valida todos los datos del cliente.
        
        Verifica que:
        - El nombre no esté vacío
        - El teléfono tenga formato válido
        - El email tenga formato válido
        
        Raises:
            ErrorValidacion: Si algún dato es inválido
        """
        # Validar nombre
        if not self.nombre or len(self.nombre.strip()) < 2:
            raise ErrorValidacion(
                campo="nombre",
                valor=self.nombre,
                motivo="El nombre debe tener al menos 2 caracteres"
            )
        
        # Validar teléfono (debe tener 10 dígitos)
        telefono_limpio = re.sub(r'[^\d]', '', self.telefono)
        if len(telefono_limpio) != 10:
            raise ErrorValidacion(
                campo="telefono",
                valor=self.telefono,
                motivo="El teléfono debe tener exactamente 10 dígitos"
            )
        
        # Actualizar teléfono con formato limpio
        self.telefono = telefono_limpio
        
        # Validar email con expresión regular simple
        patron_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(patron_email, self.email):
            raise ErrorValidacion(
                campo="email",
                valor=self.email,
                motivo="El formato del email no es válido"
            )
    
    def generar_id_cliente(self) -> str:
        """
        Genera un ID único para el cliente.
        
        Formato: Iniciales + timestamp
        Ejemplo: "AG_20241022143045" para Ana García creada el 22/10/2024 14:30:45
        
        Returns:
            ID único del cliente
        """
        # Obtener las primeras dos letras de cada palabra del nombre
        palabras = self.nombre.split()
        iniciales = ""
        
        for palabra in palabras[:2]:  # Máximo 2 palabras para las iniciales
            if palabra:  # Verificar que la palabra no esté vacía
                iniciales += palabra[0].upper()
        
        # Si solo hay una palabra o iniciales muy cortas, completar
        if len(iniciales) < 2:
            iniciales = (iniciales + self.nombre[:2].upper())[:2]
        
        # Generar timestamp
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        
        # Combinar iniciales y timestamp
        id_cliente = f"{iniciales}_{timestamp}"
        
        return id_cliente
    
    def agregar_servicio(self, descripcion: str):
        """
        Agrega un nuevo servicio a la lista del cliente.
        
        Args:
            descripcion: Descripción del servicio a agregar
            
        Raises:
            ErrorValidacion: Si la descripción está vacía
        """
        if not descripcion or not descripcion.strip():
            raise ErrorValidacion(
                campo="descripcion_servicio",
                valor=descripcion,
                motivo="La descripción del servicio no puede estar vacía"
            )
        
        # Crear nuevo servicio con la fecha actual
        nuevo_servicio = Servicio(descripcion, None)
        self.servicios.append(nuevo_servicio)
    
    def a_formato_archivo(self) -> str:
        """
        Convierte los datos del cliente al formato de archivo de texto.
        
        Genera un texto en el formato requerido por la actividad:
        ```
        Nombre: Ana Garcia
        ID_Cliente: AG_20241022143045
        Telefono: 5512345678
        Correo: ana.garcia@email.com
        FechaRegistro: 2024-10-22
        Servicios:
        - Solicitud de manufactura de pieza X (2024-10-22 14:30:45)
        - Solicitud de diseño de prototipo Y (2024-10-22 15:45:30)
        ```
        
        Returns:
            Contenido del archivo como string
        """
        contenido = []
        
        # Información básica del cliente
        contenido.append(f"Nombre: {self.nombre}")
        contenido.append(f"ID_Cliente: {self.id_cliente}")
        contenido.append(f"Telefono: {self.telefono}")
        contenido.append(f"Correo: {self.email}")
        contenido.append(f"FechaRegistro: {self.fecha_registro}")
        
        # Lista de servicios
        contenido.append("Servicios:")
        for servicio in self.servicios:
            contenido.append(f"- {servicio.descripcion} ({servicio.fecha_solicitud})")
        
        return "\n".join(contenido)
    
    @classmethod
    def desde_archivo(cls, contenido_archivo: str) -> 'Cliente':
        """
        Crea un cliente a partir del contenido de un archivo.
        
        Lee un archivo en el formato esperado y reconstruye el objeto Cliente.
        
        Args:
            contenido_archivo: Contenido del archivo como string
            
        Returns:
            Instancia de Cliente con los datos cargados
        """
        lineas = contenido_archivo.strip().split('\n')
        
        # Extraer información básica
        nombre = ""
        telefono = ""
        email = ""
        id_cliente = ""
        fecha_registro = ""
        
        servicios_seccion = False
        servicios_encontrados = []
        
        for linea in lineas:
            linea = linea.strip()
            
            if linea.startswith("Nombre:"):
                nombre = linea.split(":", 1)[1].strip()
            elif linea.startswith("ID_Cliente:"):
                id_cliente = linea.split(":", 1)[1].strip()
            elif linea.startswith("Telefono:"):
                telefono = linea.split(":", 1)[1].strip()
            elif linea.startswith("Correo:"):
                email = linea.split(":", 1)[1].strip()
            elif linea.startswith("FechaRegistro:"):
                fecha_registro = linea.split(":", 1)[1].strip()
            elif linea == "Servicios:":
                servicios_seccion = True
            elif servicios_seccion and linea.startswith("- "):
                # Extraer descripción y fecha del servicio
                servicio_texto = linea[2:]  # Quitar "- "
                
                # Buscar la fecha entre paréntesis al final
                if "(" in servicio_texto and ")" in servicio_texto:
                    # Separar descripción y fecha
                    partes = servicio_texto.rsplit("(", 1)
                    if len(partes) == 2:
                        descripcion = partes[0].strip()
                        fecha_parte = partes[1].rstrip(")")
                        servicios_encontrados.append((descripcion, fecha_parte))
                    else:
                        # Si no se puede parsear la fecha, usar solo la descripción
                        servicios_encontrados.append((servicio_texto, None))
                else:
                    servicios_encontrados.append((servicio_texto, None))
        
        # Crear cliente con los datos básicos
        cliente = cls(nombre=nombre, telefono=telefono, email=email)
        
        # Asignar campos que no se validan en __init__
        cliente.id_cliente = id_cliente
        cliente.fecha_registro = fecha_registro
        
        # Agregar servicios
        for descripcion, fecha in servicios_encontrados:
            servicio = Servicio(descripcion, fecha)
            cliente.servicios.append(servicio)
        
        return cliente
    
    def __str__(self):
        """Representación en texto del cliente."""
        return f"{self.nombre} (ID: {self.id_cliente}, Servicios: {len(self.servicios)})"
    
    def __repr__(self):
        """Representación técnica del cliente."""
        return f"Cliente(nombre='{self.nombre}', telefono='{self.telefono}', email='{self.email}')"