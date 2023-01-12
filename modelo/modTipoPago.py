from entidades.entTipoPago import eTipoPago
from funciones.tallerDB import BaseTaller

class mTipoPago:
    
    def __init__(self):
        self.data = BaseTaller()
        

    def cargarDatosTipoPago(self):
        listaTipoPago = list()
        consulta = "SELECT * FROM tipopago"
        respuestas =  self.data.consultaAll(consulta)
        if len(respuestas) > 0:
            for respuesta in respuestas:
                etipo = eTipoPago()
                etipo.setIdTipoPago(respuesta[0])
                etipo.setDescripcion(respuesta[1])
                etipo.setActivo(respuesta[2])

                listaTipoPago.append(etipo)
        
        return listaTipoPago
   
    def obtenerTipoPagoEspecifico(self, tipopago):
        dato = list()
        dato.append(tipopago)
        dato.append(tipopago)
        consulta = "SELECT * FROM tipopago WHERE idtipopago = ? or  descripcion = ?"
    
        respuesta = self.data.consultaParametros(consulta, dato)
        etipo = eTipoPago()
        if respuesta:
            etipo.setIdTipoPago(respuesta[0])
            etipo.setDescripcion(respuesta[1])
            etipo.setActivo(respuesta[2])
        
        return etipo
    
    def guardarDatosTipoPago(self, etipopago:eTipoPago):
        lista = list()
        lista.append(etipopago.getDescripcion())
        lista.append(etipopago.getActivo())
        consulta = "INSERT INTO tipopago (descripcion, activo) VALUES ( ?, ? )"

        self.data.guardarEditar(consulta, lista)

    def editarDatosTipoPago(self, etipopago:eTipoPago, modo):
        lista = list()
        consulta = "UPDATE tipopago SET descripcion = ?, activo = ? WHERE idtipopago = ?"
        lista.append(etipopago.getDescripcion())
        lista.append(modo)
        lista.append(etipopago.getIdTipoPago())

        self.data.guardarEditar(consulta, lista)