"""
Gestor de Clientes para el Sistema Axanet
========================================

Este módulo contiene la lógica principal para manejar los clientes del sistema.
Utiliza una tabla hash (diccionario de Python) para lograr búsquedas rápidas O(1).

Funcionalidades principales:
- Crear nuevos clientes con validación
- Buscar clientes por nombre (O(1) con tabla hash)
- Listar todos los clientes
- Agregar servicios a clientes existentes
- Eliminar clientes del sistema
- Gestión de archivos de texto para persistencia

La clase ClienteManager es el corazón del sistema y demuestra:
- Uso de tablas hash para búsquedas eficientes
- Gestión de archivos para persistencia
- Validación de datos
- Manejo de errores
"""

import os
from pathlib import Path
from typing import Dict, List, Union

from .modelos import Cliente, Servicio
from .excepciones import (
    ClienteError,
    ClienteNoEncontradoError,
    ClienteExisteError, 
    ErrorValidacion,
    ErrorArchivo
)


class ClienteManager:
    """
    Gestor principal de clientes que utiliza una tabla hash para almacenamiento en memoria.
    
    Esta clase demuestra conceptos importantes:
    - Tabla Hash: Diccionario para búsquedas O(1)
    - Persistencia: Archivos de texto para guardar datos
    - Caché: Datos en memoria para acceso rápido
    - Validación: Verificación de datos antes de guardar
    
    Atributos:
        _cache_clientes: Diccionario (tabla hash) que mapea nombre_normalizado → Cliente
        directorio_datos: Carpeta donde se guardan los archivos de clientes
    """
    
    def __init__(self, directorio_datos: str = "axanet_clients_data"):
        """
        Inicializa el gestor de clientes.
        
        Args:
            directorio_datos: Nombre de la carpeta donde se guardan los archivos
        """
        # TABLA HASH PRINCIPAL - Esta es la estructura de datos clave
        # Mapea nombre_normalizado (string) → objeto Cliente
        # Permite búsquedas O(1) en lugar de O(n)
        self._cache_clientes: Dict[str, Cliente] = {}
        
        # Configurar directorio de datos
        self.directorio_datos = Path(directorio_datos)
        
        # Crear el directorio si no existe
        self._crear_directorio_datos()
        
        print(f"📁 Directorio de datos: {self.directorio_datos}")
        print(f"🔧 Tabla hash inicializada (vacía)")
    
    def _crear_directorio_datos(self):
        """
        Crea el directorio para los archivos de clientes si no existe.
        """
        try:
            self.directorio_datos.mkdir(exist_ok=True)
        except Exception as e:
            raise ErrorArchivo(
                operacion="crear directorio",
                nombre_archivo=str(self.directorio_datos),
                motivo=str(e)
            )
    
    def _obtener_ruta_archivo(self, nombre_normalizado: str) -> Path:
        """
        Genera la ruta completa del archivo para un cliente.
        
        Args:
            nombre_normalizado: Nombre del cliente normalizado
            
        Returns:
            Ruta completa del archivo del cliente
        """
        nombre_archivo = f"{nombre_normalizado}.txt"
        return self.directorio_datos / nombre_archivo
    
    def _cargar_cliente_desde_archivo(self, nombre_normalizado: str) -> Cliente:
        """
        Carga un cliente desde su archivo en disco.
        
        Args:
            nombre_normalizado: Nombre normalizado del cliente
            
        Returns:
            Objeto Cliente cargado desde el archivo
            
        Raises:
            ClienteNoEncontradoError: Si el archivo no existe
            ErrorArchivo: Si hay problemas al leer el archivo
        """
        ruta_archivo = self._obtener_ruta_archivo(nombre_normalizado)
        
        # Verificar que el archivo existe
        if not ruta_archivo.exists():
            # Intentar encontrar por nombre original sin normalizar
            nombre_original = nombre_normalizado.replace('_', ' ').title()
            raise ClienteNoEncontradoError(nombre_original)
        
        try:
            # Leer el contenido del archivo
            contenido = ruta_archivo.read_text(encoding='utf-8')
            
            # Crear cliente desde el contenido
            cliente = Cliente.desde_archivo(contenido)
            
            return cliente
            
        except Exception as e:
            raise ErrorArchivo(
                operacion="leer",
                nombre_archivo=str(ruta_archivo),
                motivo=str(e)
            )
    
    def _guardar_cliente_en_archivo(self, cliente: Cliente):
        """
        Guarda un cliente en su archivo correspondiente.
        
        Args:
            cliente: Objeto Cliente a guardar
            
        Raises:
            ErrorArchivo: Si hay problemas al escribir el archivo
        """
        ruta_archivo = self._obtener_ruta_archivo(cliente.nombre_normalizado)
        
        try:
            # Convertir cliente a formato de archivo
            contenido = cliente.a_formato_archivo()
            
            # Escribir archivo
            ruta_archivo.write_text(contenido, encoding='utf-8')
            
        except Exception as e:
            raise ErrorArchivo(
                operacion="escribir",
                nombre_archivo=str(ruta_archivo),
                motivo=str(e)
            )
    
    def _eliminar_archivo_cliente(self, nombre_normalizado: str):
        """
        Elimina el archivo de un cliente del disco.
        
        Args:
            nombre_normalizado: Nombre normalizado del cliente
            
        Raises:
            ErrorArchivo: Si hay problemas al eliminar el archivo
        """
        ruta_archivo = self._obtener_ruta_archivo(nombre_normalizado)
        
        try:
            if ruta_archivo.exists():
                ruta_archivo.unlink()
            
        except Exception as e:
            raise ErrorArchivo(
                operacion="eliminar",
                nombre_archivo=str(ruta_archivo),
                motivo=str(e)
            )
    
    def _cargar_todos_clientes_a_cache(self):
        """
        Carga todos los archivos de clientes en la tabla hash.
        
        Esta función es importante para el rendimiento:
        - Lee todos los archivos .txt del directorio
        - Los carga en la tabla hash para acceso O(1)
        - Solo carga clientes que no estén ya en caché
        """
        if not self.directorio_datos.exists():
            return
        
        # Buscar todos los archivos .txt en el directorio
        archivos_clientes = list(self.directorio_datos.glob("*.txt"))
        
        for archivo in archivos_clientes:
            # Obtener nombre normalizado del archivo
            nombre_normalizado = archivo.stem
            
            # Solo cargar si no está ya en caché
            if nombre_normalizado not in self._cache_clientes:
                try:
                    cliente = self._cargar_cliente_desde_archivo(nombre_normalizado)
                    self._cache_clientes[nombre_normalizado] = cliente
                except Exception as e:
                    # Si hay un archivo corrupto, simplemente lo omitimos
                    print(f"⚠️  Advertencia: No se pudo cargar {archivo}: {e}")
    
    def crear_cliente(self, nombre: str, telefono: str, email: str, primer_servicio: str) -> Cliente:
        """
        Crea un nuevo cliente en el sistema.
        
        Esta función demuestra:
        - Validación de datos de entrada
        - Verificación de duplicados usando tabla hash
        - Creación y guardado de archivos
        - Actualización de la tabla hash
        
        Args:
            nombre: Nombre completo del cliente
            telefono: Número de teléfono
            email: Dirección de correo electrónico
            primer_servicio: Descripción del primer servicio
            
        Returns:
            Cliente creado y guardado
            
        Raises:
            ClienteExisteError: Si ya existe un cliente con ese nombre
            ErrorValidacion: Si los datos no son válidos
        """
        # Crear el objeto cliente (esto valida los datos automáticamente)
        cliente = Cliente(nombre=nombre, telefono=telefono, email=email)
        
        # Verificar si ya existe un cliente con este nombre
        # Esto es una búsqueda O(1) en la tabla hash
        if cliente.nombre_normalizado in self._cache_clientes:
            raise ClienteExisteError(cliente.nombre)
        
        # Verificar si existe archivo en disco (por si no está en caché)
        ruta_archivo = self._obtener_ruta_archivo(cliente.nombre_normalizado)
        if ruta_archivo.exists():
            raise ClienteExisteError(cliente.nombre)
        
        # Generar ID único del cliente
        cliente.id_cliente = cliente.generar_id_cliente()
        
        # Agregar el primer servicio
        cliente.agregar_servicio(primer_servicio)
        
        # Guardar en archivo
        self._guardar_cliente_en_archivo(cliente)
        
        # Agregar a la tabla hash (caché en memoria)
        self._cache_clientes[cliente.nombre_normalizado] = cliente
        
        print(f"✅ Cliente guardado en tabla hash: clave='{cliente.nombre_normalizado}'")
        
        return cliente
    
    def obtener_cliente(self, nombre: str) -> Cliente:
        """
        Busca un cliente por su nombre utilizando la tabla hash.
        
        Esta es la función que demuestra el poder de las tablas hash:
        - Búsqueda O(1) en lugar de O(n)
        - Independiente del número de clientes en el sistema
        
        Args:
            nombre: Nombre del cliente a buscar
            
        Returns:
            Objeto Cliente encontrado
            
        Raises:
            ClienteNoEncontradoError: Si el cliente no existe
        """
        # Normalizar el nombre para usarlo como clave en la tabla hash
        cliente_temp = Cliente(nombre=nombre, telefono="0000000000", email="temp@temp.com")
        nombre_normalizado = cliente_temp.nombre_normalizado
        
        # BÚSQUEDA O(1) EN LA TABLA HASH
        if nombre_normalizado in self._cache_clientes:
            print(f"🎯 Cliente encontrado en tabla hash (O(1)): '{nombre_normalizado}'")
            return self._cache_clientes[nombre_normalizado]
        
        # Si no está en caché, intentar cargar desde archivo
        try:
            cliente = self._cargar_cliente_desde_archivo(nombre_normalizado)
            
            # Agregar al caché para futuras búsquedas O(1)
            self._cache_clientes[nombre_normalizado] = cliente
            
            print(f"📂 Cliente cargado desde archivo y agregado a tabla hash")
            return cliente
            
        except ClienteNoEncontradoError:
            # Re-lanzar la excepción con el nombre original
            raise ClienteNoEncontradoError(nombre)
    
    def listar_todos_clientes(self) -> List[Cliente]:
        """
        Lista todos los clientes del sistema.
        
        Esta función:
        - Carga todos los archivos en la tabla hash si no están ya
        - Retorna una lista de todos los clientes
        - Demuestra iteración sobre diccionarios
        
        Returns:
            Lista de todos los clientes registrados
        """
        # Cargar todos los clientes en la tabla hash
        self._cargar_todos_clientes_a_cache()
        
        # Retornar lista de valores del diccionario
        clientes = list(self._cache_clientes.values())
        
        # Ordenar por nombre para presentación consistente
        clientes.sort(key=lambda c: c.nombre)
        
        print(f"📊 Clientes en tabla hash: {len(self._cache_clientes)}")
        
        return clientes
    
    def agregar_servicio_cliente(self, nombre: str, descripcion_servicio: str) -> Cliente:
        """
        Agrega un servicio a un cliente existente.
        
        Args:
            nombre: Nombre del cliente
            descripcion_servicio: Descripción del nuevo servicio
            
        Returns:
            Cliente actualizado con el nuevo servicio
            
        Raises:
            ClienteNoEncontradoError: Si el cliente no existe
        """
        # Buscar el cliente (búsqueda O(1))
        cliente = self.obtener_cliente(nombre)
        
        # Agregar el nuevo servicio
        cliente.agregar_servicio(descripcion_servicio)
        
        # Guardar cambios en archivo
        self._guardar_cliente_en_archivo(cliente)
        
        # Actualizar en tabla hash (aunque ya debería estar actualizado por referencia)
        self._cache_clientes[cliente.nombre_normalizado] = cliente
        
        return cliente
    
    def eliminar_cliente(self, nombre: str) -> bool:
        """
        Elimina un cliente del sistema.
        
        Esta función:
        - Busca el cliente en la tabla hash
        - Elimina el archivo del disco
        - Remueve la entrada de la tabla hash
        
        Args:
            nombre: Nombre del cliente a eliminar
            
        Returns:
            True si se eliminó correctamente
            
        Raises:
            ClienteNoEncontradoError: Si el cliente no existe
        """
        # Verificar que el cliente existe (búsqueda O(1))
        cliente = self.obtener_cliente(nombre)
        
        # Eliminar archivo del disco
        self._eliminar_archivo_cliente(cliente.nombre_normalizado)
        
        # Eliminar de la tabla hash
        if cliente.nombre_normalizado in self._cache_clientes:
            del self._cache_clientes[cliente.nombre_normalizado]
        
        print(f"🗑️  Cliente eliminado de tabla hash: '{cliente.nombre_normalizado}'")
        
        return True
    
    def obtener_estadisticas(self) -> Dict[str, Union[int, float]]:
        """
        Calcula y retorna estadísticas del sistema.
        
        Returns:
            Diccionario con estadísticas del sistema
        """
        # Cargar todos los clientes para tener datos completos
        self._cargar_todos_clientes_a_cache()
        
        total_clientes = len(self._cache_clientes)
        
        if total_clientes == 0:
            return {
                "total_clientes": 0,
                "total_servicios": 0,
                "promedio_servicios": 0.0
            }
        
        # Contar servicios totales
        total_servicios = sum(len(cliente.servicios) for cliente in self._cache_clientes.values())
        
        # Calcular promedio
        promedio_servicios = total_servicios / total_clientes if total_clientes > 0 else 0
        
        return {
            "total_clientes": total_clientes,
            "total_servicios": total_servicios,
            "promedio_servicios": promedio_servicios
        }
    
    def __str__(self):
        """Representación en texto del gestor."""
        return f"ClienteManager(clientes_en_cache={len(self._cache_clientes)})"
    
    def __repr__(self):
        """Representación técnica del gestor."""
        return f"ClienteManager(cache_size={len(self._cache_clientes)}, directorio='{self.directorio_datos}')"


# Función utilitaria para normalizar nombres (usada por otras partes del sistema)
def normalizar_nombre(nombre: str) -> str:
    """
    Normaliza un nombre para usar como clave en la tabla hash.
    
    Esta es la misma lógica que usa Cliente.nombre_normalizado
    pero disponible como función independiente.
    
    Args:
        nombre: Nombre a normalizar
        
    Returns:
        Nombre normalizado
    """
    import re
    
    # Crear un cliente temporal solo para usar su método de normalización
    try:
        cliente_temp = Cliente(nombre=nombre, telefono="0000000000", email="temp@temp.com")
        return cliente_temp.nombre_normalizado
    except ErrorValidacion:
        # Si el nombre no es válido para un cliente, hacer normalización básica
        normalizado = nombre.lower().strip()
        normalizado = normalizado.replace(' ', '_')
        normalizado = re.sub(r'[^a-z0-9_]', '', normalizado)
        return normalizado