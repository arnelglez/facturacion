class eFecha:
    
    def __init__(self):
        self.__idfecha = ""
        self.__fechaprocesamiento = ""
        
    
    def setIdFecha(self, idfecha):
        self.__idfecha = idfecha

    def setFechaProcesamiento(self, fechaprocesamiento):
        self.__fechaprocesamiento = fechaprocesamiento


    def getIdFecha(self):
        return self.__idfecha
        
    def getFechaProcesamiento(self):
        return self.__fechaprocesamiento
        