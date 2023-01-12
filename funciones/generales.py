
from entidades.entDuenno import eDuenno
from entidades.entTaller import eTaller
from sqlite3.dbapi2 import Date
import sys
import os
import datetime

from time import time

from PyQt6 import QtGui, QtWidgets
from PyQt6.QtCore import QSizeF
from PyQt6.QtPrintSupport import QPrintPreviewDialog, QPrinter
from modelo.modUnidadMedida import mUnidadMedida
from modelo.modEquipo import mEquipo
from cryptography.fernet import Fernet
from modelo.modFecha import mFecha, eFecha 
from unidecode import unidecode

class FuncionesGenerales:
    def __init__(self):
        self.cripto = Criptografia()

    def resource_path(self, relative_path):
        relative = relative_path[3:]
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative)



    def mensageInformacion(self, tipo, titulo, sMensaje):

        msg = QtWidgets.QMessageBox()
        if tipo == 'informacion':
            msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        elif tipo == 'error':
            msg.setIcon(QtWidgets.QMessageBox.Icon.Critical)
        msg.setText(sMensaje)
        msg.setWindowTitle(titulo)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.resource_path("../img/Ok.ico")), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        aceptar = msg.addButton('Aceptar', QtWidgets.QMessageBox.ButtonRole.AcceptRole)
        aceptar.setIcon(icon)
        # Ejecuta el MessageBox
        msg.exec()

    def mensageSiNo(self, titulo, sMensaje, sInformacion):

        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        msg.setText(sMensaje)
        msg.setInformativeText(sInformacion)
        msg.setWindowTitle(titulo)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.resource_path("../img/Si.ico")), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(self.resource_path("../img/No.ico")), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
       
        no = msg.addButton('  No', QtWidgets.QMessageBox.ButtonRole.NoRole)              
        no.setIcon(icon1)
        si = msg.addButton('  Si', QtWidgets.QMessageBox.ButtonRole.AcceptRole)
        si.setIcon(icon)
        
        msg.setDefaultButton(no)
        # Ejecuta el MessageBox
        return msg.exec()


    def cerrarVentana(self, ventana):
        ventana.hide()

    def cerrarAplicacion(self, widget):
        widget.QApplication.quit()

    def insertarFila(self, tabla): 
        rowCount = tabla.rowCount()
        tabla.insertRow(rowCount)
        return rowCount
        
    def eliminarFila(self, tabla):
        currentRow = tabla.currentRow()
        if tabla.rowCount() > 0:
            tabla.removeRow(currentRow)

    def optenerUnidadMedidad(self , unidadmedida):
        umedida = mUnidadMedida()

        medida = umedida.obtenerUnaUnidadMedidaEspecifica(unidadmedida)

        return medida

    def numeroDocumento(self, documento):
        fecha = self.fechaDocumentos()
        annofecha = fecha[-4:]
        annodoc = documento[-4:]
        numero = documento[0:-5]
        
        if documento == "" or int(annofecha) > int(annodoc):
            result = '1-'+annofecha
        else:
            actual = int(numero) + 1
            result = str(actual) + '-' +annofecha
        
        return result
            

    def fechaDocumentos(self):
        mfecha = mFecha().cargarValorFecha()
        
        ahora = mfecha.getFechaProcesamiento()

        fecha = '{}/{}/{}'.format(ahora[0:2], ahora[3:5], ahora[6:10])

        return str(fecha)

    def comboTextoAnterior(self, combo, texto):
        pos = combo.findText(texto)
        combo.setCurrentIndex(pos)

    def floatToStr(self, numero:float):
        cadena = str(numero)
        if cadena != '0':
            if cadena[-3] == '.': 
                return cadena
            elif cadena[-2] == '.':
                return cadena + '0'
            else:
                return cadena + '.00'
        else:
            return '0.00'

    def verificarLicencia(self, taller:eTaller, duenno:eDuenno, licencia):
        datos = unidecode(taller.getNombre()) + '\n' + unidecode(taller.getDireccion()) + '\n' + unidecode(duenno.getNombre())  + '\n' + unidecode(duenno.getApellidos())  + '\n' + duenno.getCarnet()
           
        lic = self.cripto.decryptLicencia(licencia)

        if datos == lic:
            return True
        else:
            return False

    def vistaPrevia(self, documento:QtGui.QTextDocument, nombre, parent, numero = ""):
        impresion = QPrinter(QPrinter.PrinterMode.HighResolution)

        vista = QPrintPreviewDialog(impresion, parent)
        vista.setWindowTitle(nombre) 
        cp = QtGui.QGuiApplication.primaryScreen().size()
        vista.resize(cp)
        vista.setMinimumSize(865, 600)
        vista.setMaximumSize(16777215, 16777215)
        

        myIcons = vista.findChildren(QtWidgets.QToolBar)
        myIcons[0].addAction(QtGui.QIcon(self.resource_path("../img/exportarPDF.png")), "Exportar a PDF", lambda:self.exportarPDF(documento, nombre, numero, parent))
        myIcons[0].addAction(QtGui.QIcon(self.resource_path("../img/Salir.png")), "Salir", lambda:self.cerrarVentana(vista))

        vista.paintRequested.connect(lambda:self.vistaPreviaImpresion(documento, impresion))
        vista.exec()

    def vistaPreviaImpresion(self, documento:QtGui.QTextDocument, impresion):
        documento.setPageSize(QSizeF(612, 792))
        documento.print(impresion)

    def exportarPDF(self, documento:QtGui.QTextDocument, nombre, numero, parent):
        if numero == "":
            nomb = nombre + '.pdf'
        else:
            nomb = nombre + '_' + numero + '.pdf'

        nombreArchivo, _ = QtWidgets.QFileDialog.getSaveFileName(parent, "Exportar a PDF", nomb,
                                                           "Archivos PDF (*.pdf);;All Files (*)")
        if nombreArchivo:
            impresion = QPrinter(QPrinter.PrinterMode.HighResolution)
            impresion.setOutputFileName(nombreArchivo)
            #impresion.setPageSize()
            #impresion.setPageMargins(25,25,25,25, QPrinter.Unit.Millimeter)
            documento.print(impresion)

    
class Criptografia:

    def __init__(self):
        self.__f = Fernet(b'k6kmmx2J1GacGIUnQRDNyod3wt04o131_1kAM1F7Zwk=')
        self.__licen = Fernet(b'a8kmmr5J0GncGIUeQRDLyod7wt02o114_9kAM0F5Zwk=')

    def crypt(self, cadena):
        passwd = self.__f.encrypt(cadena.encode())
        return passwd.decode()

    def decrypt(self, cadena):
        passwd = self.__f.decrypt(cadena.encode())
        return passwd.decode()

    def cryptLicencia(self, cadena):
        passwd = self.__licen.encrypt(cadena.encode())
        return passwd.decode()

    def decryptLicencia(self, cadena):
        passwd = self.__licen.decrypt(cadena.encode())
        return passwd.decode()

