from datetime import date
from entidades.entModelo import eModelo
from funciones.tallerDB import BaseTaller

class mModelo:
    
    def __init__(self):
        self.data = BaseTaller()
        

    def cargarDatosModelo(self):
        listaModelo = list()
        consulta = "SELECT * FROM modelo"
        respuestas =  self.data.consultaAll(consulta)
        if len(respuestas) > 0:
            for respuesta in respuestas:
                modelo = eModelo()
                modelo.setIdModelo(respuesta[0])
                modelo.setDescripcion(respuesta[1])
                modelo.setMarca(respuesta[2])
                modelo.setEquipo(respuesta[3])

                listaModelo.append(modelo)
        
        return listaModelo
   
    def obtenerModeloEspecifico(self, modelo):
        dato = list()
        dato.append(modelo)
        dato.append(modelo)
        consulta = "SELECT * FROM modelo WHERE idmodelo = ? or  descripcion = ?"
    
        respuesta = self.data.consultaParametros(consulta, dato)
        modelo = eModelo()
        if respuesta:
            modelo.setIdModelo(respuesta[0])
            modelo.setDescripcion(respuesta[1])
            modelo.setMarca(respuesta[2])
            modelo.setEquipo(respuesta[3])
        
        return modelo
        
    def guardarDatosModelo(self, modelo:eModelo):
        lista = list()
        lista.append(modelo.getDescripcion())
        lista.append(modelo.getMarca())
        lista.append(modelo.getEquipo())
        consulta = "INSERT INTO modelo (descripcion, marca, equipo) VALUES ( ?, ?, ? )"

        self.data.guardarEditar(consulta, lista)

    def editarDatosModelo(self, modelo:eModelo):
        lista = list()
        consulta = "UPDATE modelo SET descripcion = ?, marca = ?, equipo = ? WHERE idmodelo = ?"
        lista.append(modelo.getDescripcion())
        lista.append(modelo.getMarca())
        lista.append(modelo.getEquipo())
        lista.append(modelo.getIdModelo())

        self.data.guardarEditar(consulta, lista)