from entidades.entTaller import eTaller
from funciones.tallerDB import BaseTaller

class mTaller:
    def __init__(self):
        self.data = BaseTaller()

    
    def cargarValorTaller(self):
        consulta = "SELECT * FROM taller"
        respuesta = self.data.consultaOne(consulta)
        taller = eTaller()
        if respuesta:
            taller.setIdTaller(respuesta[0])
            taller.setNombre(respuesta[1])
            taller.setDireccion(respuesta[2])
            taller.setCuenta(respuesta[3])
            taller.setLogo(respuesta[4])
            taller.setLicencia(respuesta[5])
            taller.setSucursal(respuesta[6])
            taller.setCuentaMLC(respuesta[7])

        return taller

    def guardarDatosTaller(self, taller:eTaller):
        if taller.getIdTaller() == "":
            consulta = "INSERT INTO taller (nombre, direccion, cuenta, logo, licencia, sucursal, cuentamlc) VALUES (?, ?, ?, ? ,?, ?, ?)"
            datos = list()
            datos.append(taller.getNombre())
            datos.append(taller.getDireccion())
            datos.append(taller.getCuenta())
            datos.append(taller.getLogo())
            datos.append(taller.getLicencia())
            datos.append(taller.getSucursal())
            datos.append(taller.getCuentaMLC())

            self.data.guardarEditar(consulta, datos)
        
        else:
            consulta = "UPDATE taller SET nombre = ?, direccion = ?, cuenta = ?, logo = ?, licencia = ?, sucursal = ?, cuentamlc = ? WHERE idtaller = ?"
            datos = list()
            datos.append(taller.getNombre())
            datos.append(taller.getDireccion())
            datos.append(taller.getCuenta())
            datos.append(taller.getLogo())
            datos.append(taller.getLicencia())
            datos.append(taller.getSucursal())
            datos.append(taller.getCuentaMLC())
            datos.append(taller.getIdTaller())
            
            self.data.guardarEditar(consulta, datos)