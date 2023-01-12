from entidades.entFichaCliente import eFichaCliente
from funciones.tallerDB import BaseTaller

class mFichaCliente:
    
    def __init__(self):
        self.data = BaseTaller()
        

    def cargarDatosFichaCliente(self):
        listaFichaCliente = list()
        consulta = "SELECT * FROM fichacliente"
        respuestas =  self.data.consultaAll(consulta)
        if len(respuestas) > 0:
            for respuesta in respuestas:
                efcliente = eFichaCliente()
                efcliente.setIdFichaCliente(respuesta[0])
                efcliente.setNombre(respuesta[1])
                efcliente.setApellidos(respuesta[2])
                efcliente.setCarnet(respuesta[3])
                efcliente.setCargo(respuesta[4])
                efcliente.setCliente(respuesta[5])
                efcliente.setActivo(respuesta[6])

                listaFichaCliente.append(efcliente)
        
        return listaFichaCliente
   
    def obtenerFichaClienteEspecifico(self, idfichacliente):
        datos = list()
        datos.append(idfichacliente)
        consulta = "SELECT * FROM fichacliente WHERE idfichacliente = ?"
        respuesta = self.data.consultaParametros(consulta, datos)
        efcliente = eFichaCliente()
        if respuesta:
            efcliente.setIdFichaCliente(respuesta[0])
            efcliente.setNombre(respuesta[1])
            efcliente.setApellidos(respuesta[2])
            efcliente.setCarnet(respuesta[3])
            efcliente.setCargo(respuesta[4])
            efcliente.setCliente(respuesta[5])
            efcliente.setActivo(respuesta[6])
            
        return efcliente

    def guardarDatosFichaCliente(self,fichacliente:eFichaCliente):
        listaFicha = list()

        consulta = "INSERT INTO fichacliente (nombre, apellidos, carnet, cargo, cliente, activo) VALUES (? , ? , ? , ? , ? , ?)"
        
        listaFicha.append(fichacliente.getNombre())
        listaFicha.append(fichacliente.getApellidos())
        listaFicha.append(fichacliente.getCarnet())
        listaFicha.append(fichacliente.getCargo())
        listaFicha.append(fichacliente.getCliente())
        listaFicha.append(fichacliente.getActivo())

        self.data.guardarEditar(consulta, listaFicha)

    def editarDatosFichaCliente(self,fichacliente:eFichaCliente, modo):
        listaFicha = list()

        consulta = "UPDATE fichacliente SET nombre = ?, apellidos = ?, carnet = ?, cargo = ?, cliente = ?, activo = ? WHERE idfichacliente = ?"
        
        listaFicha.append(fichacliente.getNombre())
        listaFicha.append(fichacliente.getApellidos())
        listaFicha.append(fichacliente.getCarnet())
        listaFicha.append(fichacliente.getCargo())
        listaFicha.append(fichacliente.getCliente())
        listaFicha.append(modo)
        listaFicha.append(fichacliente.getIdFichaCliente())
        
        self.data.guardarEditar(consulta, listaFicha)
   