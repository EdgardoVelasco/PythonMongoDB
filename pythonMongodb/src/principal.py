import pymongo

'''
Clase alumno que usaremos para transportar información
'''
class Alumno:
    def __init__(self,id:int ,nombre: str, edad:int):
        self.id=id
        self.nombre=nombre
        self.edad=edad
    def __str__(self):
        return "Persona[id:{}, nombre:{}, edad:{}]".format(self.id, self.nombre, self.edad)
        

'''
método usado para extraer la información de mongo
'''
def info_mongo():
    info={}
    with open("C:\\Users\\40024436\\Desktop\\datos.txt") as archivo:
        for linea in archivo:
            separar=linea.split("=")
            info[separar[0]]=separar[1]
    return info

'''
Método usado para crera la conexión de mongo db
'''
def conex_mongo():
    datos=info_mongo() 
    try:
        conex=pymongo.MongoClient(datos["url"])
        return conex["escuela"]
    except Exception as ex:
        print("algo paso con la conex: {}".format(ex))

def menu():
    print("-.-.-.-.-.Menu-.-.-.-.-.")
    print("1.-Insertar alumno")
    print("2.-Ver alumnos")
    print("3.-Actualizar alumno por id")
    print("4.-Borrar alumno por id")
    print("5.-Salir")
    print("-.-.-.-.-.-.-.-.-.-.-.-")
    opc=input("Seleccióna opción: ")
    return int(opc) if opc.isdigit() else 0
    

'''Método insertar'''
def insertar_alumno(mongo, alumno:Alumno):
    coleccion=mongo["alumnos"]
    insert={
        "_id":alumno.id, 
        "nombre":alumno.nombre, 
        "edad":alumno.edad
        }
    result=coleccion.insert_one(insert)
    print(result.inserted_id)

'''Método mostrar todos'''
def mostrar_todos(mongo):
    coleccion=mongo["alumnos"]
    todos=coleccion.find();
    for tmp in todos:
        print(tmp)

def buscar_alumno_id(mongo, id:int):
    coleccion=mongo["alumnos"]
    alumno=coleccion.find_one({"_id":id})
    return Alumno(alumno["_id"], alumno["nombre"], alumno["edad"]) if alumno!=None else None

def actualizar_alumno(mongo,alumno:Alumno):
    coleccion=mongo["alumnos"]
    actualizando=coleccion.update_one({"_id":alumno.id},{"$set":{"nombre":alumno.nombre, "edad":alumno.edad}});
    print("actualizado" if actualizando.modified_count>0 else "no se actualizo")


def eliminar_alumno(mongo, alumno:Alumno):
    coleccion=mongo["alumnos"]
    eliminar=coleccion.delete_one({"_id":alumno.id})
    print("eliminado" if eliminar.deleted_count>0 else "no se elimino")


if __name__=="__main__":
    base=conex_mongo()
    opc=menu()
    while opc!=5:
        if opc==1:
            print()
            print("-.-.-.Insertar alumno-.-.-.-.")
            id=int(input("Escribe un id: "))
            nombre=input("Escribe nombre: ")
            edad=int(input("Escribe edad: "))
            insertar_alumno(base, Alumno(id, nombre, edad))
            print()
            opc=menu()
            
        elif opc==2:
            print("-.-.-.-.Ver todos los alumnos.-.-.-.")
            mostrar_todos(base)
            print()
            opc=menu()
        
        elif opc==3:
            print()
            print("-.-.-.-.-.-.Actualizar alumno-.-.-.-.")
            id=int(input("id de alumno a actualizar: "))
            alumno_encontrado=buscar_alumno_id(base, id)
            if alumno_encontrado!=None:
                print(alumno_encontrado)
                nombre_n=input("Nuevo nombre de alumno: ")
                edad_n=int(input("Nueva edad: "))
                alumno_encontrado.nombre=nombre_n
                alumno_encontrado.edad=edad_n
                actualizar_alumno(base, alumno_encontrado)
            else:
                print("no existe el alumno")
            opc=menu()
            print()

        elif opc==4:
            print()
            print("-.-.-.-.-.Eliminar alumno-.-.-.-.")
            id_b=int(input("id de alumno a eliminar: "))
            alumno_encontrado=buscar_alumno_id(base, id_b)
            if alumno_encontrado!=None:
                eliminar_alumno(base,alumno_encontrado)
            else:
                print("no existe")
            opc=menu()
            print()
        else:
            print("opción iválida intenta de nuevo")
            opc=menu()







    
    

