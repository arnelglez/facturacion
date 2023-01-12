from entidades.entCobroFactura import eCobroFactura
from funciones.tallerDB import BaseTaller

class mCobroFactura:

    def __init__(self):
        self.data = BaseTaller()
        

    def cargarDatosCobroFactura(self):
        listaCobroFactura = list()
        consulta = "SELECT * FROM cobrofactura"
        respuestas =  self.data.consultaAll(consulta)
        if len(respuestas) > 0:
            for respuesta in respuestas:
                ecobrofactura = eCobroFactura()
                ecobrofactura.setIdCobroFactura(respuesta[0])
                ecobrofactura.setCobro(respuesta[1])
                ecobrofactura.setTipo(respuesta[2])
                ecobrofactura.setFactura(respuesta[3])
                ecobrofactura.setMonto(respuesta[4])

                listaCobroFactura.append(ecobrofactura)
        
        return listaCobroFactura

    def obtenerCobroFacturaEspecifico(self, idcobrofactura):
        datos = list()
        datos.append(idcobrofactura)
        consulta = "SELECT * FROM cobrofactura WHERE idcobrofactura = ?"
        respuesta = self.data.consultaParametros(consulta, datos)
        ecobrofactura = eCobroFactura()
        if respuesta:
            ecobrofactura.setIdCobroFactura(respuesta[0])
            ecobrofactura.setCobro(respuesta[1])
            ecobrofactura.setTipo(respuesta[2])
            ecobrofactura.setFactura(respuesta[3])
            ecobrofactura.setMonto(respuesta[4])
        
        return ecobrofactura

    
    def guardarDatosCobroFactura(self, cobrofactura:eCobroFactura):
        consulta = "INSERT INTO cobrofactura (cobro, tipo, factura, monto) VALUES (?, ?, ?, ?)"
        datos = list()
        datos.append(cobrofactura.getCobro())
        datos.append(cobrofactura.getTipo())
        datos.append(cobrofactura.getFactura())
        datos.append(cobrofactura.getMonto())
        self.data.guardarEditar(consulta, datos)

    def editarDatosCobroFactura(self, cobrofactura:eCobroFactura, modo):
        consulta = "UPDATE cobrofactura SET cobro = ?, tipo = ?, factura = ?, monto = ? WHERE idcobrofactura = ?"
        datos = list()
        datos.append(cobrofactura.getCobro())
        datos.append(cobrofactura.getTipo())
        datos.append(cobrofactura.getFactura())
        datos.append(cobrofactura.getMonto())
        datos.append(cobrofactura.getIdCobroFactura())
        self.data.guardarEditar(consulta, datos)

    def eliminarDatosCobroFactura(self, idcobrofactura):
        datos = list()
        datos.append(idcobrofactura)
        consulta = 'DELETE FROM cobrofactura WHERE idcobrofactura = ?'
        self.data.guardarEditar(consulta, datos)
