from tkinter import*
from tkinter import ttk #Es dónde está la tabla
from tkinter import messagebox #Sirve para mostrar mensajes
import pymongo as mg #importo la libreria de python que permite usar mongo
from bson.objectid import ObjectId  #De bson accedo a objectid y de ahí importo objectid y lo voy usar para convertir el id (como lo tengo en python) en ObjectID (como lo tengo en mongoDB), "bson" es de binari json, lo ocupa mongo para hacer la busqueda más rápida

LOCAL_HOST_MONGO = "localhost"
PUERTO = "27017"
TIEMPO_FUERA_MONGO = 1000 #Si python tarda más de 1000 milisegundos en conectarse a mongo, se cancela la operación

MONGO_URI = 'mongodb://'+LOCAL_HOST_MONGO+":"+PUERTO+"/"

DATA_BASE = "escuela"
COLECCION = "alumnos"
ID_ALUMNO = ""

#NOTA: (documento en mongo = registro en tabla tkinter)

#------------------Conexión al servidor-----------------------
#------ Con variables acecibles desde culquier lado -------
try:
    cliente = mg.MongoClient(MONGO_URI, serverSelectionTimeoutMS = TIEMPO_FUERA_MONGO) #creo un cliente
    baseDeDatos = cliente[DATA_BASE]
    coleccion = baseDeDatos[COLECCION]
except mg.errors.ServerSelectionTimeoutError as errorPorTiempo: #Si excede tiempo de espera de conexión 
    print("Error por tiempo: "+errorPorTiempo)
except mg.errors.ConnectionFailure as errorDeConexion: #Si no se puede conectar
    print("Fallo de conexión: "+errorDeConexion)
#----------------Fin conexión al servidor---------------------

''' 
#OPCIÓN 1
def mostrarDatos(nombre = "", sexo = "", calificacion = "" ): #Al ponerlos así los parámetros son opcionales, es decir si en algún lado no se los pasa no tira error y estarán vacios 
    objetoABuscar = {} #Inicia como diccionario vacío
    if len(nombre) != 0 : #Si no está vacío lo agrego al diccionario
        objetoABuscar["nombre"] = nombre
    if len(sexo) != 0 :
        objetoABuscar["sexo"] = sexo
    if len(calificacion) != 0 :
        objetoABuscar["calificacion"] = calificacion

    for documento in coleccion.find(objetoABuscar): #Si el objetoABuscar llegara vacío, el find buscaría sin tener en cuenta algún criterio (traería todo)
        tabla.insert('', 0, text = documento["_id"], values = documento["nombre"] )  #El primer parámetro es un registro padre, en este caso no tienen (todos serán padres), segundo un indice y los demás los valores
    cliente.close() #Cierro la conexión

def buscarDocumentoAlumno():
    limparPantalla()
    mostrarDatos(buscarPorNombre.get(), buscarPorSexo.get(), buscarPorCalificacion.get())
# FIN OPCIÓN 1
'''
# OPCIÓN 2
def mostrarDatos(objetoABuscar = {}): #Al ponerlo así el parámetro es opcional, es decir si en algún lado no se lo pasa no tira error y estará vacio 
    for documento in coleccion.find(objetoABuscar): #Si el objetoABuscar llegara vacío, el find buscaría sin tener en cuenta algún criterio (traería todo)
        tabla.insert('', 0, text = documento["_id"], values = documento["nombre"] )  #El primer parámetro es un registro padre, en este caso no tienen (todos serán padres), segundo un indice y los demás los valores
    cliente.close() #Cierro la conexión

def buscarDocumentoAlumno():
    objetoABuscar = {} #Inicia como diccionario vacío
    nombre = buscarPorNombre.get() 
    sexo = buscarPorSexo.get()
    calificacion = buscarPorCalificacion.get()
    if len(nombre) != 0 : #Si no está vacío lo agrego al diccionario
        objetoABuscar["nombre"] = nombre
    if len(sexo) != 0 :
        objetoABuscar["sexo"] = sexo
    if len(calificacion) != 0 :
        objetoABuscar["calificacion"] = calificacion
    
    if objetoABuscar == {} : #Si todos los campos de texto están vacíos
        messagebox.showerror(message = "Debe ingresar al menos un dato para la búsqueda")
    else: #Si se ingresa al menos un criterio de busqueda    
        limparPantalla()
        mostrarDatos(objetoABuscar)
