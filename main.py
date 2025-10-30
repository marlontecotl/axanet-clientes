#!/usr/bin/env python3
"""
Sistema de Gestión de Clientes Axanet
====================================

Programa principal que permite gestionar los clientes de la empresa Axanet.
Utiliza tablas hash (diccionarios de Python) para búsquedas eficientes.

Funcionalidades:
- Crear nuevos clientes con su primer servicio
- Buscar clientes por nombre (búsqueda O(1) con tabla hash)
- Listar todos los clientes registrados  
- Agregar nuevos servicios a clientes existentes
- Eliminar clientes del sistema

Estructura de archivos:
- Cada cliente se guarda en un archivo .txt individual
- Los archivos se almacenan en la carpeta 'axanet_clients_data/'
- Los nombres se normalizan para evitar problemas (ej: ana_garcia.txt)

Autor: Estudiante
Actividad: Práctica II - Sistemas de Información
"""

import sys
import os
from pathlib import Path

# Agregar la carpeta src al path de Python para importar nuestros módulos
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Importar nuestros módulos personalizados
from axanet.cliente_manager import ClienteManager
from axanet.excepciones import (
    ClienteError,
    ClienteNoEncontradoError, 
    ClienteExisteError,
    ErrorValidacion
)


class AplicacionAxanet:
    """
    Clase principal de la aplicación Axanet.
    
    Esta clase maneja toda la interfaz de usuario y coordina las operaciones
    con el gestor de clientes. Utiliza el patrón de menú interactivo para
    que sea fácil de usar.
    """
    
    def __init__(self):
        """
        Inicializa la aplicación creando el gestor de clientes.
        El gestor contiene la tabla hash (diccionario) principal.
        """
        print("🔄 Inicializando sistema Axanet...")
        self.gestor_clientes = ClienteManager()
        print("✅ Sistema listo para usar")
        
    def mostrar_bienvenida(self):
        """Muestra el mensaje de bienvenida y información del sistema."""
        print("\n" + "="*55)
        print("🏢 SISTEMA DE GESTIÓN DE CLIENTES AXANET")
        print("   Utilizando Tablas Hash para Búsquedas Rápidas")
        print("="*55)
        print("📚 CONCEPTOS DEMOSTRADOS:")
        print("   • Tablas Hash (Diccionarios) - Búsqueda O(1)")
        print("   • Gestión de Archivos de Texto")
        print("   • Validación de Datos")
        print("   • Manejo de Errores")
        print("   • Programación Modular")
        
        # Mostrar estadísticas actuales si hay clientes
        try:
            estadisticas = self.gestor_clientes.obtener_estadisticas()
            if estadisticas["total_clientes"] > 0:
                print(f"\n📊 ESTADO ACTUAL:")
                print(f"   • Clientes registrados: {estadisticas['total_clientes']}")
                print(f"   • Servicios en total: {estadisticas['total_servicios']}")
                print(f"   • Promedio servicios por cliente: {estadisticas['promedio_servicios']:.1f}")
        except Exception:
            print("\n📊 ESTADO: Sistema vacío - ¡Crea tu primer cliente!")
            
        print("="*55)

    def mostrar_menu(self):
        """Muestra las opciones disponibles en el menú principal."""
        print("\n📋 MENÚ PRINCIPAL")
        print("─" * 35)
        print("1. 📝 Crear nuevo cliente")
        print("2. 🔍 Buscar cliente por nombre") 
        print("3. 📊 Ver todos los clientes")
        print("4. ➕ Agregar servicio a cliente")
        print("5. 🗑️  Eliminar cliente")
        print("6. 📈 Ver estadísticas del sistema")
        print("7. 🎓 Demostrar tabla hash")
        print("0. 🚪 Salir del programa")
        print("─" * 35)

    def crear_cliente(self):
        """
        Crea un nuevo cliente solicitando los datos al usuario.
        
        Esta función demuestra:
        - Validación de entrada de datos
        - Manejo de excepciones
        - Uso de la tabla hash para verificar existencia
        """
        print("\n📝 CREAR NUEVO CLIENTE")
        print("─" * 25)
        
        try:
            # Solicitar datos del cliente
            nombre = input("👤 Nombre completo del cliente: ").strip()
            if not nombre:
                print("❌ El nombre no puede estar vacío")
                return
                
            telefono = input("📞 Teléfono (10 dígitos): ").strip()
            if not telefono:
                print("❌ El teléfono no puede estar vacío")
                return
                
            email = input("📧 Correo electrónico: ").strip()
            if not email:
                print("❌ El correo no puede estar vacío")
                return
                
            primer_servicio = input("🔧 Descripción del primer servicio: ").strip()
            if not primer_servicio:
                print("❌ Debe proporcionar una descripción del servicio")
                return
            
            # Intentar crear el cliente usando el gestor
            print("\n⏳ Creando cliente...")
            cliente = self.gestor_clientes.crear_cliente(
                nombre=nombre,
                telefono=telefono, 
                email=email,
                primer_servicio=primer_servicio
            )
            
            print(f"✅ Cliente creado exitosamente!")
            print(f"📄 Archivo: axanet_clients_data/{cliente.nombre_normalizado}.txt")
            print(f"🆔 ID generado: {cliente.id_cliente}")
            
        except ClienteExisteError as e:
            print(f"❌ Error: {e}")
        except ErrorValidacion as e:
            print(f"❌ Error de validación: {e}")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")

    def buscar_cliente(self):
        """
        Busca un cliente por nombre utilizando la tabla hash.
        
        Esta función demuestra:
        - Búsqueda O(1) en tabla hash
        - Manejo de casos cuando no se encuentra el elemento
        - Presentación de información de manera clara
        """
        print("\n🔍 BUSCAR CLIENTE")
        print("─" * 17)
        
        nombre = input("👤 Ingrese el nombre del cliente: ").strip()
        if not nombre:
            print("❌ Debe ingresar un nombre")
            return
            
        try:
            print("⏳ Buscando en tabla hash...")
            
            # Esta búsqueda es O(1) gracias a la tabla hash
            cliente = self.gestor_clientes.obtener_cliente(nombre)
            
            print("✅ Cliente encontrado:")
            print("─" * 25)
            print(f"👤 Nombre: {cliente.nombre}")
            print(f"🆔 ID: {cliente.id_cliente}")
            print(f"📞 Teléfono: {cliente.telefono}")
            print(f"📧 Email: {cliente.email}")
            print(f"📅 Registrado: {cliente.fecha_registro}")
            print(f"\n🔧 SERVICIOS ({len(cliente.servicios)}):")
            
            for i, servicio in enumerate(cliente.servicios, 1):
                print(f"   {i}. {servicio.descripcion}")
                print(f"      📅 Fecha: {servicio.fecha_solicitud}")
                
        except ClienteNoEncontradoError:
            print(f"❌ No se encontró un cliente con el nombre '{nombre}'")
            print("💡 Verifique la ortografía o use la opción 3 para ver todos los clientes")
        except Exception as e:
            print(f"❌ Error al buscar: {e}")

    def listar_todos_clientes(self):
        """
        Lista todos los clientes cargando los archivos a la tabla hash.
        
        Esta función demuestra:
        - Carga de todos los elementos en la tabla hash
        - Iteración sobre diccionarios
        - Presentación tabular de información
        """
        print("\n📊 TODOS LOS CLIENTES")
        print("─" * 21)
        
        try:
            print("⏳ Cargando todos los clientes en tabla hash...")
            clientes = self.gestor_clientes.listar_todos_clientes()
            
            if not clientes:
                print("📭 No hay clientes registrados en el sistema")
                print("💡 Use la opción 1 para crear el primer cliente")
                return
            
            print(f"✅ Se encontraron {len(clientes)} cliente(s):\n")
            
            # Mostrar tabla de clientes
            print(f"{'#':<3} {'NOMBRE':<25} {'TELÉFONO':<12} {'SERVICIOS':<10}")
            print("─" * 55)
            
            for i, cliente in enumerate(clientes, 1):
                nombre_corto = cliente.nombre[:22] + "..." if len(cliente.nombre) > 25 else cliente.nombre
                print(f"{i:<3} {nombre_corto:<25} {cliente.telefono:<12} {len(cliente.servicios):<10}")
                
            print("─" * 55)
            print(f"Total: {len(clientes)} cliente(s) en la tabla hash")
            
        except Exception as e:
            print(f"❌ Error al listar clientes: {e}")

    def agregar_servicio(self):
        """
        Agrega un servicio a un cliente existente.
        
        Esta función demuestra:
        - Búsqueda en tabla hash para encontrar cliente
        - Modificación de datos existentes
        - Actualización de archivos
        """
        print("\n➕ AGREGAR SERVICIO A CLIENTE")
        print("─" * 29)
        
        nombre = input("👤 Nombre del cliente: ").strip()
        if not nombre:
            print("❌ Debe ingresar un nombre")
            return
            
        try:
            # Primero verificar que el cliente existe (búsqueda O(1))
            cliente = self.gestor_clientes.obtener_cliente(nombre)
            print(f"✅ Cliente encontrado: {cliente.nombre}")
            print(f"📋 Servicios actuales: {len(cliente.servicios)}")
            
            # Solicitar descripción del nuevo servicio
            nuevo_servicio = input("🔧 Descripción del nuevo servicio: ").strip()
            if not nuevo_servicio:
                print("❌ La descripción del servicio no puede estar vacía")
                return
                
            # Agregar el servicio
            print("⏳ Agregando servicio...")
            cliente_actualizado = self.gestor_clientes.agregar_servicio_cliente(
                nombre, nuevo_servicio
            )
            
            print("✅ Servicio agregado exitosamente!")
            print(f"📋 Total de servicios: {len(cliente_actualizado.servicios)}")
            
        except ClienteNoEncontradoError:
            print(f"❌ No se encontró un cliente con el nombre '{nombre}'")
        except Exception as e:
            print(f"❌ Error al agregar servicio: {e}")

    def eliminar_cliente(self):
        """
        Elimina un cliente del sistema con confirmación.
        
        Esta función demuestra:
        - Búsqueda en tabla hash
        - Confirmación de usuario para operaciones destructivas
        - Eliminación de archivos y datos de memoria
        """
        print("\n🗑️  ELIMINAR CLIENTE")
        print("─" * 18)
        
        nombre = input("👤 Nombre del cliente a eliminar: ").strip()
        if not nombre:
            print("❌ Debe ingresar un nombre")
            return
            
        try:
            # Verificar que el cliente existe
            cliente = self.gestor_clientes.obtener_cliente(nombre)
            
            # Mostrar información del cliente antes de eliminar
            print(f"\n⚠️  ATENCIÓN: Se eliminará el siguiente cliente:")
            print(f"👤 Nombre: {cliente.nombre}")
            print(f"📞 Teléfono: {cliente.telefono}")
            print(f"🔧 Servicios: {len(cliente.servicios)}")
            
            # Pedir confirmación
            confirmacion = input("\n❓ ¿Está seguro? (escriba 'SI' para confirmar): ").strip().upper()
            
            if confirmacion == "SI":
                print("⏳ Eliminando cliente...")
                exito = self.gestor_clientes.eliminar_cliente(nombre)
                
                if exito:
                    print("✅ Cliente eliminado exitosamente")
                    print("🗑️  Archivo borrado del disco")
                    print("📝 Cliente removido de la tabla hash")
                else:
                    print("❌ No se pudo eliminar el cliente")
            else:
                print("⏸️  Operación cancelada")
                
        except ClienteNoEncontradoError:
            print(f"❌ No se encontró un cliente con el nombre '{nombre}'")
        except Exception as e:
            print(f"❌ Error al eliminar: {e}")

    def mostrar_estadisticas(self):
        """
        Muestra estadísticas del sistema y del rendimiento de la tabla hash.
        
        Esta función demuestra:
        - Análisis de datos almacenados
        - Cálculos estadísticos básicos
        - Información sobre el rendimiento de la tabla hash
        """
        print("\n📈 ESTADÍSTICAS DEL SISTEMA")
        print("─" * 27)
        
        try:
            estadisticas = self.gestor_clientes.obtener_estadisticas()
            
            print("📊 DATOS GENERALES:")
            print(f"   • Total de clientes: {estadisticas['total_clientes']}")
            print(f"   • Total de servicios: {estadisticas['total_servicios']}")
            print(f"   • Promedio servicios/cliente: {estadisticas['promedio_servicios']:.2f}")
            
            if estadisticas['total_clientes'] > 0:
                print("\n💾 INFORMACIÓN DE ALMACENAMIENTO:")
                print(f"   • Archivos en disco: {estadisticas['total_clientes']}")
                print(f"   • Clientes en tabla hash: {len(self.gestor_clientes._cache_clientes)}")
                print(f"   • Directorio: axanet_clients_data/")
                
                print("\n⚡ RENDIMIENTO DE TABLA HASH:")
                print(f"   • Tiempo de búsqueda: O(1) constante")
                print(f"   • Colisiones: 0 (nombres únicos)")
                print(f"   • Factor de carga: {len(self.gestor_clientes._cache_clientes)} elementos")
                
        except Exception as e:
            print(f"❌ Error al obtener estadísticas: {e}")

    def demostrar_tabla_hash(self):
        """
        Modo educativo que demuestra cómo funciona la tabla hash.
        
        Esta función es puramente educativa y muestra:
        - La estructura interna del diccionario
        - Cómo se normalizan las claves
        - El proceso de búsqueda O(1)
        """
        print("\n🎓 DEMOSTRACIÓN DE TABLA HASH")
        print("─" * 29)
        print("📚 Esta demostración muestra cómo funciona internamente")
        print("   la tabla hash (diccionario) que usamos para los clientes.")
        
        try:
            # Cargar todos los clientes si no están en caché
            self.gestor_clientes._cargar_todos_clientes_a_cache()
            cache = self.gestor_clientes._cache_clientes
            
            if not cache:
                print("\n📭 La tabla hash está vacía")
                print("💡 Cree algunos clientes primero para ver la demostración")
                return
            
            print(f"\n🔧 ESTRUCTURA INTERNA DE LA TABLA HASH:")
            print(f"   • Tipo: dict (diccionario de Python)")
            print(f"   • Elementos: {len(cache)}")
            print(f"   • Complejidad de búsqueda: O(1)")
            
            print(f"\n🗝️  CLAVES EN LA TABLA HASH:")
            for i, (clave, cliente) in enumerate(cache.items(), 1):
                print(f"   {i}. '{clave}' → {cliente.nombre}")
                
            # Demostración de búsqueda
            print(f"\n🔍 DEMOSTRACIÓN DE BÚSQUEDA O(1):")
            if cache:
                primera_clave = list(cache.keys())[0]
                print(f"   • Buscando clave: '{primera_clave}'")
                print(f"   • Resultado: cache['{primera_clave}'] = {cache[primera_clave].nombre}")
                print(f"   • Tiempo: O(1) - ¡Inmediato sin importar cuántos clientes hay!")
                
        except Exception as e:
            print(f"❌ Error en la demostración: {e}")

    def ejecutar(self):
        """
        Método principal que ejecuta el bucle de la aplicación.
        
        Este es el corazón de la aplicación que:
        - Muestra la bienvenida
        - Presenta el menú en bucle
        - Procesa las opciones del usuario
        - Maneja errores de entrada
        """
        self.mostrar_bienvenida()
        
        while True:
            try:
                self.mostrar_menu()
                opcion = input("\n🎯 Seleccione una opción (0-7): ").strip()
                
                if opcion == "0":
                    print("\n👋 ¡Gracias por usar el Sistema Axanet!")
                    print("🎓 Esperamos que haya aprendido sobre tablas hash")
                    break
                elif opcion == "1":
                    self.crear_cliente()
                elif opcion == "2":
                    self.buscar_cliente()
                elif opcion == "3":
                    self.listar_todos_clientes()
                elif opcion == "4":
                    self.agregar_servicio()
                elif opcion == "5":
                    self.eliminar_cliente()
                elif opcion == "6":
                    self.mostrar_estadisticas()
                elif opcion == "7":
                    self.demostrar_tabla_hash()
                else:
                    print("❌ Opción no válida. Por favor seleccione 0-7.")
                    
                # Pausa para que el usuario pueda leer el resultado
                if opcion != "0":
                    input("\n⏸️  Presione Enter para continuar...")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Programa interrumpido por el usuario")
                break
            except Exception as e:
                print(f"\n❌ Error inesperado: {e}")
                print("💡 Intente nuevamente o contacte al soporte técnico")


def main():
    """
    Función principal que inicia la aplicación.
    
    Esta función:
    - Crea la instancia de la aplicación
    - Maneja errores de inicialización
    - Proporciona un punto de entrada limpio
    """
    try:
        print("🚀 Iniciando Sistema de Gestión de Clientes Axanet...")
        aplicacion = AplicacionAxanet()
        aplicacion.ejecutar()
        
    except KeyboardInterrupt:
        print("\n\n👋 Programa interrumpido")
    except Exception as e:
        print(f"\n💥 Error crítico al iniciar la aplicación: {e}")
        print("🔧 Verifique que todos los archivos estén en su lugar")
        sys.exit(1)


# Punto de entrada del programa
if __name__ == "__main__":
    main()