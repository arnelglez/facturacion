class eServicio:
    
    def __init__(self):
        self.__idservicio = ""
        self.__descripcion = ""
        self.__precio = ""
        self.__unidadmedida = ""
        self.__equipo = ""
        self.__activo = ""

    def setIdServicio(self, idservicio):
        self.__idservicio = idservicio

    def setDescripcion(self, descripcion):
        self.__descripcion = descripcion

    def setPrecio(self, precio):
        self.__precio = precio

    def setUnidadMedida(self, unidadmedida):
        self.__unidadmedida = unidadmedida

    def setEquipo(self, equipo):
        self.__equipo = equipo

    def setActivo(self, activo):
        self.__activo = activo


    def getIdServicio(self):
        return self.__idservicio
        
    def getDescripcion(self):
        return self.__descripcion

    def getPrecio(self):
        return self.__precio

    def getUnidadMedida(self):
        return self.__unidadmedida

    def getEquipo(self):
        return self.__equipo

    def getActivo(self):
        return self.__activo