#FIN OPCIÓN 2

def limparPantalla():
    for registro in tabla.get_children():
        tabla.delete( registro )  #Borro cada registro que se está mostrando en la tabla

def crearInputAndLabel(texto, labelRow, labelColumn, campoTextoRow, campoTextoColumn):
    Label(ventana, text = texto ).grid(row = labelRow, column = labelColumn, sticky = W+E) # Label(dónde va as estar, texto).grid(ubicación)
    #sticky = W+E, que abarque todo de izquierda a derecha 
    varEntry = Entry(ventana) #Va a estar en la ventana
    varEntry.grid(row = campoTextoRow, column = campoTextoColumn, sticky = W+E) # La posisión del input
    return varEntry

def limpiarInputs(): #Saca de los input que fueron agregados al tocar el boton "Agregar alumno" 
    nombre.delete(0, END) #Borra el input de inicio a fin
    sexo.delete(0, END)
    calificacion.delete(0, END)

def agregarDocumentoAlumno():
    if len(nombre.get()) != 0 and len(sexo.get()) != 0 and len(calificacion.get()) != 0 : #Si se cargaron todos los campos
        try:
            documento = {"nombre": nombre.get(), "sexo": sexo.get(), "calificacion": calificacion.get()} #Cargo un diccionario (así se llama a json en python) en una variable
            coleccion.insert(documento) #Inserto en la BD
            limpiarInputs()
        except mg.errors.ConnectionFailure as errorDeConexion: #Si no se puede conectar
            print("Fallo de conexión al intentar insertar: "+errorDeConexion)
    else:
        messagebox.showerror(message = "No puede haber campos vacios")
    limparPantalla() #Saco lo que se estaba mostrando en la tabla
    mostrarDatos() #Recargo para ver tambien lo último agregado

def editarDocumentoAlumno():
    global ID_ALUMNO #Lo declaro global para que entre acá y la inicializo más arriba como string vacío para poder usarla en otros lados
    if len(nombre.get()) != 0 and len(sexo.get()) != 0 and len(calificacion.get()) != 0 : #Si se cargaron todos los campos
        try:
            idBuscar = {"_id": ObjectId(ID_ALUMNO)}
            nuevosValoresDocumento = {"nombre": nombre.get(), "sexo": sexo.get(), "calificacion": calificacion.get()} #Cargo un diccionario (así se llama a json en python) en una variable
            coleccion.update(idBuscar, nuevosValoresDocumento) #Busca en la BD por idBuscar y reemplaza los nuevos valores
            limpiarInputs()
        except mg.errors.ConnectionFailure as errorDeConexion: #Si no se puede conectar
            print("Fallo de conexión al intentar actualizar: "+errorDeConexion)
    else:
        messagebox.showerror(message = "No puede haber campos vacios")
    limparPantalla() #Saco lo que se estaba mostrando en la tabla
    mostrarDatos() #Recargo para ver tambien lo último agregado 
    editar["state"] = "disabled" #cuando se de clic en el botón editar (es como llega acá) el estado del botón editar será disabled
    borrar["state"] = "disabled"
    agregar["state"] = "normal"

def borrarDocumentoAlumno():
    global ID_ALUMNO #Lo declaro global para que entre acá y la inicializo más arriba como string vacío para poder usarla en otros lados
    try:
        idBuscar = {"_id": ObjectId(ID_ALUMNO)}
        coleccion.delete_one(idBuscar) #Busca en la BD por idBuscar y lo borra
        limpiarInputs()
    except mg.errors.ConnectionFailure as errorDeConexion: #Si no se puede conectar
        print("Fallo de conexión al intentar eliminar: "+errorDeConexion)
    limparPantalla() #Saco lo que se estaba mostrando en la tabla
    mostrarDatos() #Recargo para ver tambien lo último agregado 
    borrar["state"] = "disabled" #cuando se de clic en el botón editar (es como llega acá) el estado del botón editar será disabled
    editar["state"] = "disabled"
    agregar["state"] = "normal"

