import mysql.connector
from mysql.connector import errorcode

cursor = None
cnx = None


def ConectarBase():
    global cnx, cursor
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


def ConsultaInsertar(nombre,patente,teléfono,historial_lavados):
    sql = "INSERT INTO clientes (nombre, patente, teléfono, historial_lavados)VALUES( %s, %s, %s, %s)"
    cursor.execute(sql,(nombre,patente,teléfono,historial_lavados))
    cnx.commit()
    return cursor.lastrowid

def insertar():
    nombre = str(input("Nombre: "))
    patente = str(input("Patente: "))
    telefono = int(input("Telefono: "))
    historial_lavados = int(input("Historial: "))
    ConsultaInsertar(nombre,patente,telefono,historial_lavados)

def Buscar_Cliente_Patente():
    consulta = "SELECT Patente FROM clientes GROUP BY Patente;"
    cursor.execute(consulta)
    for x in cursor:
        print(x)
    Patente = str(input("Ingrese una patente para buscar al cliente: "))
    Consulta = f"SELECT Nombre FROM clientes WHERE Patente = '{Patente}' GROUP BY Patente;"
    cursor.execute(Consulta)
    print("Se ha seleccionado la patente de:")
    for x in cursor:
        print(x)


ConectarBase()
Buscar_Cliente_Patente()

if cnx.is_connected():
    cnx.close()
    print("La conexión a la base de datos ha sido cerrada.")