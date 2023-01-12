
class eModelo:
    
    def __init__(self):
        self.__idmodelo =  ""
        self.__descripcion = ""
        self.__marca = ""
        self.__equipo = ""

    def setIdModelo(self, idmodelo):
        self.__idmodelo = idmodelo

    def setDescripcion(self, descripcion):
        self.__descripcion = descripcion

    def setMarca(self, marca):
        self.__marca = marca

    def setEquipo(self, equipo):
        self.__equipo = equipo


    def getIdModelo(self):
        return self.__idmodelo

    def getDescripcion(self):
        return self.__descripcion

    def getMarca(self):
        return self.__marca

    def getEquipo(self):
        return self.__equipo
    