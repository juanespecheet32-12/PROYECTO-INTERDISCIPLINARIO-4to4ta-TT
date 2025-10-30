import mysql.connector
from mysql.connector import errorcode
cursor = None
cnx = None

def ConectarBase():
    global cursor, cnx
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
    Consulta = "SELECT * FROM turnos;"
    cursor.execute(Consulta)
    for x in cursor:
        print(x)
    return cursor.fetchall()

def ConsultaInsertar(Id_Cliente, Id_Servicios, Id_Empleados, Fecha, Hora, Estado):
    sql = "INSERT INTO turnos (Id_Cliente, Id_Servicios, Id_Empleados, Fecha, Hora, Estado)VALUES(%s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, (Id_Cliente, Id_Servicios, Id_Empleados, Fecha, Hora, Estado))
    cnx.commit()
    return cursor.lastrowid

def Insertar_datos():
    Id_Cliente = int(input("Id del Cliente: "))
    Id_Servicios = int(input("Id del Servicio: "))
    Id_Empleados = int(input("Id del Empleado: "))
    Fecha = str(input("Fecha: "))
    Hora = str(input("Hora: "))
    Estado = str(input("Estado: "))
    ConsultaInsertar(Id_Cliente, Id_Servicios, Id_Empleados, Fecha, Hora, Estado)
ConectarBase()
Insertar_datos()
print(ConsultaSelect())
if cnx.is_connected():
    cnx.close()
    print("La conexión a la base de datos ha sido cerrada.")