import os
import sqlite3

# Intentamos importar colorama para darle una estética premium a la terminal
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    COLOR_ACTIVO = True
except ImportError:
    COLOR_ACTIVO = False

# =================================================================
# 🗃️ CONFIGURACIÓN DE LA BASE DE DATOS LOCAL (SQLite)
# =================================================================
def inicializar_base_datos():
    """
    Establece la conexión local con SQLite y crea la tabla 'productos'
    respetando de forma estricta los campos obligatorios de la consigna.
    """
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL,
            categoria TEXT
        )
    """)
    conexion.commit()
    return conexion

# =================================================================
# ⚙️ MÓDULOS DE GESTIÓN OBLIGATORIOS (CRUD)
# =================================================================
def registrar_producto(conexion):
    """Permite el ingreso de un nuevo producto validando los tipos de datos."""
    print("\n--- 📥 REGISTRAR NUEVO PRODUCTO ---")
    try:
        nombre = input("Nombre del producto (Obligatorio): ").strip()
        descripcion = input("Breve descripción: ").strip()
        cantidad = int(input("Cantidad disponible (Entero): "))
        precio = float(input("Precio unitario (Real): "))
        categoria = input("Categoría: ").strip()

        if not nombre:
            raise ValueError("El campo nombre es obligatorio.")

        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria) 
            VALUES (?, ?, ?, ?, ?)
        """, (nombre, descripcion, cantidad, precio, categoria))
        conexion.commit()
        print("✅ Producto registrado con éxito en inventario.db.")
    except ValueError as e:
        print(f"❌ Error de Validación: {e}")

def visualizar_productos(conexion):
    """Muestra en formato tabular todos los datos registrados en la tabla."""
    print("\n--- 📊 INVENTARIO GLOBAL DE PRODUCTOS ---")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()

    if not productos:
        print("📭 El inventario se encuentra vacío.")
        return

    encabezado = f"{'ID':<5} | {'Nombre':<15} | {'Descripción':<20} | {'Cant':<6} | {'Precio':<10} | {'Categoría':<12}"
    print(encabezado)
    print("-" * 78)
    for p in productos:
        print(f"{p[0]:<5} | {p[1]:<15} | {p[2]:<20} | {p[3]:<6} | ${p[4]:<9.2f} | {p[5]:<12}")

def actualizar_producto(conexion):
    """Modifica los valores de un producto existente localizándolo mediante su ID."""
    print("\n--- 🔄 ACTUALIZAR DATOS DE PRODUCTO ---")
    try:
        id_prod = int(input("Ingrese el ID del producto a modificar: "))
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos WHERE id = ?", (id_prod,))
        if not cursor.fetchone():
            print("❌ El ID especificado no existe.")
            return

        print("Deje en blanco si no desea modificar el campo.")
        nuevo_nombre = input("Nuevo Nombre: ").strip()
        nueva_desc = input("Nueva Descripción: ").strip()
        nueva_cant = input("Nueva Cantidad: ").strip()
        nuevo_precio = input("Nuevo Precio: ").strip()
        nueva_cat = input("Nueva Categoría: ").strip()

        if nuevo_nombre: cursor.execute("UPDATE productos SET nombre = ? WHERE id = ?", (nuevo_nombre, id_prod))
        if nueva_desc: cursor.execute("UPDATE productos SET descripcion = ? WHERE id = ?", (nueva_desc, id_prod))
        if nueva_cant: cursor.execute("UPDATE productos SET cantidad = ? WHERE id = ?", (int(nueva_cant), id_prod))
        if nuevo_precio: cursor.execute("UPDATE productos SET precio = ? WHERE id = ?", (float(nuevo_precio), id_prod))
        if nueva_cat: cursor.execute("UPDATE productos SET categoria = ? WHERE id = ?", (nueva_cat, id_prod))
        
        conexion.commit()
        print("✅ Producto actualizado correctamente.")
    except ValueError:
        print("❌ Error: Tipo de dato incorrecto en la edición.")

def eliminar_producto(conexion):
    """Remueve de la base de datos un registro filtrado por su clave primaria."""
    print("\n--- 🗑️ ELIMINACIÓN DE PRODUCTO ---")
    try:
        id_prod = int(input("Ingrese el ID del producto a eliminar: "))
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM productos WHERE id = ?", (id_prod,))
        conexion.commit()
        print("✅ Operación completada. Si el ID existía, fue eliminado.")
    except ValueError:
        print("❌ El ID debe ser un número entero.")

