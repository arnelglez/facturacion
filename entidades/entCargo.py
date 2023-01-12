class eCargo:
    
    def __init__(self):
        self.__idcargo = ""
        self.__descripcion = ""

    def setIdCargo(self, idcargo):
        self.__idcargo = idcargo

    def setDescripcion(self, descripcion):
        self.__descripcion = descripcion

 
    def getIdCargo(self):
        return self.__idcargo
        
    def getDescripcion(self):
        return self.__descripcion

   