from re import M


class eEquipo:
    
    def __init__(self):
        self.__idequipo = ""
        self.__descripcion = ""
        self.__activo = ""
        self.__multiple = ""

    def setIdEquipo(self, idequipo):
        self.__idequipo = idequipo

    def setDescripcion(self, descripcion):
        self.__descripcion = descripcion

    def setActivo(self, activo):
        self.__activo = activo

    def setMultiple(self, multiple):
        self.__multiple = multiple

 
    def getIdEquipo(self):
        return self.__idequipo
        
    def getDescripcion(self):
        return self.__descripcion

    def getActivo(self):
        return self.__activo

    def getMultiple(self):
        return self.__multiple

   