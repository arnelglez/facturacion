class eMarca:

    def __init__(self):
        self.__idmarca = ""
        self.__descripcion = ""
        self.__equipo = ""

    def setIdMarca(self, idmarca):
        self.__idmarca = idmarca

    def setDescripcion(self, descripcion):
        self.__descripcion = descripcion

    def setEquipo(self, equipo):
        self.__equipo = equipo


    def getIdMarca(self):
        return self.__idmarca

    def getDescripcion(self):
        return self.__descripcion

    def getEquipo(self):
        return self.__equipo