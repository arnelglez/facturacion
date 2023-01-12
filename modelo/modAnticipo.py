from entidades.entAnticipo import eAnticipo
from funciones.tallerDB import BaseTaller

class mAnticipo:

    def __init__(self):
        self.data = BaseTaller()
        

    def cargarDatosAnticipo(self):
        listaAnticipo = list()
        consulta = "SELECT * FROM anticipo"
        respuestas =  self.data.consultaAll(consulta)
        if len(respuestas) > 0:
            for respuesta in respuestas:
                eanticipo = eAnticipo()
                eanticipo.setIdAnticipo(respuesta[0])
                eanticipo.setCobroFactura(respuesta[1])
                eanticipo.setUsuario(respuesta[2])
                eanticipo.setCliente(respuesta[3])
                eanticipo.setNoAnticipo(respuesta[4])
                eanticipo.setFecha(respuesta[5])
                eanticipo.setDocumento(respuesta[6])
                eanticipo.setFechaEmision(respuesta[7])
                eanticipo.setFactura(respuesta[8])
                eanticipo.setMonto(respuesta[9])
                eanticipo.setEstado(respuesta[10])

                listaAnticipo.append(eanticipo)
        
        return listaAnticipo

    def obtenerAnticipoEspecifico(self, idanticipo):
        datos = list()
        datos.append(idanticipo)
        consulta = "SELECT * FROM anticipo WHERE idanticipo = ?"
        respuesta = self.data.consultaParametros(consulta, datos)
        eanticipo = eAnticipo()
        if respuesta:
            eanticipo.setIdAnticipo(respuesta[0])
            eanticipo.setCobroFactura(respuesta[1])
            eanticipo.setUsuario(respuesta[2])
            eanticipo.setCliente(respuesta[3])
            eanticipo.setNoAnticipo(respuesta[4])
            eanticipo.setFecha(respuesta[5])
            eanticipo.setDocumento(respuesta[6])
            eanticipo.setFechaEmision(respuesta[7])
            eanticipo.setFactura(respuesta[8])
            eanticipo.setMonto(respuesta[9])
            eanticipo.setEstado(respuesta[10])
        
        return eanticipo

    
    def guardarDatosAnticipo(self, anticipo:eAnticipo):
        consulta = "INSERT INTO anticipo (cobrofactura, usuario, cliente, noanticipo, fecha, nodocumento, fechaemision, factura, monto, estado) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        datos = list()
        datos.append(anticipo.getCobroFactura())
        datos.append(anticipo.getUsuario())
        datos.append(anticipo.getCliente())
        datos.append(anticipo.getNoAnticipo())
        datos.append(anticipo.getFecha())
        datos.append(anticipo.getDocumento())
        datos.append(anticipo.getFechaEmision())
        datos.append(anticipo.getFactura())
        datos.append(anticipo.getMonto())
        datos.append(anticipo.getEstado())
        self.data.guardarEditar(consulta, datos)

    def editarDatosAnticipo(self, anticipo:eAnticipo, modo):
        consulta = "UPDATE anticipo SET cobrofactura = ?, usuario = ?, cliente = ?, noanticipo = ?, fecha = ?, nodocumento = ?, fechaemision = ?, factura = ?, monto = ?, estado = ? WHERE idanticipo = ?"
        datos = list()
        datos.append(anticipo.getCobroFactura())
        datos.append(anticipo.getUsuario())
        datos.append(anticipo.getCliente())
        datos.append(anticipo.getNoAnticipo())
        datos.append(anticipo.getFecha())
        datos.append(anticipo.getDocumento())
        datos.append(anticipo.getFechaEmision())
        datos.append(anticipo.getFactura())
        datos.append(anticipo.getMonto())
        datos.append(modo)
        datos.append(anticipo.getIdAnticipo())
        self.data.guardarEditar(consulta, datos)

    def eliminarDatosAnticipo(self, idanticipo):
        datos = list()
        datos.append(idanticipo)
        consulta = 'DELETE FROM anticipo WHERE idanticipo = ?'
        self.data.guardarEditar(consulta, datos)
