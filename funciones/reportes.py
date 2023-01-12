
import base64

from modelo.modTipoPago import mTipoPago
from entidades.entRecepcion import eRecepcion
from modelo.modEquipo import mEquipo
from modelo.modUnidadMedida import mUnidadMedida
from entidades.entFacturaDesglose import eFacturaDesglose
from PyQt6.QtGui import QTextDocument
from modelo.modDuenno import mDuenno
from modelo.modTaller import mTaller
from modelo.modCliente import mCliente
from modelo.modFichaCliente import mFichaCliente
from modelo.modCargo import mCargo
from modelo.modFacturaDesglose import mFacturaDesglose
from modelo.modUsuario import mUsuario, eUsuario
from modelo.modFactura import mFactura, eFactura
from modelo.modInventario import mInventario, eInventario
from modelo.modRecepcion import mRecepcion, eRecepcion
from modelo.modCobro import mCobro, eCobro
from modelo.modCobroFactura import mCobroFactura, eCobroFactura
from modelo.modAnticipo import mAnticipo, eAnticipo
from modelo.modMarca import mMarca
from modelo.modModelo import mModelo
from modelo.modServicio import mServicio
from funciones.generales import FuncionesGenerales

from jinja2.environment import Environment
from jinja2.loaders import FileSystemLoader


