from entidades.entFactura import eFactura
from funciones.tallerDB import BaseTaller


class mFactura:

    def __init__(self):
        self.data = BaseTaller()
        

    def cargarDatosFactura(self):
        listaFactura = list()
        consulta = "SELECT * FROM factura ORDER BY nofactura and fecha"
        respuestas =  self.data.consultaAll(consulta)
        if len(respuestas) > 0:
            for respuesta in respuestas:
                efactura = eFactura()
                efactura.setIdFactura(respuesta[0])
                efactura.setNoFactura(respuesta[1])
                efactura.setUsuario(respuesta[2])
                efactura.setCliente(respuesta[3])
                efactura.setFichaCliente(respuesta[4])
                efactura.setFecha(respuesta[5])
                efactura.setTotalFactura(respuesta[6])
                efactura.setEstado(respuesta[7])
                efactura.setNota(respuesta[8])
                efactura.setMoneda(respuesta[9])

                listaFactura.append(efactura)
        
        return listaFactura
    
    def cargarDatosFacturaConNumero(self):
        listaFactura = list()
        consulta = "SELECT * FROM factura WHERE nofactura <> 'S/N'"
        respuestas =  self.data.consultaAll(consulta)
        if len(respuestas) > 0:
            for respuesta in respuestas:
                efactura = eFactura()
                efactura.setIdFactura(respuesta[0])
                efactura.setNoFactura(respuesta[1])
                efactura.setUsuario(respuesta[2])
                efactura.setCliente(respuesta[3])
                efactura.setFichaCliente(respuesta[4])
                efactura.setFecha(respuesta[5])
                efactura.setTotalFactura(respuesta[6])
                efactura.setEstado(respuesta[7])
                efactura.setNota(respuesta[8])
                efactura.setMoneda(respuesta[9])

                listaFactura.append(efactura)
        
        return listaFactura
   
    def obtenerFacturaEspecifico(self, idfactura):
        datos = list()
        datos.append(idfactura)
        consulta = "SELECT * FROM factura WHERE idfactura = ?"
        respuesta = self.data.consultaParametros(consulta, datos)
        efactura = eFactura()
        if respuesta:
            efactura.setIdFactura(respuesta[0])
            efactura.setNoFactura(respuesta[1])
            efactura.setUsuario(respuesta[2])
            efactura.setCliente(respuesta[3])
            efactura.setFichaCliente(respuesta[4])
            efactura.setFecha(respuesta[5])
            efactura.setTotalFactura(respuesta[6])
            efactura.setEstado(respuesta[7])
            efactura.setNota(respuesta[8])
            efactura.setMoneda(respuesta[9])
        
        return efactura


    def busquedaFactura(self, factura, cliente):

        listaFactura = list()

        if factura == '':
            lista = self.cargarDatosFactura()
            for resp in lista:
                if resp.getCliente() == cliente:
                    listaFactura.append(resp)

        else:
            valor = '%'+factura+'%'
            consulta = "SELECT * FROM factura where (nofactura LIKE ? or totalfactura LIKE ?) and cliente = ?"
            datos = list()
            datos.append(valor)
            datos.append(valor)
            datos.append(cliente)

            respuestas =  self.data.consultaBusqueda(consulta, datos)
            if len(respuestas) > 0:
                for respuesta in  respuestas:
                    efactura = eFactura()
                    efactura.setIdFactura(respuesta[0])
                    efactura.setNoFactura(respuesta[1])
                    efactura.setUsuario(respuesta[2])
                    efactura.setCliente(respuesta[3])
                    efactura.setFichaCliente(respuesta[4])
                    efactura.setFecha(respuesta[5])
                    efactura.setTotalFactura(respuesta[6])
                    efactura.setEstado(respuesta[7])
                    efactura.setNota(respuesta[8])
                    efactura.setMoneda(respuesta[9])

                    listaFactura.append(efactura)
                    
        return listaFactura
    
    def guardarDatosFactura(self, factura:eFactura):
        consulta = "INSERT INTO factura (nofactura, usuario, cliente, fichacliente, fecha, totalfactura, estado, nota, moneda) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
        datos = list()
        datos.append(factura.getNoFactura())
        datos.append(factura.getUsuario())
        datos.append(factura.getCliente())
        datos.append(factura.getFichaCliente())
        datos.append(factura.getFecha())
        datos.append(factura.getTotalFactura())
        datos.append(factura.getEstado())
        datos.append(factura.getNota())
        datos.append(factura.getMoneda())
        self.data.guardarEditar(consulta, datos)

    def editarDatosFactura(self, factura:eFactura, modo):
        consulta = "UPDATE factura SET nofactura = ?, usuario = ?, cliente = ?, fichacliente = ?, fecha = ?, totalfactura = ?, estado = ?, nota = ?, moneda = ? WHERE idfactura = ?"
        datos = list()
        datos.append(factura.getNoFactura())
        datos.append(factura.getUsuario())
        datos.append(factura.getCliente())
        datos.append(factura.getFichaCliente())
        datos.append(factura.getFecha())
        datos.append(factura.getTotalFactura())
        datos.append(modo)
        datos.append(factura.getNota())
        datos.append(factura.getMoneda())
        datos.append(factura.getIdFactura())
        self.data.guardarEditar(consulta, datos)

    def eliminarFactura(self, idfactura):
        datos = list()
        datos.append(idfactura)
        consulta = 'DELETE FROM factura WHERE idfactura = ?'
        self.data.guardarEditar(consulta, datos)