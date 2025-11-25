import mysql.connector
from mysql.connector import errorcode
import json

cursor = None
cnx = None

try:
    cnx = mysql.connector.connect(user="root", password="", host="Localhost", database="lavadero_de_autos")
    cursor = cnx.cursor(dictionary=True)
    print('Conexión establecida')

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('Usuario o contraseña incorrectos!')
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print('La base de datos no existe!')
    else:
        print(err)


def ConsultaSelect():
    Consulta = "SELECT * FROM clientes;"
    cursor.execute(Consulta)
    for x in cursor:
        print(x)
    return cursor.fetchall


def ConsultaInsertar(Nombre, Patente, Telefono, historial_lavados):
    sql = "INSERT INTO clientes (Nombre, Patente, Telefono, historial_lavados)VALUES( %s, %s, %s, %s)"
    cursor.execute(sql,(Nombre, Patente, Telefono, historial_lavados))
    cnx.commit()
    return cursor.lastrowid

def Buscar_Cliente_Patente():
    Patentes = "SELECT Id, Patente  FROM clientes GROUP BY Patente"
    cursor.execute(Patentes)
    for x in cursor:
        print(x)
    Patente = input("Ingrese una patente(XX-XXX-XX): ")
    Consulta = f"SELECT Nombre FROM clientes WHERE Patente = '{Patente}' GROUP BY Patente;"
    cursor.execute(Consulta)
    print("Ha seleccionado la patente de:")
    for x in cursor:
        print(x)
    return cursor.fetchall()

def Empleado_Insertar(Nombre, Rol, Horario, Servicio):
    sql = "INSERT INTO empleados (Nombre, Rol, Horario, Servicio)VALUES( %s, %s, %s, %s)"
    cursor.execute(sql, (Nombre, Rol, Horario, Servicio))
    cnx.commit()
    return cursor.lastrowid

def Turno_Insertar(Id_Cliente,Id_Servicios,Id_Empleados,Fecha,Hora,Estado):
    sql = "INSERT INTO turnos (Id_Cliente, Id_Servicios, Id_Empleados, Fecha, Hora, Estado)VALUES(%s,%s,%s,%s,%s,%s)"
    cursor.execute(sql, (Id_Cliente, Id_Servicios, Id_Empleados, Fecha, Hora, Estado))
    cnx.commit()
    return cursor.lastrowid

def Insertar_Cliente(Nombre, Patente, Telefono, historial_lavados):
    sql = "INSERT INTO clientes (Nombre, Patente, Teléfono, historial_lavados)VALUES(%s, %s, %s, %s)"
    cursor.execute(sql, (Nombre, Patente, Telefono, historial_lavados))
    cnx.commit()
    return cursor.lastrowid

def Buscar_Servicio_Demanda():
    consulta = "SELECT Nombre, Demanda FROM servicios WHERE Demanda = 'Alta';"
    cursor.execute(consulta)
    print("El servicio mas demandado es:")
    for x in cursor:
        print(x)
    return cursor.fetchall()

def Consulta_servicios():
    print("||||SERVICIOS||||")
    Consulta_servicios = "SELECT * FROM servicios;"
    cursor.execute(Consulta_servicios)
    for x in cursor:
        print(x)

def Consulta_empleados():
    print("||||EMPLEADOS||||")
    Consulta_empleados = "SELECT * FROM empleados;"
    cursor.execute(Consulta_empleados)
    for x in cursor:
        print(x)

def Consulta_turnos():
    print("||||TURNOS||||")
    Consulta_turnos = "SELECT * FROM turnos;"
    cursor.execute(Consulta_turnos)
    for x in cursor:
        print(x)

def Empleado_servicios():
    consulta = "SELECT nombre, rol, servicio FROM empleados WHERE servicio = 5;"
    cursor.execute(consulta)
    print("El empleado con mas servicios es:")
    for x in cursor:
        print(x)
    return cursor.fetchall()

def Consulta_clientes():
    print("||||CLIENTES||||")
    Consulta_clientes = "SELECT * FROM clientes;"
    cursor.execute(Consulta_clientes)
    for x in cursor:
        print(x)

def ConsultaTodo():
    Consulta_clientes()
    Consulta_empleados()
    Consulta_servicios()

def Registrar_Turno():
    Consulta_servicios()
    Consulta_empleados()
    Consulta_clientes()
    print("Ingrese los DATOS")
    Id_Cliente = int(input("ID del Cliente: "))
    Id_Servicios = int(input("ID del servicio (1-4): "))
    Id_Empleados = int(input("ID del empleado (1-5): "))
    Fecha = input("Ingrese la Fecha (AAAA/MM/DD): ")
    Hora = input("Ingrese la hora (XX:XX:XX): ")
    Estado = input("Ingrese El estado del Turno (Completo-En espera): ")
    Turno_Insertar(Id_Cliente, Id_Servicios, Id_Empleados, Fecha, Hora, Estado)

