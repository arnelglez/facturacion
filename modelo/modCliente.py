from entidades.entCliente import eCliente
from funciones.tallerDB import BaseTaller

class mCliente:

    def __init__(self):
        self.data = BaseTaller()

    def cargarDatosClientes(self):
        listaCliente = list()
        consulta = "SELECT * FROM cliente"
        respuestas =  self.data.consultaAll(consulta)
        if len(respuestas) > 0:
            for respuesta in  respuestas:
                eclient = eCliente()
                eclient.setIdCliente(respuesta[0])
                eclient.setNombre(respuesta[1])
                eclient.setContrato(respuesta[2])
                eclient.setDireccion(respuesta[3])
                eclient.setCuenta(respuesta[4])
                eclient.setActivo(respuesta[5])

                listaCliente.append(eclient)
                
        return listaCliente

    def obtenerDatosClientesEspecifica(self, cliente):
        consulta = "SELECT * FROM cliente WHERE idcliente = ? or nombre = ?"
        datos = list()
        datos.append(cliente)
        datos.append(cliente)

        respuesta = self.data.consultaParametros(consulta,datos)
        eclient = eCliente()
        if respuesta:
            eclient.setIdCliente(respuesta[0])
            eclient.setNombre(respuesta[1])
            eclient.setContrato(respuesta[2])
            eclient.setDireccion(respuesta[3])
            eclient.setCuenta(respuesta[4])
            eclient.setActivo(respuesta[5])
        
        return eclient

    def busquedaClientes(self, cliente):
        if cliente == '':
            respuesta = self.cargarDatosClientes()
            return respuesta
        else:
            valor = '%'+cliente+'%'
            consulta = "SELECT * FROM cliente where idcliente LIKE ? or nombre LIKE ?"
            datos = list()
            datos.append(valor)
            datos.append(valor)

            listaCliente = list()
            respuestas =  self.data.consultaBusqueda(consulta, datos)
            if len(respuestas) > 0:
                for respuesta in  respuestas:
                    eclient = eCliente()
                    eclient.setIdCliente(respuesta[0])
                    eclient.setNombre(respuesta[1])
                    eclient.setContrato(respuesta[2])
                    eclient.setDireccion(respuesta[3])
                    eclient.setCuenta(respuesta[4])
                    eclient.setActivo(respuesta[5])

                    listaCliente.append(eclient)
                    
            return listaCliente
    
    def guardarDatosCliente(self, cliente:eCliente):
        consulta = "INSERT INTO cliente (nombre, contrato, direccion, cuenta, activo) VALUES (?, ?, ?, ?, ?)"
        datos = list()
        datos.append(cliente.getNombre())
        datos.append(cliente.getContrato())
        datos.append(cliente.getDireccion())
        datos.append(cliente.getCuenta())
        datos.append(1)
        self.data.guardarEditar(consulta, datos)

    def editarDatosCliente(self, cliente:eCliente, modo):
        consulta = "UPDATE cliente SET nombre = ?, contrato = ?, direccion = ?, cuenta = ?, activo = ? WHERE idcliente = ?"
        datos = list()
        datos.append(cliente.getNombre())
        datos.append(cliente.getContrato())
        datos.append(cliente.getDireccion())
        datos.append(cliente.getCuenta())
        datos.append(modo)
        datos.append(cliente.getIdCliente())
        self.data.guardarEditar(consulta, datos)
