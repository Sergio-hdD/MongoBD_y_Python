import pymongo as mg #importo la libreria de python que permite usar mongo

LOCAL_HOST_MONGO = "localhost"
PUERTO = "27017"
TIEMPO_FUERA_MONGO = 1000 #Si python tarda más de 1000 milisegundos en conectarse a mongo, se cancela la operación

MONGO_URI = 'mongodb://'+LOCAL_HOST_MONGO+":"+PUERTO+"/"

#------------------Conexión BÁSICA al servidor-----------------------
''' try:
    cliente = mg.MongoClient(MONGO_URI, serverSelectionTimeoutMS = TIEMPO_FUERA_MONGO) #creo un cliente
    cliente.server_info() #conecto al cliente
    print("Conexión con Mongo EXITOSA!!! ")
    cliente.close() #Cierro la conexión
except mg.errors.ServerSelectionTimeoutError as errorPorTiempo: #Si excede tiempo de espera de conexión 
    print("Error por tiempo: "+errorPorTiempo)
except mg.errors.ConnectionFailure as errorDeConexion: #Si no se puede conectar
    print("Fallo de conexión: "+errorDeConexion) '''
#----------------Fin conexión BÁSICA al servidor---------------------

DATA_BASE = "escuela"
COLECCION = "alumnos"

#------------------Conexión (TRABAJANDO CON DATOS) al servidor-----------------------
try:
    cliente = mg.MongoClient(MONGO_URI, serverSelectionTimeoutMS = TIEMPO_FUERA_MONGO) #creo un cliente
    baseDeDatos = cliente[DATA_BASE]
    coleccion = baseDeDatos[COLECCION]
    print("Alumnos/as: ")
    for documento in coleccion.find():
        print("Nombre: "+documento["nombre"]+", sexo: "+documento["sexo"]+", calificación: "+str(documento["calificacion"]))
    cliente.close() #Cierro la conexión
except mg.errors.ServerSelectionTimeoutError as errorPorTiempo: #Si excede tiempo de espera de conexión 
    print("Error por tiempo: "+errorPorTiempo)
except mg.errors.ConnectionFailure as errorDeConexion: #Si no se puede conectar
    print("Fallo de conexión: "+errorDeConexion)
#----------------Fin conexión (TRABAJANDO CON DATOS) al servidor---------------------