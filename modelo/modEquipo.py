from entidades.entEquipo import eEquipo
from funciones.tallerDB import BaseTaller

class mEquipo:
    
    def __init__(self):
        self.data = BaseTaller()
        

    def cargarDatosEquipo(self):
        listaEquipo = list()
        consulta = "SELECT * FROM equipo"
        respuestas =  self.data.consultaAll(consulta)
        if len(respuestas) > 0:
            for respuesta in respuestas:
                equipo = eEquipo()
                equipo.setIdEquipo(respuesta[0])
                equipo.setDescripcion(respuesta[1])
                equipo.setActivo(respuesta[2])
                equipo.setMultiple(respuesta[3])

                listaEquipo.append(equipo)
        
        return listaEquipo
   
    def obtenerEquipoEspecifico(self, equipo):
        dato = list()
        dato.append(equipo)
        dato.append(equipo)
        consulta = "SELECT * FROM equipo WHERE idequipo = ? or descripcion = ?"
    
        respuesta = self.data.consultaParametros(consulta, dato)
        equipo = eEquipo()
        if respuesta:
            equipo.setIdEquipo(respuesta[0])
            equipo.setDescripcion(respuesta[1])
            equipo.setActivo(respuesta[2])
            equipo.setMultiple(respuesta[3])
        
        return equipo
    
    def guardarDatosEquipo(self, equipo:eEquipo):
        lista = list()
        lista.append(equipo.getDescripcion())
        lista.append(equipo.getMultiple())
        lista.append(1)
        consulta = "INSERT INTO equipo (descripcion, activo, multiple) VALUES ( ?, ?, ? )"

        self.data.guardarEditar(consulta, lista)

    def editarDatosEquipo(self, equipo:eEquipo, modo):
        lista = list()
        consulta = "UPDATE equipo SET descripcion = ?, activo = ?, multiple = ? WHERE idequipo = ?"
        lista.append(equipo.getDescripcion())
        lista.append(modo)
        lista.append(equipo.getMultiple())
        lista.append(equipo.getIdEquipo())
        
        self.data.guardarEditar(consulta, lista)