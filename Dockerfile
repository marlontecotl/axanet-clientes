# Dockerfile Simplificado - Sistema de Gestión de Clientes Axanet
# ==============================================================
# 
# Este Dockerfile demuestra cómo containerizar nuestra aplicación
# de manera sencilla para ejecutarla en cualquier entorno.
#
# ¿Qué hace Docker?
# - Empaqueta la aplicación con todas sus dependencias
# - Garantiza que funcione igual en cualquier computadora
# - Aísla la aplicación del sistema operativo host

# ================================
# COMANDO FROM - Imagen Base
# ================================
# FROM especifica qué imagen base usar como punto de partida
# python:3.9-slim = Imagen oficial de Python 3.9 en versión "slim" (liviana)
# "slim" significa que tiene menos paquetes instalados, haciendo la imagen más pequeña
FROM python:3.9-slim

# ================================
# COMANDOS LABEL - Metadatos
# ================================
# LABEL agrega metadatos al contenedor (como etiquetas informativas)
# Estos no afectan la funcionalidad, solo proporcionan información

# Quién mantiene esta imagen Docker
LABEL maintainer="Proyecto Académico Axanet"

# Descripción del proyecto containerizado  
LABEL description="Sistema de Gestión de Clientes - Actividad II"

# Versión de la aplicación académica
LABEL version="1.0-academica"

# ================================
# COMANDO WORKDIR - Directorio de Trabajo
# ================================
# WORKDIR establece el directorio de trabajo dentro del contenedor
# Es como hacer "cd /app" - todos los comandos siguientes se ejecutarán desde aquí
# Si el directorio no existe, Docker lo crea automáticamente
WORKDIR /app

# ================================
# COMANDO COPY - Copiar Archivos
# ================================
# COPY copia archivos desde tu computadora (host) hacia el contenedor
# Sintaxis: COPY <origen_en_host> <destino_en_contenedor>
# El punto (.) significa "todo el directorio actual"
# Esto copia: main.py, src/, README.md, .gitignore, etc.
COPY . /app/

# ================================
# COMANDO RUN - Ejecutar Comandos
# ================================
# RUN ejecuta comandos durante la construcción de la imagen
# mkdir -p = crear directorio y directorios padre si no existen
# Este comando crea la carpeta donde se guardarán los archivos de clientes
RUN mkdir -p /app/axanet_clients_data

# ================================
# COMANDOS ENV - Variables de Entorno
# ================================
# ENV establece variables de entorno dentro del contenedor
# Estas variables estarán disponibles cuando se ejecute la aplicación

# PYTHONPATH=/app - Le dice a Python dónde buscar módulos
# Esto permite que "from src.axanet import ..." funcione correctamente
ENV PYTHONPATH=/app

# PYTHONUNBUFFERED=1 - Hace que Python muestre output inmediatamente
# Sin esto, los print() podrían no mostrarse hasta que termine el programa
ENV PYTHONUNBUFFERED=1

# ================================
# COMANDO CMD - Comando por Defecto
# ================================
# CMD especifica qué comando ejecutar cuando se inicie el contenedor
# Sintaxis de array: ["programa", "argumento1", "argumento2"]
# Esto es equivalente a ejecutar "python main.py" en la terminal
# Nota: Solo puede haber un CMD por Dockerfile (el último prevalece)
CMD ["python", "main.py"]

# ================================
# RESUMEN DE COMANDOS USADOS:
# ================================
# FROM    - Define imagen base (Python 3.11)
# LABEL   - Agrega metadatos informativos  
# WORKDIR - Establece directorio de trabajo (/app)
# COPY    - Copia archivos del host al contenedor
# RUN     - Ejecuta comandos durante la construcción
# ENV     - Define variables de entorno
# CMD     - Especifica comando por defecto a ejecutar
# ================================