def dobleClicTabla(envent):
    global ID_ALUMNO #Lo declaro global para que entre acá y la inicializo más arriba como string vacío para poder usarla en otros lados 
    ID_ALUMNO = str(tabla.item(tabla.selection())["text"]) #obtengo el item de la tabla que fue seleccionado (todo el registro) y de este solo campo de texto (el id), convierto a es string aunque ya esta en string (por las dudas)
    documento = coleccion.find({"_id": ObjectId(ID_ALUMNO)})[0] #Lo convierto porque MongoDB nececita un ObjectId, trae un documento completo (todos los campos) por id, pero como devuelve un array accedo al primero con [0]
    #Tomo del ducumento los valores de cada campo
    nombre.delete(0,END ) #Limpio la varible para no sobrescrir
    nombre.insert(0,documento["nombre"]) #Inserto desde el inicio ("0") el campo del documento que coincida con el texto
    sexo.delete(0,END ) 
    sexo.insert(0,documento["sexo"])
    calificacion.delete(0,END ) 
    calificacion.insert(0,documento["calificacion"])
    agregar["state"] = "disabled" #cuando se de doble clic en la tabla (es como llega acá) el estado del botón agregar será disabled
    editar["state"] = "normal"
    borrar["state"] = "normal"

ventana = Tk() #Creo una ventana
tabla = ttk.Treeview(ventana, columns = 2) #Treeview es una tabla en forma de árbol pero la voy a usar comol tabla común (primer parámetro es dónde va a estar la tabla, el segundo parámetro es cantidad de columnas que quiero que tenga) 
tabla.grid(row = 1, column = 0, columnspan = 2) #Creo una grila en la fila 1, columna 0 y que abarque 2 columnas
tabla.heading("#0",text = "ID") # la cabecera en la posición 0 va a ser ID 
tabla.heading("#1",text = "Nombre")
tabla.bind("<Double-Button-1>", dobleClicTabla) #Cuando se da doble clic llama a la función, <Button-1> para 1 clic y <Double-Button-1> para doble clic, (con el 1 toma el botón izquierdo del mouse, <Button-2> el derecho y <Button-3> el scroll)
#Hecho con doble clic ya que si lo hago con un clic, por ejemplo si tengo A y B, al hacer clic en A y luego clic en B toma el valor pero de A (es decir en el segundo clic tama el primero)... pidiendo doble clic para elegir, se evita esto

#Nombre
nombre = crearInputAndLabel("Nombre", 2, 0, 2, 1)
nombre.focus() #Para que cuando inicie la ventana el cursor esté en este campo de texto
#Sexo
sexo = crearInputAndLabel("Sexo", 3, 0, 3, 1)
#Calificación
calificacion = crearInputAndLabel("Calificación", 4, 0, 4, 1)

#Botón agregar
agregar = Button(ventana,text = "Agregar alumno", command = agregarDocumentoAlumno, bg = "green", fg = "white") #Command llama a la función al tocar el botón, bg es el fondo, fg la letra 
agregar.grid(row = 5, columnspan = 2, sticky = W+E) #sticky = W+E, que abarque todo de izquierda a derecha   

#Botón editar 
editar = Button(ventana,text = "Editar alumno", command = editarDocumentoAlumno, bg = "yellow") 
editar.grid(row = 6, columnspan = 2, sticky = W+E) 
editar["state"] = "disabled" #El botón arranca en estado disabled

#Botón borrar 
borrar = Button(ventana,text = "Borrar alumno", command = borrarDocumentoAlumno, bg = "red", fg = "white") 
borrar.grid(row = 7, columnspan = 2, sticky = W+E)
borrar["state"] = "disabled" #El botón arranca en estado disabled

#Buscar por nombre
buscarPorNombre = crearInputAndLabel("Buscar por nombre", 8, 0, 8, 1)
#Buscar por sexo
buscarPorSexo = crearInputAndLabel("Buscar por sexo", 9, 0, 9, 1)
#Buscar por calificación
buscarPorCalificacion = crearInputAndLabel("Buscar por calificación", 10, 0, 10, 1)
#Botón buscar 
buscar = Button(ventana,text = "Buscar alumno", command = buscarDocumentoAlumno, bg = "blue", fg = "white") 
buscar.grid(row = 11, columnspan = 2, sticky = W+E) 

mostrarDatos()
ventana.mainloop() #Ciclo principal