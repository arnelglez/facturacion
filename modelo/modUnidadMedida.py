from entidades.entUnidadMedida import eUnidadMedida
from funciones.tallerDB import BaseTaller


class mUnidadMedida:
    
    def __init__(self):
        self.data = BaseTaller()
    
    def cargarDatosUnidadMedida(self):
        listaUM = list()
        consulta = "SELECT * FROM unidadmedida"
        respuestas =  self.data.consultaAll(consulta)
        if len(respuestas) > 0:
            for um in respuestas:
                umedida = eUnidadMedida()
                umedida.setIdUnidadMedida(um[0])
                umedida.setDescripcion(um[1])
                umedida.setSigla(um[2])
                umedida.setActivo(um[3])

                listaUM.append(umedida)
                
        return listaUM
   
    def obtenerUnaUnidadMedidaEspecifica(self, unidadmedida):
        dato = list()
        dato.append(unidadmedida)
        dato.append(unidadmedida)

        consulta = "SELECT * FROM unidadmedida WHERE idunidadmedida = ? or descripcion = ?"

        respuesta = self.data.consultaParametros(consulta, dato)
        umedida = eUnidadMedida()
        if respuesta:
            umedida.setIdUnidadMedida(respuesta[0])
            umedida.setDescripcion(respuesta[1])
            umedida.setSigla(respuesta[2])
            umedida.setActivo(respuesta[3])
        
        return umedida
       
    def guardarDatosUnidadMedida(self, umedida:eUnidadMedida):
        lista = list()
        lista.append(umedida.getDescripcion())
        lista.append(umedida.getSigla())
        lista.append(umedida.getActivo())
        consulta = "INSERT INTO unidadmedida (descripcion, sigla, activo) VALUES ( ?, ?, ? )"

        self.data.guardarEditar(consulta, lista)

    def editarDatosUnidadMedida(self, umedida:eUnidadMedida, modo):
        lista = list()
        consulta = "UPDATE unidadmedida SET descripcion = ?, sigla = ?, activo = ? WHERE idunidadmedida = ?"
        lista.append(umedida.getDescripcion())
        lista.append(umedida.getSigla())
        lista.append(modo)
        lista.append(umedida.getIdUnidadMedida())

        self.data.guardarEditar(consulta, lista)