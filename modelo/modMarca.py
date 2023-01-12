from datetime import date
from entidades.entMarca import eMarca
from funciones.tallerDB import BaseTaller

class mMarca:
    
    def __init__(self):
        self.data = BaseTaller()
        

    def cargarDatosMarca(self):
        listaMarca = list()
        consulta = "SELECT * FROM marca"
        respuestas =  self.data.consultaAll(consulta)
        if len(respuestas) > 0:
            for respuesta in respuestas:
                marca = eMarca()
                marca.setIdMarca(respuesta[0])
                marca.setDescripcion(respuesta[1])
                marca.setEquipo(respuesta[2])

                listaMarca.append(marca)
        
        return listaMarca
   
    def obtenerMarcaEspecifico(self, marca):
        dato = list()
        dato.append(marca)
        dato.append(marca)
        consulta = "SELECT * FROM marca WHERE idmarca = ? or descripcion = ?"
    
        respuesta = self.data.consultaParametros(consulta, dato)
        marca = eMarca()
        if respuesta:
            marca.setIdMarca(respuesta[0])
            marca.setDescripcion(respuesta[1])
            marca.setEquipo(respuesta[2])
        
        return marca
    
    def guardarDatosMarca(self, marca:eMarca):
        lista = list()
        lista.append(marca.getDescripcion())
        lista.append(marca.getEquipo())
        consulta = "INSERT INTO marca (descripcion, equipo) VALUES ( ?, ? )"

        self.data.guardarEditar(consulta, lista)

    def editarDatosMarca(self, marca:eMarca):
        lista = list()
        consulta = "UPDATE marca SET descripcion = ?, equipo = ? WHERE idmarca = ?"
        lista.append(marca.getDescripcion())
        lista.append(marca.getEquipo())
        lista.append(marca.getIdMarca())

        self.data.guardarEditar(consulta, lista)