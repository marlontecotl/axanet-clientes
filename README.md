# Sistema de Gestión de Clientes Axanet

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-enabled-green.svg)](https://github.com/features/actions)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Academic](https://img.shields.io/badge/Project-Academic-orange.svg)](https://github.com/features/actions)

**Sistema Académico de Gestión de Clientes - Versión Simplificada**

Sistema de gestión de clientes desarrollado en Python para demostrar conceptos fundamentales de estructuras de datos y programación orientada a objetos. Implementa tablas hash para búsquedas eficientes O(1) y persistencia de datos mediante archivos de texto.

## Objetivos Educativos

Este proyecto está diseñado para estudiantes universitarios que desean aprender:

### Conceptos Fundamentales de Ciencias de la Computación
- **Tablas Hash**: Rendimiento de búsqueda O(1) usando diccionarios de Python
- **Operaciones de Archivos**: Gestión de archivos de texto y persistencia de datos
- **Estructuras de Datos**: Modelos de Cliente y Servicio con relaciones
- **Diseño de Algoritmos**: Operaciones CRUD con validación y manejo de errores

### Prácticas de Ingeniería de Software
- **Arquitectura Modular**: Separación de responsabilidades entre clases
- **Manejo de Errores**: Excepciones personalizadas con mensajes claros
- **Validación de Datos**: Integridad de datos y buenas prácticas
- **Programación Orientada a Objetos**: Encapsulación, herencia y polimorfismo

### Características Académicas
- **Código Comentado en Español**: Explicaciones detalladas para aprendizaje
- **Complejidad de Nivel Junior**: Código fácil de entender y modificar
- **Demostraciones Interactivas**: Ejemplos prácticos de conceptos teóricos
- **Documentación Educativa**: Guías paso a paso y ejemplos de uso

## Funcionalidades del Sistema

### Operaciones Básicas
- **Crear nuevos clientes** con información de contacto completa y servicio inicial
- **Buscar clientes** por nombre con demostración de búsqueda O(1)  
- **Listar todos los clientes** registrados en el sistema
- **Agregar servicios** a clientes existentes con timestamps automáticos
- **Eliminar clientes** del sistema con confirmación
- **Ver estadísticas** del sistema (totales, promedios)

### Características Técnicas
- **Implementación de tabla hash** usando diccionarios Python para búsqueda O(1)
- **Almacenamiento en archivos** con archivos de texto individuales por cliente
- **Validación de datos** automática con excepciones personalizadas
- **Interfaz de menú** intuitiva con opciones numeradas
- **Demostraciones educativas** de conceptos de estructuras de datos

## Estructura del Proyecto Simplificado

```
axanet-client-manager/
├── main.py                    # Aplicación principal con interfaz de menú
├── src/axanet/               # Paquete principal del sistema
│   ├── __init__.py           # Inicialización del paquete
│   ├── cliente_manager.py    # Gestor de clientes con tabla hash
│   ├── modelos.py           # Clases Cliente y Servicio
│   └── excepciones.py       # Excepciones personalizadas
├── axanet_clients_data/     # Directorio de datos (se crea automáticamente)
├── requirements.txt         # Dependencias (solo Python estándar)
├── EJECUCION_SIMPLE.md     # Guía de ejecución paso a paso
└── README.md               # Documentación principal
```
- **Comprehensive logging** with configurable levels and rotation
- **Input validation** with custom exception hierarchy
- **Configuration management** with environment variable support
- **Professional CLI** with subcommands and help documentation
- **Modo interactivo** con interfaz de menú fácil de usar
- **Compatibilidad multiplataforma** (Windows, macOS, Linux)

## Inicio Rápido

### Requisitos Previos
- Python 3.8 o superior
- Terminal o línea de comandos

### Instalación y Ejecución

1. **Descargar o clonar el repositorio**
   ```bash
   git clone https://github.com/tu-usuario/axanet-client-manager.git
   cd axanet-client-manager
   ```

2. **Ejecutar la aplicación** (no requiere instalación de dependencias)
   ```bash
   python main.py
   ```
   
   O en sistemas con Python 3:
   ```bash
   python3 main.py
   ```

### ¡Es así de simple! El sistema usa solo librerías estándar de Python.

## Uso del Sistema

Al ejecutar la aplicación verás un menú como este:

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                    🏢 SISTEMA AXANET - GESTIÓN DE CLIENTES 🏢              ║
║                          Versión Académica 1.0                           ║
╠═══════════════════════════════════════════════════════════════════════════╣
║  Este sistema demuestra el uso de TABLAS HASH para gestión eficiente     ║
║  de clientes. Todas las búsquedas son O(1) - tiempo constante.          ║
╚═══════════════════════════════════════════════════════════════════════════╝

📋 MENÚ PRINCIPAL:

1️⃣  Crear nuevo cliente
2️⃣  Buscar cliente (Demostración de Tabla Hash)  
3. Update existing client
4. Delete client
5. Exit
```

### Creating a New Client
- Enter client name, phone, email, and first service description
- The system automatically generates a unique client ID
- Client data is stored in `axanet_clients_data/` directory

### Viewing Clients
- Search by specific client name
- List all registered clients

### Updating Clients
- Add new services to existing client records
- Services are appended with current timestamp

### Deleting Clients
- Remove client files with confirmation prompt
- Includes safety checks to prevent accidental deletion

## Project Structure

```
axanet-client-manager/
├── axanet_client_manager.py    # Main application
├── axanet_clients_data/        # Client data files
├── requirements.txt            # Python dependencies
├── .github/workflows/          # GitHub Actions workflows
│   ├── new-client-notification.yml
│   ├── client-update-notification.yml
│   └── client-query-notification.yml
├── README.md                   # This file
└── LICENSE                     # Project license
```

3️⃣  Listar todos los clientes  
4️⃣  Agregar servicio a cliente existente
5️⃣  Eliminar cliente del sistema
6️⃣  Ver estadísticas del sistema
7️⃣  Demostración educativa de conceptos
8️⃣  Salir del sistema
```

### Ejemplos de Uso

**Crear un nuevo cliente:**
1. Selecciona la opción 1
2. Ingresa el nombre completo
3. Proporciona un teléfono de 10 dígitos
4. Ingresa un email válido
5. Describe el primer servicio

**Buscar un cliente (Demostración O(1)):**
1. Selecciona la opción 2
2. Ingresa el nombre del cliente
3. El sistema te mostrará cómo funciona la búsqueda en tabla hash

## Características Educativas Destacadas

### 🔍 Demostración de Tablas Hash
- **Búsqueda O(1)**: Explicación visual de por qué es más rápido que búsqueda lineal
- **Normalización de claves**: Cómo convertir nombres en claves de hash consistentes
- **Comparación práctica**: Ejemplos con 1, 100, y 1000 clientes

### 📚 Conceptos de Programación
- **Orientación a Objetos**: Clases bien diseñadas con responsabilidades claras
- **Manejo de Excepciones**: Sistema robusto de errores personalizados
- **Persistencia de Datos**: Archivos de texto legibles y bien estructurados
- **Validación**: Verificación automática de datos de entrada

### 📁 Gestión de Archivos
- **Un archivo por cliente**: Fácil de entender y gestionar
- **Formato legible**: Los archivos se pueden abrir con cualquier editor de texto
- **Recuperación automática**: Los datos se cargan automáticamente al iniciar

## GitHub Actions (Workflows Académicos)

El proyecto incluye 3 workflows básicos para notificaciones:

1. **Nuevo Cliente** - Se activa al crear clientes
2. **Actualización de Cliente** - Se activa al modificar datos
3. **Consulta de Cliente** - Se activa al buscar información

Para ejecutar workflows:
1. Ve a la pestaña **Actions** en GitHub
2. Selecciona el workflow deseado
3. Haz clic en **Run workflow**

## Estructura de Datos Generados

Cada cliente se guarda en un archivo individual con este formato:

```
Cliente: Ana García
Teléfono: 5551234567
Email: ana.garcia@email.com
ID: AG_202410_001
Fecha Registro: 2024-10-22 10:30:15

Servicios:
1. Internet residencial 50 Mbps (2024-10-22)
2. Instalación de router Wi-Fi (2024-10-22)
```

## Para Estudiantes

### ¿Qué aprenderás?
- **Estructuras de Datos**: Diferencia entre listas y tablas hash
- **Complejidad Algorítmica**: O(1) vs O(n) con ejemplos prácticos
- **Programación Orientada a Objetos**: Clases, métodos, encapsulación
- **Manejo de Archivos**: Persistencia de datos sin bases de datos
- **Manejo de Errores**: Excepciones personalizadas y validación

### Conceptos Demostrados
- ✅ Tablas hash y búsquedas eficientes
- ✅ Persistencia de datos en archivos
- ✅ Validación y manejo de errores
- ✅ Interfaz de usuario por consola
- ✅ Organización modular de código

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## Autor

Proyecto académico desarrollado para demostrar conceptos de estructuras de datos y programación orientada a objetos en Python.

¡Perfecto para estudiantes que quieren entender cómo funcionan las tablas hash en aplicaciones reales!
