from entidades.entUsuario import eUsuario
from funciones.generales import Criptografia
from funciones.tallerDB import BaseTaller

class mUsuario:
    def __init__(self):
        self.data = BaseTaller()
        self.cripto = Criptografia()

    
    def cargarDatosUsuario(self):
        listaUsuario = list()
        consulta = "SELECT * FROM usuario"
        respuestas =  self.data.consultaAll(consulta)
        if len(respuestas) > 0:
            for respuesta in respuestas:
                eusuario = eUsuario()
                eusuario.setIdUsuario(respuesta[0])
                eusuario.setUsername(respuesta[1])
                passwd = self.cripto.decrypt(respuesta[2])
                eusuario.setPasswd(passwd)
                eusuario.setCarnet(respuesta[3])
                eusuario.setNombre(respuesta[4])
                eusuario.setApellidos(respuesta[5])
                eusuario.setActivo(respuesta[6])

                listaUsuario.append(eusuario)
                
        return listaUsuario

    def verificarUsuario(self, user, password):
        usuario = eUsuario()
        consulta = "SELECT * FROM usuario WHERE username = ? AND activo = ?"
        lista = list()
        lista.append(user)
        lista.append(1)
        respuesta = self.data.consultaParametros(consulta, lista)
        if respuesta:
            passwd = self.cripto.decrypt(respuesta[2])
            if password == passwd:
                usuario.setIdUsuario(respuesta[0])
                usuario.setUsername(respuesta[1])
                usuario.setPasswd(passwd)
                usuario.setCarnet(respuesta[3])
                usuario.setNombre(respuesta[4])
                usuario.setApellidos(respuesta[5])
                usuario.setActivo(respuesta[6])
        
        return usuario


   
    def obtenerUsuarioEspecifico(self, idusuario):
        datos = list()
        datos.append(idusuario)
        consulta = "SELECT * FROM usuario WHERE idusuario = ?"
        respuesta = self.data.consultaParametros(consulta, datos)
        eusuario = eUsuario()
        if respuesta:
            eusuario.setIdUsuario(respuesta[0])
            eusuario.setUsername(respuesta[1])
            passwd = self.cripto.decrypt(respuesta[2])
            eusuario.setPasswd(passwd)
            eusuario.setCarnet(respuesta[3])
            eusuario.setNombre(respuesta[4])
            eusuario.setApellidos(respuesta[5])
            eusuario.setActivo(respuesta[6])
        
        return eusuario

    
    def guardarDatosUsuario(self, usuario:eUsuario):
        consulta = "INSERT INTO usuario (username, passwd, carnet, nombre, apellidos, activo) VALUES (?, ?, ?, ?, ?, ?)"
        passwd = self.cripto.crypt(usuario.getPasswd())
        datos = list()
        datos.append(usuario.getUsername())
        datos.append(passwd)
        datos.append(usuario.getCarnet())
        datos.append(usuario.getNombre())
        datos.append(usuario.getApellidos())
        datos.append(usuario.getActivo())
        self.data.guardarEditar(consulta, datos)

    def editarDatosUsuario(self, usuario:eUsuario, modo):
        consulta = "UPDATE usuario SET username = ?, passwd = ?, carnet = ?, nombre = ?, apellidos = ?, activo = ? WHERE idusuario = ?"
        passwd = self.cripto.crypt(usuario.getPasswd())
        datos = list()
        datos.append(usuario.getUsername())
        datos.append(passwd)
        datos.append(usuario.getCarnet())
        datos.append(usuario.getNombre())
        datos.append(usuario.getApellidos())
        datos.append(modo)
        datos.append(usuario.getIdUsuario())
        self.data.guardarEditar(consulta, datos)