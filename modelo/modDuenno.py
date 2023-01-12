from entidades.entDuenno import eDuenno
from funciones.tallerDB import BaseTaller

class mDuenno():
    def __init__(self):
        self.data = BaseTaller()
    

    def cargarDatosDuenno(self):
        consulta = "SELECT * FROM duenno"
        respuesta = self.data.consultaOne(consulta)        
        eduenno = eDuenno()
        if respuesta:
            eduenno.setIdDuenno(respuesta[0])
            eduenno.setNombre(respuesta[1])
            eduenno.setApellidos(respuesta[2])
            eduenno.setCarnet(respuesta[3])
            eduenno.setLicencia(respuesta[4])
            eduenno.setTelefono(respuesta[5])

        return eduenno

    def guardarDatosDuenno(self, duenno:eDuenno):
        if duenno.getIdDuenno() == "":
            consulta = "INSERT INTO duenno (nombre, apellidos, carnet, licencia, telefono) VALUES (?, ?, ?, ?, ?)"
            datos = list()
            datos.append(duenno.getNombre())
            datos.append(duenno.getApellidos())
            datos.append(duenno.getCarnet())
            datos.append(duenno.getLicencia())
            datos.append(duenno.getTelefono())

            self.data.guardarEditar(consulta, datos)
        
        else:
            consulta = "UPDATE duenno SET nombre = ?, apellidos = ?, carnet = ?, licencia = ?, telefono = ? WHERE idduenno = ?"
            datos = list()
            datos.append(duenno.getNombre())
            datos.append(duenno.getApellidos())
            datos.append(duenno.getCarnet())
            datos.append(duenno.getLicencia())
            datos.append(duenno.getTelefono())
            datos.append(duenno.getIdDuenno())
            
            self.data.guardarEditar(consulta, datos)