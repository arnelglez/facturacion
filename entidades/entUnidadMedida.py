class eUnidadMedida:
    
    def __init__(self):
        self.__idunidadmedida = ""
        self.__descripcion = ""
        self.__sigla = ""
        self.__activo = ""

    def setIdUnidadMedida(self, idunidadmedida):
        self.__idunidadmedida = idunidadmedida

    def setDescripcion(self, descripcion):
        self.__descripcion = descripcion

    def setSigla(self, sigla):
        self.__sigla = sigla

    def setActivo(self, activo):
        self.__activo = activo

 
    def getIdUnidadMedida(self):
        return self.__idunidadmedida
        
    def getDescripcion(self):
        return self.__descripcion
        
    def getSigla(self):
        return self.__sigla

    def getActivo(self):
        return self.__activo

   