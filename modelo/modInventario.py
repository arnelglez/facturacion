from entidades.entInventario import eInventario
from funciones.tallerDB import BaseTaller


class mInventario:

    def __init__(self):
        self.data = BaseTaller()
        

    def cargarDatosInventario(self):
        listaInventario = list()
        consulta = "SELECT * FROM inventario"
        respuestas =  self.data.consultaAll(consulta)
        if len(respuestas) > 0:
            for respuesta in respuestas:
                einventario = eInventario()
                einventario.setIdInventario(respuesta[0])
                einventario.setRecepcion(respuesta[1])
                einventario.setEquipo(respuesta[2])
                einventario.setMarca(respuesta[3])
                einventario.setModelo(respuesta[4])
                einventario.setNoInventario(respuesta[5])
                einventario.setObservaciones(respuesta[6])
                einventario.setActivo(respuesta[7])
                einventario.setCantidad(respuesta[8])

                listaInventario.append(einventario)
        
        return listaInventario

   
    def obtenerInventarioEspecifico(self, idinventario):
        datos = list()
        datos.append(idinventario)
        consulta = "SELECT * FROM inventario WHERE idinventario = ?"
        respuesta = self.data.consultaParametros(consulta, datos)
        einventario = eInventario()
        if respuesta:
            einventario.setIdInventario(respuesta[0])
            einventario.setRecepcion(respuesta[1])
            einventario.setEquipo(respuesta[2])
            einventario.setMarca(respuesta[3])
            einventario.setModelo(respuesta[4])
            einventario.setNoInventario(respuesta[5])
            einventario.setObservaciones(respuesta[6])
            einventario.setActivo(respuesta[7])
            einventario.setCantidad(respuesta[8])
        
        return einventario


    def busquedaInventarios(self, inventario):
        if inventario == '':
            respuesta = self.cargarDatosInventario()
            return respuesta
        else:
            valor = '%'+inventario+'%'
            consulta = "SELECT * FROM inventario where noinventario LIKE ? "
            datos = list()
            datos.append(valor)

            listaInventario = list()
            respuestas =  self.data.consultaBusqueda(consulta, datos)
            if len(respuestas) > 0:
                for respuesta in  respuestas:
                    einventario = eInventario()
                    einventario.setIdInventario(respuesta[0])
                    einventario.setRecepcion(respuesta[1])
                    einventario.setEquipo(respuesta[2])
                    einventario.setMarca(respuesta[3])
                    einventario.setModelo(respuesta[4])
                    einventario.setNoInventario(respuesta[5])
                    einventario.setObservaciones(respuesta[6])
                    einventario.setActivo(respuesta[7])
                    einventario.setCantidad(respuesta[8])

                    listaInventario.append(einventario)
                    
            return listaInventario



    def busquedaListaInventarios(self, equipo, marca, modelo ):
        datos = list()
        if equipo != '*':
            consultaEquipo = " equipo = ? and"
            datos.append(equipo)
        else:
            consultaEquipo = ''
            
        if marca != '*':
            consultaMarca = " marca = ? and"
            datos.append(marca)
        else:
            consultaMarca = ''
    
        if modelo != '*':
            consultaModelo = " modelo = ? and"
            datos.append(modelo)
        else:
            consultaModelo = ''
            
        
        consulta = "SELECT * FROM inventario where" + consultaEquipo + consultaMarca + consultaModelo + " activo <> 0"
        
            
        listaInventario = list()
        respuestas =  self.data.consultaBusqueda(consulta, datos)
        if len(respuestas) > 0:
            for respuesta in  respuestas:
                einventario = eInventario()
                einventario.setIdInventario(respuesta[0])
                einventario.setRecepcion(respuesta[1])
                einventario.setEquipo(respuesta[2])
                einventario.setMarca(respuesta[3])
                einventario.setModelo(respuesta[4])
                einventario.setNoInventario(respuesta[5])
                einventario.setObservaciones(respuesta[6])
                einventario.setActivo(respuesta[7])
                einventario.setCantidad(respuesta[8])

                listaInventario.append(einventario)
                    
            return listaInventario
    
    def guardarDatosInventario(self, inventario:eInventario):
        consulta = "INSERT INTO inventario (recepcion, equipo, marca, modelo, noinventario, observaciones, activo, cantidad) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        datos = list()
        datos.append(inventario.getRecepcion())
        datos.append(inventario.getEquipo())
        datos.append(inventario.getMarca())
        datos.append(inventario.getModelo())
        datos.append(inventario.getNoInventario())
        datos.append(inventario.getObservaciones())
        datos.append(inventario.getActivo())
        datos.append(inventario.getCantidad())
        
        self.data.guardarEditar(consulta, datos)

    def editarDatosInventario(self, inventario:eInventario, modo):
        consulta = "UPDATE inventario SET recepcion = ?, equipo = ?, marca = ?, modelo = ?, noinventario = ?, observaciones = ?, activo = ?, cantidad = ? WHERE idinventario = ?"
        datos = list()
        datos.append(inventario.getRecepcion())
        datos.append(inventario.getEquipo())
        datos.append(inventario.getMarca())
        datos.append(inventario.getModelo())
        datos.append(inventario.getNoInventario())
        datos.append(inventario.getObservaciones())
        datos.append(modo)
        datos.append(inventario.getCantidad())
        datos.append(inventario.getIdInventario())
        self.data.guardarEditar(consulta, datos)

    def eliminarDatosInventario(self, idinventario):
        datos = list()
        datos.append(idinventario)
        consulta = 'DELETE FROM inventario WHERE idinventario = ?'
        self.data.guardarEditar(consulta, datos)
