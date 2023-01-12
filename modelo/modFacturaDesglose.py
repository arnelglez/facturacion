from entidades.entFacturaDesglose import eFacturaDesglose
from funciones.tallerDB import BaseTaller

class mFacturaDesglose:
    
    def __init__(self):
        self.data = BaseTaller()

    def cargarDatosFacturaDesglose(self):
        listaFacturaDesglose = list()
        consulta = "SELECT * FROM facturadesglose"
        respuestas =  self.data.consultaAll(consulta)
        if len(respuestas) > 0:
            for respuesta in respuestas:
                efacturadesglose = eFacturaDesglose()
                efacturadesglose.setIdFacturaDesglose(respuesta[0])
                efacturadesglose.setFactura(respuesta[1])
                efacturadesglose.setTipo(respuesta[2])
                efacturadesglose.setServicio(respuesta[3])
                efacturadesglose.setInventario(respuesta[4])
                efacturadesglose.setCantidad(respuesta[5])
                efacturadesglose.setPrecio(respuesta[6])
                efacturadesglose.setPrecioTotal(respuesta[7])

                listaFacturaDesglose.append(efacturadesglose)
        
        return listaFacturaDesglose

   
    def obtenerFacturaDesgloseEspecifico(self, idfacdesglose):
        datos = list()
        datos.append(idfacdesglose)
        consulta = "SELECT * FROM facturadesglose WHERE idfacdesglose = ?"
        respuesta = self.data.consultaParametros(consulta, datos)
        efacturadesglose = eFacturaDesglose()
        if respuesta:
            efacturadesglose.setIdFacturaDesglose(respuesta[0])
            efacturadesglose.setFactura(respuesta[1])
            efacturadesglose.setTipo(respuesta[2])
            efacturadesglose.setServicio(respuesta[3])
            efacturadesglose.setInventario(respuesta[4])
            efacturadesglose.setCantidad(respuesta[5])
            efacturadesglose.setPrecio(respuesta[6])
            efacturadesglose.setPrecioTotal(respuesta[7])
        
        return efacturadesglose

    
    def guardarDatosFacturaDesglose(self, facturadesglose:eFacturaDesglose):
        consulta = "INSERT INTO facturadesglose (factura, tipo, servicio, inventario, cantidad, precio, preciototal) VALUES (?, ?, ?, ?, ?, ?, ?)"
        datos = list()
        datos.append(facturadesglose.getFactura())
        datos.append(facturadesglose.getTipo())
        datos.append(facturadesglose.getServicio())
        datos.append(facturadesglose.getInventario())
        datos.append(facturadesglose.getCantidad())
        datos.append(facturadesglose.getPrecio())
        datos.append(facturadesglose.getPrecioTotal())
        
        self.data.guardarEditar(consulta, datos)

    def editarDatosFacturaDesglose(self, facturadesglose:eFacturaDesglose):
        consulta = "UPDATE facturadesglose SET factura = ?, tipo = ?, servicio = ?, inventario = ?, cantidad = ?, precio = ?, preciototal = ? WHERE idfacdesglose = ?"
        datos = list()
        datos.append(facturadesglose.getFactura())
        datos.append(facturadesglose.getTipo())
        datos.append(facturadesglose.getServicio())
        datos.append(facturadesglose.getInventario())
        datos.append(facturadesglose.getCantidad())
        datos.append(facturadesglose.getPrecio())
        datos.append(facturadesglose.getPrecioTotal())
        datos.append(facturadesglose.getIdFacturaDesglose())
        
        self.data.guardarEditar(consulta, datos)

    def eliminarDatosFacturaDesglose(self, idfacdesglose):
        datos = list()
        datos.append(idfacdesglose)
        consulta = 'DELETE FROM facturadesglose WHERE idfacdesglose = ?'
        self.data.guardarEditar(consulta, datos)