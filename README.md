# Sistema-Gestion-Inventario-
Proyecto final integrador de Python avanzado y SQLite para Talento Tech 
🗃️ Sistema de Gestión de Inventario Local (CRUD)

Este proyecto final integrador fue desarrollado en el marco del programa **Talento Tech (Buenos Aires Aprende)** en el trayecto de Python Avanzado. Consiste en una aplicación de consola interactiva y portable diseñada para la administración autónoma de inventarios mediante persistencia de datos relacional y un robusto esquema de control de errores.

---

## 🚀 Requerimientos Técnicos Implementados

El software está completamente modularizado mediante funciones independientes para garantizar la legibilidad y escalabilidad del código:

*   **Persistencia en Base de Datos (SQLite3):** Conexión directa y local a un motor embebido que genera el archivo `inventario.db`. Se gestionan operaciones CRUD mediante sentencias SQL estrictas (`INSERT INTO`, `SELECT`, `UPDATE`, `DELETE`) parametrizadas con *placeholders* (`?`) para neutralizar vulnerabilidades de inyección de código.
*   **Campos de Base de Datos Obligatorios:**
    *   `id` (Clave primaria, autoincremental)
    *   `nombre` (Texto, no nulo)
    *   `descripcion` (Texto)
    *   `cantidad` (Entero, no nulo)
    *   `precio` (Real, no nulo)
    *   `categoria` (Texto)

## ⚙️ Funcionalidades del Sistema
1.  **📥 Registrar Producto (Create):** Ingreso validado de nuevos productos al inventario local.
2.  **📊 Visualizar Inventario (Read):** Recuperación y despliegue tabular prolijo de todos los registros.
3.  **🔄 Actualizar Datos (Update):** Edición selectiva y dinámica de cualquier campo filtrado por ID único.
4.  **🗑️ Eliminar Producto (Delete):** Remoción física de registros individuales por clave primaria.
5.  **🔍 Búsqueda Avanzada:** Búsqueda exacta por ID o coincidencia de texto en campos clave mediante el operador `LIKE`.
6.  **⚠️ Reporte de Bajo Stock:** Filtro en tiempo real para alertar sobre productos cuya cantidad sea igual o inferior a un límite definido a demanda por el usuario.

## 🧪 Control Pedagógico de Excepciones (`try...except`)
El sistema integra un módulo dedicado que fuerza y captura de forma aislada y segura las excepciones requeridas por la cátedra para evitar desbordamientos o caídas del programa en producción:
*   `ValueError`
*   `ZeroDivisionError`
*   `IndexError`
*   `AttributeError`
*   `ImportError` (Manejo de contingencia para la librería opcional `colorama`)

---

## 🛠️ Cómo ejecutar el proyecto localmente / Installation & Usage

1. Asegúrate de tener instalado Python 3 en tu entorno local.
2. Clona o descarga este repositorio.
3. Abre una terminal de comandos (`cmd` o bash) en la ruta del archivo y ejecuta:

```bash
python proyecto_final.py
```

*Nota: El sistema operará bajo arquitectura Edge (100% Offline) y generará el archivo de base de datos relacional `inventario.db` de forma automática en el primer arranque.*

---
Developed by **Victor Damian Olivera**  
*Futuro Estudiante de Ingeniería en Informática (UNAJ) | Infraestructura y Resiliencia Local*
