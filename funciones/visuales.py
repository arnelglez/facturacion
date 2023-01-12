
from PyQt6.QtCore import QBuffer, QByteArray, QIODevice
from PyQt6.QtWidgets import QTableWidgetItem

class Tablas:

    # funcion para ponerle la cabecera a las tablas            
    def headerClientes(self , posicion, tabla):
        titulo = (        
        ( 0 , "Id"),
        ( 1 , "Nombre"),
        ( 2 , "Contrato"),
        ( 3 , "Direccion"),
        ( 4 , "Cuenta"),
        ( 5 , "Activo")
        )
        
        tabla.setHorizontalHeaderItem(posicion,QTableWidgetItem(titulo[posicion][1]))

    def headerUM(self , posicion, tabla):
        titulo = (        
        ( 0 , "Id"),
        ( 1 , "Descripción"),
        ( 2 , "Sigla"),
        ( 3 , "Activo")
        )
        
        tabla.setHorizontalHeaderItem(posicion,QTableWidgetItem(titulo[posicion][1]))

    def headerEquipos(self , posicion, tabla):
        titulo = (        
        ( 0 , "Id"),
        ( 1 , "Descripción"),
        ( 2 , "Descripción"),
        ( 3 , "Activo")
        )
        
        tabla.setHorizontalHeaderItem(posicion,QTableWidgetItem(titulo[posicion][1]))

    def headerDosColumnas(self , posicion, tabla):
        titulo = (        
        ( 0 , "Id"),
        ( 1 , "Descripción"),
        ( 2 , "Activo")
        )
        
        tabla.setHorizontalHeaderItem(posicion,QTableWidgetItem(titulo[posicion][1]))

    def headerServicio(self , posicion, tabla):
        titulo = (        
        ( 0 , "Id"),
        ( 1 , "Descripcion"),
        ( 2 , "UM"),
        ( 3 , "Precio"),
        ( 4 , "Activo"),
        ( 5 , "Desc Real"),
        ( 6 , "tipo Equipo"),
        ( 7 , "idUM")
        )
        
        tabla.setHorizontalHeaderItem(posicion,QTableWidgetItem(titulo[posicion][1]))

        
    def headerFichaClientes(self , posicion, tabla):
        titulo = (        
        ( 0 , "Id"),
        ( 1 , "Nombre y Apellidos"),
        ( 2 , "Carnet"),
        ( 3 , "Cargo"),
        ( 4 , "Cliente"),
        ( 5 , "Nombre"),
        ( 6 , "Apellidos"),
        ( 7 , "Activo"),
        )
        
        tabla.setHorizontalHeaderItem(posicion,QTableWidgetItem(titulo[posicion][1]))     
        
    def headerBuscarCliente(self , posicion, tabla):
        titulo = (        
        ( 0 , "Id Cliente"),
        ( 1 , "Nombre del Cliente"),
        )
        
        tabla.setHorizontalHeaderItem(posicion,QTableWidgetItem(titulo[posicion][1]))

    def headerBuscarInventario(self , posicion, tabla):
        titulo = (        
        ( 0 , "idinventario"),
        ( 1 , "No. Inventario"),
        ( 2 , "Equipo"),
        )
        
        tabla.setHorizontalHeaderItem(posicion,QTableWidgetItem(titulo[posicion][1]))

    def headerBuscarFactura(self , posicion, tabla):
        titulo = (        
        ( 0 , "idfactura"),
        ( 1 , "No. Factura"),
        ( 2 , "Importe"),
        )
        
        tabla.setHorizontalHeaderItem(posicion,QTableWidgetItem(titulo[posicion][1]))

    def headerRecepcion(self , posicion, tabla):
        titulo = (        
        ( 0 , "idinventario"),
        ( 1 , "No Inventario"),
        ( 2 , "Equipo"),
        ( 3 , "Marca"),
        ( 4 , "Modelo"),
        ( 5 , "Ctdad"),
        ( 6 , "Observaciones")
        )
        
        tabla.setHorizontalHeaderItem(posicion,QTableWidgetItem(titulo[posicion][1]))

    def headerListaRecepciones(self , posicion, tabla):
        titulo = (        
        ( 0 , "idrecepcion"),
        ( 1 , "estado"),
        ( 2 , "No Recepción"),
        ( 3 , "Cliente"),
        ( 4 , "Fecha"),
        ( 5 , "Usuario"),
        )
        
        tabla.setHorizontalHeaderItem(posicion,QTableWidgetItem(titulo[posicion][1]))

    def headerFactura(self , posicion, tabla):
        titulo = (        
        ( 0 , "idfacturadesglose"),
        ( 1 , "Tipo"),
        ( 2 , "Servicio"),
        ( 3 , "Equipo"),
        ( 4 , "UM"),
        ( 5 , "Cantidad"),
        ( 6 , "Precio"),
        ( 7 , "Importe"),
        ( 8 , "idservicio"),
        ( 9 , "idequipo"),
        ( 10 , "cantidad")
        )
        
        tabla.setHorizontalHeaderItem(posicion,QTableWidgetItem(titulo[posicion][1]))

    def headerListaFacturas(self , posicion, tabla):
        titulo = (        
        ( 0 , "idfactura"),
        ( 1 , "estado"),
        ( 2 , "No Factura"),
        ( 3 , "Cliente"),
        ( 4 , "Importe"),
        ( 5 , "Fecha"),
        ( 6 , "Usuario"),
        )
        
        tabla.setHorizontalHeaderItem(posicion,QTableWidgetItem(titulo[posicion][1]))
        
    def headerCobro(self , posicion, tabla):
        titulo = (        
        ( 0 , "idcobrofactura"),
        ( 1 , "Tipo de Pago"),
        ( 2 , "Factura"),
        ( 3 , "Importe"),
        ( 4 , "idfactura")
        )
        
        tabla.setHorizontalHeaderItem(posicion,QTableWidgetItem(titulo[posicion][1]))
    

    def headerListaCobros(self , posicion, tabla):
        titulo = (        
        ( 0 , "idcobro"),
        ( 1 , "estado"),
        ( 2 , "No Cobro"),
        ( 3 , "Cliente"),
        ( 4 , "Importe"),
        ( 5 , "Fecha"),
        ( 6 , "Usuario"),
        )

        tabla.setHorizontalHeaderItem(posicion,QTableWidgetItem(titulo[posicion][1]))

    def headerListaUsuario(self, posicion, tabla):
        titulo = (        
        ( 0 , "idusuario"),
        ( 1 , "usuario"),
        ( 2 , "Nombre y apellidos"),
        ( 3 , "Carnet Identidad"),
        ( 4 , "Activo")
        )

        tabla.setHorizontalHeaderItem(posicion,QTableWidgetItem(titulo[posicion][1]))

    def headerAnticipos(self, posicion, tabla):
        titulo = (        
        ( 0 , "idusuario"),
        ( 1 , "Cliente"),
        ( 2 , "Fecha"),
        ( 3 , "Importe"),
        ( 4 , "idCliente")
        )

        tabla.setHorizontalHeaderItem(posicion,QTableWidgetItem(titulo[posicion][1]))

    def headerListaAnticipos(self , posicion, tabla):
        titulo = (        
        ( 0 , "idAnticipo"),
        ( 1 , "estado"),
        ( 2 , "No Documento"),
        ( 3 , "Cliente"),
        ( 4 , "Importe"),
        ( 5 , "Fecha"),
        ( 6 , "Usuario"),
        )
        
        tabla.setHorizontalHeaderItem(posicion,QTableWidgetItem(titulo[posicion][1]))