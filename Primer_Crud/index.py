from tkinter import*
from tkinter import ttk #Es dónde está la tabla
from tkinter import messagebox #Sirve para mostrar mensajes
import pymongo as mg #importo la libreria de python que permite usar mongo

LOCAL_HOST_MONGO = "localhost"
PUERTO = "27017"
TIEMPO_FUERA_MONGO = 1000 #Si python tarda más de 1000 milisegundos en conectarse a mongo, se cancela la operación

MONGO_URI = 'mongodb://'+LOCAL_HOST_MONGO+":"+PUERTO+"/"

DATA_BASE = "escuela"
COLECCION = "alumnos"

#------------------Conexión (TRABAJANDO CON DATOS) al servidor-----------------------
def mostrarDatos(tabla):
    try:
        cliente = mg.MongoClient(MONGO_URI, serverSelectionTimeoutMS = TIEMPO_FUERA_MONGO) #creo un cliente
        baseDeDatos = cliente[DATA_BASE]
        coleccion = baseDeDatos[COLECCION]
        for documento in coleccion.find():
            tabla.insert('', 0, text = documento["_id"], values = (documento["nombre"], documento["sexo"], documento["calificacion"]) )  #El primer parámetro es un registro padre, en este caso no tienen (todos serán padres), segundo un indice y los demás los valores
        cliente.close() #Cierro la conexión
    except mg.errors.ServerSelectionTimeoutError as errorPorTiempo: #Si excede tiempo de espera de conexión 
        print("Error por tiempo: "+errorPorTiempo)
    except mg.errors.ConnectionFailure as errorDeConexion: #Si no se puede conectar
        print("Fallo de conexión: "+errorDeConexion)
#----------------Fin conexión (TRABAJANDO CON DATOS) al servidor---------------------

ventana = Tk() #Creo una ventana
tabla = ttk.Treeview(ventana, columns = ("#0", "#1", "#2", "#3")) #Treeview es una tabla en forma de árbol pero la voy a usar comol tabla común (primer parámetro es dónde va a estar la tabla, el segundo parámetro es cantidad de columnas que quiero que tenga) 
tabla.grid(row = 1, column = 0, columnspan = 4) #Creo una grila en la fila 1, columna 0 y que abarque 2 columnas
tabla.heading("#0",text = "ID") # la cabecera en la posición 0 va a ser ID 
tabla.heading("#1",text = "Nombre")
tabla.heading("#2",text = "Sexo")
tabla.heading("#3",text = "Calificación")
mostrarDatos(tabla)
ventana.mainloop() #Ciclo principal