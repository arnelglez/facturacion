from entidades.entFecha import eFecha
from funciones.tallerDB import BaseTaller

class mFecha:
    def __init__(self):
        self.data = BaseTaller()

    
    def cargarValorFecha(self):
        consulta = "SELECT * FROM fecha"
        respuesta = self.data.consultaOne(consulta)
        fecha = eFecha()
        if respuesta:
            fecha.setIdFecha(respuesta[0])
            fecha.setFechaProcesamiento(respuesta[1])

        return fecha

    def guardarDatosFecha(self, fecha:eFecha):
        if fecha.getIdFecha() == "":
            consulta = "INSERT INTO fecha (fecha_procesamiento) VALUES ( ? )"
            datos = list()
            datos.append(fecha.getFechaProcesamiento())

            self.data.guardarEditar(consulta, datos)
        
        else:
            consulta = "UPDATE fecha SET fecha_procesamiento = ? WHERE idfecha = ?"
            datos = list()
            datos.append(fecha.getFechaProcesamiento())
            datos.append(fecha.getIdFecha())
            
            self.data.guardarEditar(consulta, datos)