from entidades.entCargo import eCargo
from funciones.tallerDB import BaseTaller

class mCargo:
    
    def __init__(self):
        self.data = BaseTaller()
    
    def cargarDatosCargo(self):
        listaCargos = list()
        consulta = "SELECT * FROM cargo"
        respuestas =  self.data.consultaAll(consulta)
        if len(respuestas) > 0:
            for resp in respuestas:
                cargo = eCargo()
                cargo.setIdCargo(resp[0])
                cargo.setDescripcion(resp[1])

                listaCargos.append(cargo)

        return listaCargos
   
    def obtenerCargoEspecifico(self, cargo):
        consulta = "SELECT * FROM cargo WHERE idcargo = ? or descripcion = ?"

        datos = list()
        datos.append(cargo)
        datos.append(cargo)

        respuesta = self.data.consultaParametros(consulta, datos)
        ecargo = eCargo()
        if respuesta:
            ecargo.setIdCargo(respuesta[0])
            ecargo.setDescripcion(respuesta[1])
        
        return ecargo

    
    def guardarDatosCargo(self,cargo:eCargo):
        consulta = "INSERT INTO cargo (descripcion) VALUES (?)"
        lista = list()
        lista.append(cargo.getDescripcion())
        self.data.guardarEditar(consulta, lista)
   