def Registrar_Cliente():
    Consulta_clientes()
    print("Ingrese los DATOS")
    nombre = input("Nombre: ")
    patente = input("Patente (XX-XXX-XX): ")
    telefono = int(input("Telefono (+54 11 XXX-XXX): "))
    historial_lavados = int(input("Historial (NO ingrese 0): "))
    Insertar_Cliente(nombre, patente, telefono, historial_lavados)

def ArchivoJSON():
    tablas = ['clientes', 'empleados', 'turnos', 'servicios']
    base_de_datos = "lavadero_de_autos.json"
    for x in range(0, 4):
        consulta = f"SELECT * FROM {tablas[x]};"
        cursor.execute(consulta)
        with open(base_de_datos, 'a', encoding='utf-8') as archivo:
            archivo.write(f"\n{tablas[x]}:\n")
        for y in cursor:
            print(str(y))
            with open(base_de_datos, 'a', encoding='utf-8') as archivo:
                json.dump(str(y), archivo, indent=4, ensure_ascii=False)
                archivo.write("\n")
    print(f"¡Archivo '{base_de_datos}' creado con éxito!")

def Registrar_Empleado():
    Consulta_empleados()
    print("Ingrese los DATOS")
    nombre = str(input("Nombre: "))
    rol = str(input("Rol: "))
    horario = input("Horario: ")
    estado = 0
    Empleado_Insertar(nombre, rol, horario, estado)

def Registrar_Turnos_Id(Id_Cliente):
    consulta = f"SELECT * FROM turnos WHERE id_cliente = {Id_Cliente};"
    cursor.execute(consulta)
    for x in cursor:
        print(x)

def Registrar_Turnos_Patente(Patente):
    consulta = f"""SELECT * 
    FROM turnos 
    WHERE id_cliente in(
        SELECT Id
        FROM clientes
        WHERE patente = '{Patente}')"""
    cursor.execute(consulta)
    for x in cursor:
        print(x)

def Registrar_Turnos_Telefono(Teléfono):
    consulta = f"""SELECT * 
    FROM turnos 
    WHERE id_cliente in(
        SELECT Id
        FROM clientes
        WHERE Teléfono = '{Teléfono}')"""
    cursor.execute(consulta)
    for x in cursor:
        print(x)

def Registrar_Turnos_Empleado(Nombre):
    consulta = f"""SELECT * 
    FROM turnos 
    WHERE id_empleados in(
        SELECT Id
        FROM empleados
        WHERE Nombre = '{Nombre}')"""
    cursor.execute(consulta)
    for x in cursor:
        print(x)

def Registrar_Turnos_Servicio(Nombre):
    consulta = f"""SELECT * 
    FROM turnos 
    WHERE id_servicios in(
        SELECT Id
        FROM servicios
        WHERE Nombre = '{Nombre}')"""
    cursor.execute(consulta)
    for x in cursor:
        print(x)

def Consultar_Turnos():
    while True:
        print("""
            ---------------------Menú-------------------------
            1. Registrar turnos por id
            2. Registrar turnos por patente
            3. Registrar turnos por teléfono
            4. Registrar turnos por empleado
            5. Registrar turnos por servicio
            0. Salir
            --------------------------------------------------
            """)
        opc = int(input("Ingrese que opcion quiere registrar: "))
        if opc == 1:
            Id_Cliente = int(input("Ingrese la id del cliente: "))
            Registrar_Turnos_Id(Id_Cliente)
        elif opc == 2:
            Patente = str(input("Ingrese la patente (XX-XXX-XX): "))
            Registrar_Turnos_Patente(Patente)
        elif opc == 3:
            Telefono = int(input("Ingrese el telefono (+54 9 11 XXX-XXX): "))
            Registrar_Turnos_Telefono(Telefono)
        elif opc == 4:
            Empleado = str(input("Ingrese el nombre del empleado: "))
            Registrar_Turnos_Empleado(Empleado)
        elif opc == 5:
            Servicio = str(input("Ingrese el nombre del servicio: "))
            Registrar_Turnos_Servicio(Servicio)
        elif opc == 0:
            break
        else:
            print("Opcion invalida")




def menu():
    print("""
    -----------------------Menú-----------------------------
    1.Registrar turno
    2.Buscar cliente por patente
    3.Registrar cliente
    4.Generar reporte ingresos diarios
    5.Empleado con mas servicios
    6.Servicio mas demandado
    7.Registrar empleado
    8.Consultar turnos
    0.Salir
    --------------------------------------------------------""")
    opc = int(input("Seleccione una opcion (0-6): "))

    if opc == 1:
        Registrar_Turno()
    elif opc == 2:
        Buscar_Cliente_Patente()
    elif opc == 3:
        Registrar_Cliente()
    elif opc == 4:
        ArchivoJSON()
    elif opc == 5:
        Empleado_servicios()
    elif opc == 6:
        Buscar_Servicio_Demanda()
    elif opc == 7:
        Registrar_Empleado()
    elif opc == 8:
        Consultar_Turnos()
    elif opc == 0:
        print("Saliendo del programa...")
    else:
        print("Error. Ha ingresado algo mal...")

Consultar_Turnos()

if cnx.is_connected():
    cnx.close()
    print("La conexión a la base de datos ha sido cerrada.")