def buscar_producto(conexion):
    """Módulo flexible: busca por ID exacto o por coincidencia en texto de campos."""
    print("\n--- 🔍 BÚSQUEDA AVANZADA ---")
    print("1. Buscar por ID")
    print("2. Buscar por Nombre o Categoría")
    opc = input("Seleccione tipo de búsqueda (1-2): ").strip()
    cursor = conexion.cursor()

    if opc == "1":
        try:
            id_prod = int(input("ID del producto: "))
            cursor.execute("SELECT * FROM productos WHERE id = ?", (id_prod,))
            p = cursor.fetchone()
            if p:
                print(f"\n📍 ID: {p[0]} | {p[1]} | Desc: {p[2]} | Cant: {p[3]} | ${p[4]:.2f} | Cat: {p[5]}")
            else:
                print("❌ No se encontró ningún producto con ese ID.")
        except ValueError:
            print("❌ Entrada inválida.")
    elif opc == "2":
        termino = input("Texto a buscar (Nombre/Categoría): ").strip()
        cursor.execute("SELECT * FROM productos WHERE nombre LIKE ? OR categoria LIKE ?", ("%"+termino+"%", "%"+termino+"%"))
        resultados = cursor.fetchall()
        if resultados:
            for p in resultados:
                print(f"📍 ID: {p[0]} | {p[1]} | Cant: {p[3]} | ${p[4]:.2f} | Cat: {p[5]}")
        else:
            print("❌ Sin coincidencias.")

def generar_reporte_bajo_stock(conexion):
    """Filtra y lista productos cuyo stock es menor o igual al límite especificado."""
    print("\n--- ⚠️ REPORTE DE BAJO STOCK ---")
    try:
        limite = int(input("Defina el límite de alerta (Cantidad máxima): "))
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos WHERE cantidad <= ?", (limite,))
        alertas = cursor.fetchall()

        if not alertas:
            print("✅ Excelente: No hay productos en riesgo de quiebre de stock.")
            return

        print(f"\n🚨 PRODUCTOS CON STOCK CRÍTICO (<= {limite}):")
        for p in alertas:
            print(f"   👉 [ID: {p[0]}] {p[1]} | Cantidad Actual: {p[3]} unidades")
    except ValueError:
        print("❌ Debe ingresar un valor numérico entero.")

# =================================================================
# 🚨 BANCO PEDAGÓGICO DE EXCEPCIONES REQUERIDO
# =================================================================
def ejecutar_pruebas_excepciones():
    """Demuestra al evaluador la correcta captura de las excepciones de la cátedra."""
    print("\n=== 🧪 BANCO DE PRUEBAS DE EXCEPCIONES ===")
    
    try:
        print("\n[Fallo 1] Provocando ZeroDivisionError...")
        _ = 5 / 0
    except ZeroDivisionError as e:
        print(f"✅ Captura Segura -> ZeroDivisionError: {e}")

    try:
        print("\n[Fallo 2] Provocando IndexError...")
        lista = [1, 2]
        _ = lista[5]
    except IndexError as e:
        print(f"✅ Captura Segura -> IndexError: {e}")

    try:
        print("\n[Fallo 3] Provocando AttributeError...")
        entero = 100
        entero.lower()
    except AttributeError as e:
        print(f"✅ Captura Segura -> AttributeError: {e}")

    try:
        print("\n[Fallo 4] Provocando ValueError...")
        _ = int("TextoInvalido")
    except ValueError as e:
        print(f"✅ Captura Segura -> ValueError: {e}")

    print("\nPresione ENTER para continuar...")
    input()

# =================================================================
# 💻 MENÚ PRINCIPAL INTERACTIVO
# =================================================================
def main():
    conexion = inicializar_base_datos()

    while True:
        print("\n=======================================================")
        print("    SISTEMA DE CONTROL DE INVENTARIO - TALENTO TECH    ")
        print("=======================================================")
        print(" 1. 📥 Registrar Producto (Create)")
        print(" 2. 📊 Visualizar Inventario Completo (Read)")
        print(" 3. 🔄 Actualizar Datos de un Producto (Update)")
        print(" 4. 🗑️ Eliminar Producto (Delete)")
        print(" 5. 🔍 Búsqueda de Productos (ID / Nombre / Cat)")
        print(" 6. ⚠️ Generar Reporte de Bajo Stock")
        print(" 7. 🧪 Ejecutar Pruebas de Excepciones de Cátedra")
        print(" 8. ❌ Salir del Sistema")
        print("=======================================================")

        opcion = input("Seleccione opción (1-8): ").strip()

        if opcion == "1": registrar_producto(conexion)
        elif opcion == "2": visualizar_productos(conexion)
        elif opcion == "3": actualizar_producto(conexion)
        elif opcion == "4": eliminar_producto(conexion)
        elif opcion == "5": buscar_producto(conexion)
        elif opcion == "6": generar_reporte_bajo_stock(conexion)
        elif opcion == "7": ejecutar_pruebas_excepciones()
        elif opcion == "8":
            print("\nCerrando sistema. Conexión SQLite liberada de forma segura.")
            conexion.close()
            break
        else:
            print("❌ Selección no válida. Reintente.")

if __name__ == "__main__":
    main()