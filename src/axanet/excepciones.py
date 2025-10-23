"""
Excepciones personalizadas para el Sistema Axanet
================================================

Este módulo define las excepciones específicas que puede generar
el sistema de gestión de clientes. Esto ayuda a manejar errores
de manera más específica y proporcionar mejores mensajes al usuario.

Jerarquía de excepciones:
- ClienteError (base)
  ├── ClienteNoEncontradoError (cliente no existe)
  ├── ClienteExisteError (cliente ya existe)
  └── ErrorValidacion (datos inválidos)
"""


class ClienteError(Exception):
    """
    Excepción base para todos los errores relacionados con clientes.
    
    Esta es la clase padre de todas las excepciones específicas del sistema.
    Permite capturar cualquier error relacionado con clientes de manera general.
    """
    
    def __init__(self, mensaje: str, nombre_cliente: str):
        """
        Inicializa la excepción con un mensaje y opcionalmente el nombre del cliente.
        
        Args:
            mensaje: Descripción del error ocurrido
            nombre_cliente: Nombre del cliente relacionado con el error (opcional)
        """
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.nombre_cliente = nombre_cliente


class ClienteNoEncontradoError(ClienteError):
    """
    Se lanza cuando se intenta buscar un cliente que no existe en el sistema.
    
    Esta excepción se usa cuando:
    - Se busca un cliente por nombre y no se encuentra
    - Se intenta modificar un cliente inexistente  
    - Se trata de eliminar un cliente que no está registrado
    """
    
    def __init__(self, nombre_cliente: str):
        """
        Inicializa la excepción para un cliente no encontrado.
        
        Args:
            nombre_cliente: El nombre del cliente que no se pudo encontrar
        """
        mensaje = f"No se encontró un cliente con el nombre '{nombre_cliente}'"
        super().__init__(mensaje, nombre_cliente)


class ClienteExisteError(ClienteError):
    """
    Se lanza cuando se intenta crear un cliente que ya existe en el sistema.
    
    Esta excepción se usa cuando:
    - Se intenta registrar un cliente con un nombre que ya está en uso
    - El sistema detecta duplicados al crear nuevos registros
    """
    
    def __init__(self, nombre_cliente: str):
        """
        Inicializa la excepción para un cliente que ya existe.
        
        Args:
            nombre_cliente: El nombre del cliente que ya está registrado
        """
        mensaje = f"Ya existe un cliente con el nombre '{nombre_cliente}'"
        super().__init__(mensaje, nombre_cliente)


class ErrorValidacion(ClienteError):
    """
    Error cuando los datos de entrada no cumplen con los requisitos de validación.
    
    Ejemplos:
    - Nombre vacío o demasiado largo
    - Teléfono con formato incorrecto 
    - Email sin formato válido
    """
    
    def __init__(self, campo: str, motivo: str):
        """
        Inicializa el error de validación.
        
        Args:
            campo: Nombre del campo que falló la validación
            motivo: Descripción específica del error
        """
        self.campo = campo
        self.motivo = motivo
        super().__init__(f"Error de validación en {campo}: {motivo}")


class ErrorArchivo(ClienteError):
    """
    Se lanza cuando ocurre un error al leer o escribir archivos.
    
    Esta excepción se usa cuando:
    - No se puede crear un archivo de cliente
    - No se puede leer un archivo existente
    - No se puede eliminar un archivo
    - Hay problemas de permisos en el sistema de archivos
    """
    
    def __init__(self, operacion: str, nombre_archivo: str, motivo: str):
        """
        Inicializa la excepción para errores de archivo.
        
        Args:
            operacion: La operación que se estaba realizando (leer, escribir, eliminar)
            nombre_archivo: El nombre del archivo involucrado
            motivo: La causa del error
        """
        mensaje = f"Error al {operacion} el archivo '{nombre_archivo}': {motivo}"
        super().__init__(mensaje)
        self.operacion = operacion
        self.nombre_archivo = nombre_archivo
        self.motivo = motivo