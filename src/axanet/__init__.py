"""
Paquete Sistema de Gestión de Clientes Axanet
=============================================

Sistema académico simplificado para gestión de clientes de telecomunicaciones.

Este paquete proporciona:
- Gestión de datos de clientes con archivos de texto
- Implementación de tabla hash para búsquedas rápidas O(1)
- Manejo de errores y validación de datos
- Interfaz educativa con demostraciones interactivas

Módulos:
--------
- modelos: Clases de datos Cliente y Servicio
- cliente_manager: Gestor principal con tabla hash
- excepciones: Excepciones personalizadas del sistema

Ejemplo de uso:
---------------
    from axanet.cliente_manager import ClienteManager
    from axanet.modelos import Cliente
    
    # Crear gestor de clientes
    manager = ClienteManager()
    
    # Crear nuevo cliente
    cliente = manager.crear_cliente(
        nombre="Ana García", 
        telefono="5512345678",
        email="ana.garcia@email.com",
        primer_servicio="Instalación de internet 100 Mbps"
    )
    
    # Buscar cliente (demostración O(1))
    encontrado = manager.obtener_cliente("Ana García")
"""

__version__ = "1.0.0-academica"
__author__ = "Proyecto Académico Axanet"
__email__ = "estudiante@universidad.edu"

# Exportar clases principales para importación fácil
from .modelos import Cliente, Servicio
from .cliente_manager import ClienteManager
from .excepciones import (
    ClienteError, 
    ClienteNoEncontradoError, 
    ClienteExisteError,
    ErrorValidacion,
    ErrorArchivo
)

__all__ = [
    "Cliente",
    "Servicio", 
    "ClienteManager",
    "ClienteError",
    "ClienteNoEncontradoError",
    "ClienteExisteError",
    "ErrorValidacion",
    "ErrorArchivo"
]