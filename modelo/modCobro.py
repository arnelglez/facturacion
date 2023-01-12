from entidades.entCobro import eCobro
from funciones.tallerDB import BaseTaller

class mCobro:

    def __init__(self):
        self.data = BaseTaller()
        

    def cargarDatosCobro(self):
        listaCobro = list()
        consulta = "SELECT * FROM cobro"
        respuestas =  self.data.consultaAll(consulta)
        if len(respuestas) > 0:
            for respuesta in respuestas:
                ecobro = eCobro()
                ecobro.setIdCobro(respuesta[0])
                ecobro.setNoCobro(respuesta[1])
                ecobro.setUsuario(respuesta[2])
                ecobro.setCliente(respuesta[3])
                ecobro.setFecha(respuesta[4])
                ecobro.setTotalCobro(respuesta[5])
                ecobro.setTipoPago(respuesta[6])
                ecobro.setDocumento(respuesta[7])
                ecobro.setEstado(respuesta[8])
                ecobro.setFechaEmision(respuesta[9])

                listaCobro.append(ecobro)
        
        return listaCobro

    def obtenerCobroEspecifico(self, idcobro):
        datos = list()
        datos.append(idcobro)
        consulta = "SELECT * FROM cobro WHERE idcobro = ?"
        respuesta = self.data.consultaParametros(consulta, datos)
        ecobro = eCobro()
        if respuesta:
            ecobro.setIdCobro(respuesta[0])
            ecobro.setNoCobro(respuesta[1])
            ecobro.setUsuario(respuesta[2])
            ecobro.setCliente(respuesta[3])
            ecobro.setFecha(respuesta[4])
            ecobro.setTotalCobro(respuesta[5])
            ecobro.setTipoPago(respuesta[6])
            ecobro.setDocumento(respuesta[7])
            ecobro.setEstado(respuesta[8])
            ecobro.setFechaEmision(respuesta[9])
        
        return ecobro

    
    def guardarDatosCobro(self, cobro:eCobro):
        consulta = "INSERT INTO cobro (nocobro, usuario, cliente, fecha, totalcobro, tipopago, documento, estado, fechaemision) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
        datos = list()
        datos.append(cobro.getNoCobro())
        datos.append(cobro.getUsuario())
        datos.append(cobro.getCliente())
        datos.append(cobro.getFecha())
        datos.append(cobro.getTotalCobro())
        datos.append(cobro.getTipoPago())
        datos.append(cobro.getDocumento())
        datos.append(cobro.getEstado())
        datos.append(cobro.getFechaEmision())
        self.data.guardarEditar(consulta, datos)

    def editarDatosCobro(self, cobro:eCobro, modo):
        consulta = "UPDATE cobro SET nocobro = ?, usuario = ?, cliente = ?, fecha = ?, totalcobro = ?, tipopago = ?, documento = ?, estado = ?, fechaemision = ? WHERE idcobro = ?"
        datos = list()
        datos.append(cobro.getNoCobro())
        datos.append(cobro.getUsuario())
        datos.append(cobro.getCliente())
        datos.append(cobro.getFecha())
        datos.append(cobro.getTotalCobro())
        datos.append(cobro.getTipoPago())
        datos.append(cobro.getDocumento())
        datos.append(modo)
        datos.append(cobro.getFechaEmision())
        datos.append(cobro.getIdCobro())
        self.data.guardarEditar(consulta, datos)

    def eliminarCobro(self, idcobro):
        datos = list()
        datos.append(idcobro)
        consulta = 'DELETE FROM cobro WHERE idcobro = ?'
        self.data.guardarEditar(consulta, datos)