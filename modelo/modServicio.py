from entidades.entServicio import eServicio
from funciones.tallerDB import BaseTaller

class mServicio:
    
    def __init__(self):
        self.data = BaseTaller()
        

    def cargarDatosServicio(self):
        listaServicio = list()
        consulta = "SELECT * FROM servicio"
        respuestas =  self.data.consultaAll(consulta)
        if len(respuestas) > 0:
            for respuesta in respuestas:
                eservicio = eServicio()
                eservicio.setIdServicio(respuesta[0])
                eservicio.setDescripcion(respuesta[1])
                eservicio.setPrecio(respuesta[2])
                eservicio.setUnidadMedida(respuesta[3])
                eservicio.setEquipo(respuesta[4])
                eservicio.setActivo(respuesta[5])

                listaServicio.append(eservicio)
        
        return listaServicio
   
    def obtenerServicioEspecifico(self, idservicio):
        datos = list()
        datos.append(idservicio)
        consulta = "SELECT * FROM servicio WHERE idservicio = ?"
        respuesta = self.data.consultaParametros(consulta, datos)
        eservicio = eServicio()
        if respuesta:
            eservicio.setIdServicio(respuesta[0])
            eservicio.setDescripcion(respuesta[1])
            eservicio.setPrecio(respuesta[2])
            eservicio.setUnidadMedida(respuesta[3])
            eservicio.setEquipo(respuesta[4])
            eservicio.setActivo(respuesta[5])
        
        return eservicio

    
    def guardarDatosServicio(self, servicio:eServicio):
        consulta = "INSERT INTO servicio (descripcion, precio, unidadmedida, equipo, activo) VALUES (?, ?, ?, ?, ?)"
        datos = list()
        datos.append(servicio.getDescripcion())
        datos.append(servicio.getPrecio())
        datos.append(servicio.getUnidadMedida())
        datos.append(servicio.getEquipo())
        datos.append(servicio.getActivo())
        self.data.guardarEditar(consulta, datos)

    def editarDatosServicio(self, servicio:eServicio, modo):
        consulta = "UPDATE servicio SET descripcion = ?, precio = ?, unidadmedida = ?, equipo = ?, activo = ? WHERE idservicio = ?"
        datos = list()
        datos.append(servicio.getDescripcion())
        datos.append(servicio.getPrecio())
        datos.append(servicio.getUnidadMedida())
        datos.append(servicio.getEquipo())
        datos.append(modo)
        datos.append(servicio.getIdServicio())
        self.data.guardarEditar(consulta, datos)
