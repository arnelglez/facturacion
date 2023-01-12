from entidades.entRecepcion import eRecepcion
from funciones.tallerDB import BaseTaller


class mRecepcion:

    def __init__(self):
        self.data = BaseTaller()
        

    def cargarDatosRecepcion(self):
        listaRecepcion = list()
        consulta = "SELECT * FROM recepcion"
        respuestas =  self.data.consultaAll(consulta)
        if len(respuestas) > 0:
            for respuesta in respuestas:
                erecepcion = eRecepcion()
                erecepcion.setIdRecepcion(respuesta[0])
                erecepcion.setNoRecepcion(respuesta[1])
                erecepcion.setUsuario(respuesta[2])
                erecepcion.setCliente(respuesta[3])
                erecepcion.setFecha(respuesta[4])
                erecepcion.setEstado(respuesta[5])

                listaRecepcion.append(erecepcion)
        
        return listaRecepcion

    def cargarRecepcionesFechas(self, fechainicio, fechafinal):
        datos = list()
        datos.append(fechainicio)
        datos.append(fechafinal)

        consulta = "SELECT * FROM recepcion WHERE fecha > ? "
   
    def obtenerRecepcionEspecifico(self, idrecepcion):
        datos = list()
        datos.append(idrecepcion)
        consulta = "SELECT * FROM recepcion WHERE idrecepcion = ?"
        respuesta = self.data.consultaParametros(consulta, datos)
        erecepcion = eRecepcion()
        if respuesta:
            erecepcion.setIdRecepcion(respuesta[0])
            erecepcion.setNoRecepcion(respuesta[1])
            erecepcion.setUsuario(respuesta[2])
            erecepcion.setCliente(respuesta[3])
            erecepcion.setFecha(respuesta[4])
            erecepcion.setEstado(respuesta[5])
        
        return erecepcion

    
    def guardarDatosRecepcion(self, recepcion:eRecepcion):
        consulta = "INSERT INTO recepcion (norecepcion, usuario, cliente, fecha, estado) VALUES (?, ?, ?, ?, ?)"
        datos = list()
        datos.append(recepcion.getNoRecepcion())
        datos.append(recepcion.getUsuario())
        datos.append(recepcion.getCliente())
        datos.append(recepcion.getFecha())
        datos.append(recepcion.getEstado())
        self.data.guardarEditar(consulta, datos)

    def editarDatosRecepcion(self, recepcion:eRecepcion, modo):
        consulta = "UPDATE recepcion SET norecepcion = ?, usuario = ?, cliente = ?, fecha = ?, estado = ? WHERE idrecepcion = ?"
        datos = list()
        datos.append(recepcion.getNoRecepcion())
        datos.append(recepcion.getUsuario())
        datos.append(recepcion.getCliente())
        datos.append(recepcion.getFecha())
        datos.append(modo)
        datos.append(recepcion.getIdRecepcion())
        self.data.guardarEditar(consulta, datos)

    def eliminarRecepcion(self, idrecepcion):
        datos = list()
        datos.append(idrecepcion)
        consulta = 'DELETE FROM recepcion WHERE idrecepcion = ?'
        self.data.guardarEditar(consulta, datos)