class Reporte:

    def __init__(self):

        self.generales = FuncionesGenerales()
        self.env = Environment(loader=FileSystemLoader(self.generales.resource_path("../reportes")))
        self.eduenno = mDuenno().cargarDatosDuenno()
        self.etaller = mTaller().cargarValorTaller()

    
    def obtenerEquipo(self, idequipo):
        equipo = mEquipo().obtenerEquipoEspecifico(idequipo)
        return equipo.getDescripcion()

    def obtenerModelo(self, idmodelo):
        modelo = mModelo().obtenerModeloEspecifico(idmodelo)
        return modelo.getDescripcion()

    def obtenerMarca(self, idmarca):
        marca = mMarca().obtenerMarcaEspecifico(idmarca)
        return marca.getDescripcion()

    
    def facturaDesglosada(self, efactura:eFactura, usuario:eUsuario, parent):
        salto = ''
        if int(efactura.getMoneda()) == 0:
            cuenta = self.etaller.getCuenta()
            sigla = ' CUP'
            if not cuenta:
                salto = 'CUP'
        else:
            cuenta = self.etaller.getCuentaMLC()
            sigla = ' USD'    
            if not cuenta:
                salto = 'USD'

        if salto != '':
            self.generales.mensageInformacion("informacion",
                                "Error de Cuenta",
                                f"No se puede generar la Factura si no tiene cuenta en {salto} asociada, por favor asocie una cuenta en {salto}. ")
        else:            
            ecliente = mCliente().obtenerDatosClientesEspecifica(efactura.getCliente())
            efcliente = mFichaCliente().obtenerFichaClienteEspecifico(efactura.getFichaCliente())
            desglose = ""
            listfdesglose = list()
            for factdesglose in mFacturaDesglose().cargarDatosFacturaDesglose():
                if factdesglose.getFactura() == efactura.getIdFactura():
                    listfdesglose.append(factdesglose)


            def obtenerUM(idunidadmedida):
                um = mUnidadMedida().obtenerUnaUnidadMedidaEspecifica(idunidadmedida)
                return um.getSigla()
            
            def obtenerInventario(idinventario):
                inv = mInventario().obtenerInventarioEspecifico(idinventario)
                
                return inv.getNoInventario()
            

            for fila, data in enumerate(listfdesglose):
                serv = mServicio().obtenerServicioEspecifico(data.getServicio())
                
                
                if data.getInventario() != "":
                    tipo = serv.getDescripcion() + ' ' + self.obtenerEquipo(serv.getEquipo()) + ' (inv-' + obtenerInventario(data.getInventario()) + ')'
                else:
                    tipo =  serv.getDescripcion() + ' ' + self.obtenerEquipo(serv.getEquipo())

                desglose += '<tr><td class="centro">{}</td><td class="inicio">{}</td><td class="centro">{}</td><td class="centro">{}</td><td class="centro">{}</td><td class="centro">{}</td></tr>'.format(fila+1,
                                                                                                                tipo,                                                                  
                                                                                                                    obtenerUM(serv.getUnidadMedida()),   #um                                                                                     
                                                                                                                    data.getCantidad(), #cantidad
                                                                                                                    self.generales.floatToStr(data.getPrecio()),   #precio
                                                                                                                    self.generales.floatToStr(data.getPrecioTotal()))  #importe   
            desglose += '<tr><td></td><td></td><td></td><td></td><td></td><td class="centro">______</td></tr>'
            desglose += '<tr><td></td><td></td><td></td><td></td><td class="fin"><b>TOTAL: </b></td><td class="centro"><b>{}</b></td></tr>'.format(self.generales.floatToStr(efactura.getTotalFactura()))
            contador = 24
                
            if efactura.getNota() != "":
                desglose += "<tr><td colspan='6' aling='left'><b>Comentarios:  </b></td></tr>"
                linea = efactura.getNota()
                desglose += "<tr><td colspan='6' aling='left'>" + linea + "</td></tr>"
                contador = 22
                
            
            for i in range(contador-listfdesglose.__len__()):
                desglose += '<br>'
            
            if efactura.getEstado() == 0:
                nombre = 'Factura Cancelada'
            elif efactura.getEstado() == 1:
                nombre = 'Pre-Factura'
            else:
                nombre = 'Factura'

            imagen = self.imagenImprimir()      
            
            if efcliente.getIdFichaCliente() != "":
                ecargo = mCargo().obtenerCargoEspecifico(efcliente.getCargo()) 
                cargoCliente = ecargo.getDescripcion()
                nombreCliente =efcliente.getNombre() + ' ' + efcliente.getApellidos()
                carnetCliente = efcliente.getCarnet()
            else:
                cargoCliente = '___________________________________'
                nombreCliente = '_______________________________'
                carnetCliente = '_______________________________'
                
            
            factura = {
                'IMAGEN' : imagen,
                'DUENNO':  self.eduenno.getNombre() + ' ' + self.eduenno.getApellidos(),
                'DIRECCION': self.etaller.getDireccion(),
                'LICENCIA': self.eduenno.getLicencia(),
                'TELEFONO': self.eduenno.getTelefono(),
                'FECHA': efactura.getFecha(),
                'TIPO' : nombre + sigla,
                'DOCUMENTO': efactura.getNoFactura(),
                'CLIENTE' : ecliente.getNombre(),
                'DIRCLIENTE' : ecliente.getDireccion(),
                'CTACLIENTE' : ecliente.getCuenta(),
                'CUENTA' : 'en' + sigla + ' ' + cuenta,
                'SUCURSAL' : self.etaller.getSucursal(),
                'NOMBREFAC' : usuario.getNombre() + ' ' + usuario.getApellidos(),
                'CARNETFAC' : usuario.getCarnet(),
                'NOMBRE': nombreCliente,
                'CARNET' : carnetCliente,
                'CARGO' : cargoCliente,
                'DATOS' : desglose
            }
            
            html = self.env.get_template('factura.html')
            documento = QTextDocument()
            
            documento.setHtml(html.render(factura))

            self.generales.vistaPrevia(documento, nombre, parent, efactura.getNoFactura())

    def recepcionDesglosada(self, erecepcion:eRecepcion, usuario:eUsuario, parent): 
        self.eduenno = mDuenno().cargarDatosDuenno()
        self.etaller = mTaller().cargarValorTaller()
        ecliente = mCliente().obtenerDatosClientesEspecifica(erecepcion.getCliente())
        desglose = ""
        listainventario = list()
        for inv in mInventario().cargarDatosInventario():
            if inv.getRecepcion() == erecepcion.getIdRecepcion():
                listainventario.append(inv)


        for fila, data in enumerate(listainventario):
            desglose += '<tr><td class="centro">{}</td><td class="inicio">{}</td><td class="inicio">{}</td><td class="centro">{}</td><td class="centro">{}</td><td class="centro">{}</td></tr>'.format(fila+1,
                                                                                                            data.getNoInventario(),                   #inv                                                               
                                                                                                            self.obtenerEquipo(data.getEquipo()),   #eqipo                                                                                     
                                                                                                            self.obtenerModelo(data.getModelo()),   #modelo
                                                                                                            self.obtenerMarca(data.getMarca()),     #marca
                                                                                                            data.getObservaciones())                  #observaciones
            
        desglose += '<tr><td class="centro"></td><td class="inicio"></td><td class="centro"></td><td class="centro"></td><td class="centro"></td><td class="centro"></td></tr>'
            
        for i in range(26-listainventario.__len__()):
            desglose += '<br>'
        if erecepcion.getEstado() == 0:
            nombre = 'Recepción Cancelada'
        elif erecepcion.getEstado() == 1:
            nombre = 'Pre-Recepción'
        else:
            nombre = 'Recepción'

        imagen = self.imagenImprimir()        

        recepcion = {
            'IMAGEN' : imagen,
            'DUENNO':  self.eduenno.getNombre() + ' ' + self.eduenno.getApellidos(),
            'DIRECCION': self.etaller.getDireccion(),
            'LICENCIA': self.eduenno.getLicencia(),
            'TELEFONO': self.eduenno.getTelefono(),
            'FECHA': erecepcion.getFecha(),
            'TIPO' : nombre,
            'DOCUMENTO': erecepcion.getNoRecepcion(),
            'CLIENTE' : ecliente.getNombre(),
            'DIRCLIENTE' : ecliente.getDireccion(),
            'CTACLIENTE' : ecliente.getCuenta(),
             'NOMBREFAC' : usuario.getNombre() + ' ' + usuario.getApellidos(),
            'CARNETFAC' : usuario.getCarnet(),
            'DATOS' : desglose
        }

        html = self.env.get_template('recepcion.html')
        documento = QTextDocument()
        
        documento.setHtml(html.render(recepcion))

        self.generales.vistaPrevia(documento, nombre, parent, erecepcion.getNoRecepcion())


    def cobroDesglosado(self, ecobro:eCobro, usuario:eUsuario, parent): 
        self.eduenno = mDuenno().cargarDatosDuenno()
        self.etaller = mTaller().cargarValorTaller()
        ecliente = mCliente().obtenerDatosClientesEspecifica(ecobro.getCliente())

        def factura(idfactura):
            efactura = mFactura().obtenerFacturaEspecifico(idfactura)
            return efactura.getNoFactura()

        def tipoPago(idtipo):
            etipo = mTipoPago().obtenerTipoPagoEspecifico(idtipo)
            return etipo.getDescripcion()

        desglose = ""
        listacobro = list()
        for cobro in mCobroFactura().cargarDatosCobroFactura():
            if cobro.getCobro() == ecobro.getIdCobro():
                listacobro.append(cobro)

        tipos = ['Total', 'Parcial', 'Anticipado']

        for fila, data in enumerate(listacobro):
            desglose += '<tr><td class="centro">{}</td><td class="centro">{}</td><td class="centro">{}</td><td class="centro">{}</td></tr>'.format(fila+1,
                                                                                                            tipos[data.getTipo()],   #tipo pago                                                               
                                                                                                            factura(data.getFactura()),   #factura                                                                                     
                                                                                                            self.generales.floatToStr(data.getMonto()))   #importe
            
        desglose += '<tr><td class="centro"></td><td class="centro"></td><td class="centro"></td><td class="centro">___________________</td></tr>'
        desglose += '<tr><td class="centro"></td><td class="centro"></td><td class="fin"><b>{}</b></td><td class="centro"><b>{}</b></td></tr>'.format('TOTAL', self.generales.floatToStr(ecobro.getTotalCobro()))
            
        for i in range(20-listacobro.__len__()):
            desglose += '<br>'
        if ecobro.getEstado() == 0:
            nombre = 'Cobro Cancelado'
        elif ecobro.getEstado() == 1:
            nombre = 'Pre-Cobro'
        else:
            nombre = 'Cobro'

        imagen = self.imagenImprimir()       

        cobro = {
            'IMAGEN' : imagen,
            'DUENNO':  self.eduenno.getNombre() + ' ' + self.eduenno.getApellidos(),
            'DIRECCION': self.etaller.getDireccion(),
            'LICENCIA': self.eduenno.getLicencia(),
            'TELEFONO': self.eduenno.getTelefono(),
            'FECHA': ecobro.getFecha(),
            'TIPO' : nombre,
            'DOCUMENTO': ecobro.getNoCobro(),
            'CLIENTE' : ecliente.getNombre(),
            'DIRCLIENTE' : ecliente.getDireccion(),
            'CTACLIENTE' : ecliente.getCuenta(),
            'INSTRUMENTO' : tipoPago(ecobro.getTipoPago()),
            'NUMERO' : ecobro.getDocumento(),
            'IMPORTE' : self.generales.floatToStr(ecobro.getTotalCobro()),
            'NOMBREFAC' : usuario.getNombre() + ' ' + usuario.getApellidos(),
            'CARNETFAC' : usuario.getCarnet(),
            'DATOS' : desglose
        }

        html = self.env.get_template('cobro.html')
        documento = QTextDocument()
        
        documento.setHtml(html.render(cobro))

        self.generales.vistaPrevia(documento, nombre, parent, ecobro.getNoCobro())
        

    def anticipoDesglosado(self, eanticipo:eAnticipo, usuario:eUsuario, parent): 
        pass
    
        
    def certificoConformidad(self, efactura:eFactura, usuario:eUsuario, parent):
        ecliente = mCliente().obtenerDatosClientesEspecifica(efactura.getCliente())
        efcliente = mFichaCliente().obtenerFichaClienteEspecifico(efactura.getFichaCliente())
        
        equipos = ""
        trabajos = ""
        listfdesglose = list()
        listaTrabajos = list()
        listaEquipos = list()
        for factdesglose in mFacturaDesglose().cargarDatosFacturaDesglose():
            if factdesglose.getFactura() == efactura.getIdFactura():
                listfdesglose.append(factdesglose)


        for data in listfdesglose:
            serv = mServicio().obtenerServicioEspecifico(data.getServicio())
            equip = self.obtenerEquipo(serv.getEquipo())
            trab = serv.getDescripcion()
            
            # verifico que el equipo no se repita
            aux = True            
            for equipo in listaEquipos:
                if equip == equipo:
                    aux = False
                    break
            
            if aux == True:    
                listaEquipos.append(equip)                                                              
       
            # verifico que el trabajo realizado no se repita
            aux = True            
            for trabajo in listaTrabajos:
                if trab == trabajo:
                    aux = False
                    break
            
            if aux == True:     
                listaTrabajos.append(trab)
         
       
        
        for equipo in listaEquipos:
            equipos += equipo + ', '
        
        for trabajo in listaTrabajos:
            trabajos += trabajo + ', '
            
        equipos = equipos[:-2] + '.'
        trabajos = trabajos[:-2] + '.'
        nodocumento = efactura.getNoFactura().replace('-','/')
        
        if efcliente.getIdFichaCliente() != "":
            nombreCliente =efcliente.getNombre() + ' ' + efcliente.getApellidos()
        else:
            nombreCliente = '_______________________________'
        
        conformidad = {
            'DUENNO':  self.eduenno.getNombre() + ' ' + self.eduenno.getApellidos(),
            'DIRECCION': self.etaller.getDireccion(),
            'LICENCIA': self.eduenno.getLicencia(),
            'TELEFONO': self.eduenno.getTelefono(),
            'FECHA': efactura.getFecha(),
            'DOCUMENTO': nodocumento,
            'CLIENTE' : ecliente.getNombre(),
            'DIRCLIENTE' : ecliente.getDireccion(),
            'CTACLIENTE' : ecliente.getCuenta(),
            'CUENTA' : self.etaller.getCuenta(),
            'SUCURSAL' : self.etaller.getSucursal(),
            'NOMBREFAC' : usuario.getNombre() + ' ' + usuario.getApellidos(),
            'NOMBRE': nombreCliente,
            'EQUIPOS' : equipos,
            'TRABAJOS': trabajos,
        }

        html = self.env.get_template('conformidad.html')
        documento = QTextDocument()
        
        documento.setHtml(html.render(conformidad))

        self.generales.vistaPrevia(documento, 'Certifico de Conformidad', parent, nodocumento)
        
        
    def listasConfiguraciones(self, plantilla, datos, nombre, parent):
        imagen = self.imagenImprimir()
        lista = {
            'IMAGEN' : imagen, 
            'NOMBRE' : nombre,
            'DATOS' : datos
        }
    
        html = self.env.get_template(plantilla)
        documento = QTextDocument()
        
        documento.setHtml(html.render(lista))

        self.generales.vistaPrevia(documento, nombre, parent)
    
    
    def imagenImprimir(self):
        self.etaller = mTaller().cargarValorTaller()
        if self.etaller.getLogo() == "../img/Taller.jpeg":
            imagen = self.generales.resource_path("../img/blank.png")
        else:
            encoded = base64.b64encode(self.etaller.getLogo()).decode()  
            imagen = 'data:image/png;base64,{}'.format(encoded)

        return imagen