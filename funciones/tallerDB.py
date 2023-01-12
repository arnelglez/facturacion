import sqlite3

class BaseDatos:

    def __init__(self):
        self.conn = sqlite3.connect('taller.db')
        self.cursor = self.conn.cursor()


        self.cursor.execute('''CREATE TABLE IF NOT EXISTS taller (        
            idtaller INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre	TEXT,
            direccion	TEXT,
            cuenta	TEXT,
            logo	BLOB,
            licencia	TEXT,
            sucursal	TEXT,
            cuentamlc	TEXT
            ); ''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS duenno (
            idduenno INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre	TEXT,
            apellidos	TEXT,
            carnet	TEXT,
            licencia	INTEGER,
            telefono	TEXT
            ); ''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS cliente (
            idcliente INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre	TEXT,
            contrato	TEXT,
            direccion	TEXT,
            cuenta	TEXT,
            activo  INTEGER
            ); ''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS cargo (
            idcargo INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion	TEXT
            ); ''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS fichacliente (
            idfichacliente INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre	TEXT,
            apellidos	TEXT,
            carnet	TEXT,
            cargo	INTEGER,
            cliente INTEGER,
            activo  INTEGER,
            FOREIGN KEY(cargo) REFERENCES cargo(idcargo),
            FOREIGN KEY(cliente) REFERENCES cliente(idcliente)
            ); ''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS unidadmedida (
            idunidadmedida INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion	TEXT,
            sigla	TEXT,
            activo  INTEGER
            ); ''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS equipo (
            idequipo INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion	TEXT,
            activo  INTEGER,
            multiple INTEGER
            ); ''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS servicio (
            idservicio INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion	TEXT,
            precio	REAL,
            unidadmedida    INTEGER,
            equipo	INTEGER,
            activo  INTEGER,
            FOREIGN KEY(equipo) REFERENCES equipo(idequipo),
            FOREIGN KEY(unidadmedida) REFERENCES unidadmedida(idunidadmedida)
            ); ''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS marca (
            idmarca INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion   TEXT,
            equipo  INTEGER,
            FOREIGN KEY(equipo) REFERENCES equipo(idequipo)
            ); ''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS modelo (
            idmodelo INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion  TEXT,
            marca   INTEGER,
            equipo	INTEGER,
            FOREIGN KEY(marca) REFERENCES marca(idmarca),
            FOREIGN KEY(equipo) REFERENCES equipo(idequipo)
            ); ''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS usuario (
            idusuario INTEGER PRIMARY KEY AUTOINCREMENT,
            username	TEXT, 
            passwd	TEXT,
            carnet  TEXT,
            nombre	TEXT,
            apellidos	TEXT,
            activo  INTEGER
            );  ''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS recepcion (
            idrecepcion INTEGER PRIMARY KEY AUTOINCREMENT,
            norecepcion TEXT,
            usuario	INTEGER,
            cliente	INTEGER,
            fecha	TEXT,
            estado  INTEGER,
            FOREIGN KEY(usuario) REFERENCES usuario(idusuario),
            FOREIGN KEY(cliente) REFERENCES cliente(idcliente)
            ); ''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS inventario (
            idinventario INTEGER PRIMARY KEY AUTOINCREMENT,
            recepcion	INTEGER,
            equipo	INTEGER,
            marca	INTEGER,
            modelo	INTEGER,
            noinventario	TEXT,
            observaciones	TEXT,
            activo	 INTEGER,
            FOREIGN KEY(recepcion) REFERENCES recepcion(idrecepcion),
            FOREIGN KEY(equipo) REFERENCES equipo(idequipo)                        
            ); ''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS factura (
            idfactura INTEGER PRIMARY KEY AUTOINCREMENT,
            nofactura   TEXT,
            usuario	INTEGER,
            cliente	INTEGER,
            fichacliente    INTEGER,
            fecha	TEXT,
            totalfactura	REAL,
            estado  INTEGER,
            nota TEXT,
            moneda  INTEGER,
            FOREIGN KEY(usuario) REFERENCES usuario(idusuario),
            FOREIGN KEY(cliente) REFERENCES cliente(idcliente),
            FOREIGN KEY(fichacliente) REFERENCES fichacliente(idfichacliente)
            ); ''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS facturadesglose (
            idfacdesglose INTEGER PRIMARY KEY AUTOINCREMENT,
            factura	INTEGER,
            tipo    INTEGER,
            servicio	INTEGER,
            inventario  INTEGER,
            cantidad    FLOAT,
            precio	REAL,
            preciototal REAL,
            FOREIGN KEY(factura) REFERENCES factura(idfactura),
            FOREIGN KEY(servicio) REFERENCES servicios(idservicio)
            ); ''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tipopago (
            idtipopago INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion	TEXT,
            activo  INTEGER
            ); ''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS cobro (
            idcobro INTEGER PRIMARY KEY AUTOINCREMENT,
            nocobro TEXT,
            usuario	INTEGER,
            cliente	INTEGER,
            fecha	TEXT,
            totalcobro	REAL,
            tipopago	INTEGER,
            documento   TEXT,
            estado  INTEGER,
            fechaemision    TEXT,
            FOREIGN KEY(tipopago) REFERENCES tipopago(idtipopago),
            FOREIGN KEY(usuario) REFERENCES usuario(idusuario),
            FOREIGN KEY(cliente) REFERENCES cliente(idcliente)
            ); ''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS cobrofactura (
            idcobrofactura INTEGER PRIMARY KEY AUTOINCREMENT,
            cobro	INTEGER,
            tipo    INTEGER,
            factura	INTEGER,
            monto	REAL,
            FOREIGN KEY(cobro) REFERENCES cobro(idcobro)
            ); ''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS anticipo (
            idanticipo INTEGER PRIMARY KEY AUTOINCREMENT,
            cobrofactura   INTEGER,
            usuario	INTEGER,
            cliente	INTEGER,
            noanticipo    TEXT,
            fecha   TEXT,
            nodocumento   TEXT,
            fechaemision TEXT,
            factura INTEGER,
            monto	REAL,
            estado  INTEGER,
            FOREIGN KEY(cobrofactura) REFERENCES cobrofactura(idcobrofactura)
            ); ''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS fecha (
            idfecha INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha_procesamiento   DATE
            ); ''')

        self.cursor.execute('''DROP TABLE IF EXISTS liquidado;''')

        # agegando columna fecha de eimsion en la tabla cobro
        self.cursor.execute("PRAGMA table_info(cobro)")
        campos = self.cursor.fetchall()

        existe = False
        for campo in campos:
            if campo[1] == 'fechaemision':
                existe = True
                break
        
        if existe == False:
            self.cursor.execute("ALTER TABLE cobro ADD COLUMN fechaemision TEXT")

        # agegando columna nota en la tabla factura
        self.cursor.execute("PRAGMA table_info(factura)")
        campos = self.cursor.fetchall()

        existe = False
        for campo in campos:
            if campo[1] == 'nota':
                existe = True
                break
        
        if existe == False:
            self.cursor.execute("ALTER TABLE factura ADD COLUMN nota TEXT")
            # inicializo commentarios vacios
            self.cursor.execute("SELECT idfactura FROM factura")
            factura = self.cursor.fetchall()  

            for fac in factura:
                consulta = "UPDATE factura SET nota = '' WHERE idfactura = ?"
                self.cursor.execute(consulta, fac )
                self.conn.commit()
        
        
        # agegando columna moneda en la tabla factura
        self.cursor.execute("PRAGMA table_info(factura)")
        campos = self.cursor.fetchall()

        existe = False
        for campo in campos:
            if campo[1] == 'moneda':
                existe = True
                break
        
        if existe == False:
            self.cursor.execute("ALTER TABLE factura ADD COLUMN moneda TEXT")
            # inicializo en 0 (CUP)
            self.cursor.execute("SELECT idfactura FROM factura")
            factura = self.cursor.fetchall()  

            for fac in factura:
                consulta = "UPDATE factura SET moneda = 0 WHERE idfactura = ?"
                self.cursor.execute(consulta, fac )
                self.conn.commit()
        
        
        # agregando columna multiple en tabla equipo
        self.cursor.execute("PRAGMA table_info(equipo)")
        campos = self.cursor.fetchall()

        existe = False
        for campo in campos:
            if campo[1] == 'multiple':
                existe = True
                break
        
        if existe == False:
            self.cursor.execute("ALTER TABLE equipo ADD COLUMN multiple INTEGER")
            # inicializo todos los equipos el campo multiple a 0
            self.cursor.execute("SELECT idequipo FROM equipo")
            equipos = self.cursor.fetchall()  

            for equipo in equipos:
                consulta = "UPDATE equipo SET multiple = 0 WHERE idequipo = ?"
                self.cursor.execute(consulta, equipo )
                self.conn.commit()
        
        # agregando columna cantidad en tabla inventario
        self.cursor.execute("PRAGMA table_info(inventario)")
        campos = self.cursor.fetchall()

        existe = False
        for campo in campos:
            if campo[1] == 'cantidad':
                existe = True
                break
        
        if existe == False:
            self.cursor.execute("ALTER TABLE inventario ADD COLUMN cantidad INTEGER")
            # inicializo todos los inventarios anteriores a 1
            self.cursor.execute("SELECT idinventario FROM inventario")
            inventario = self.cursor.fetchall()  

            for inv in inventario:
                consulta = "UPDATE inventario SET cantidad = 1 WHERE idinventario = ?"
                self.cursor.execute(consulta, inv )
                self.conn.commit()

      
        # agregando columna cuenta mlc en tabla taller
        self.cursor.execute("PRAGMA table_info(taller)")
        campos = self.cursor.fetchall()

        existe = False
        for campo in campos:
            if campo[1] == 'cuentamlc':
                existe = True
                break
        
        if existe == False:
            self.cursor.execute("ALTER TABLE taller ADD COLUMN cuentamlc TEXT")

        ### Verifico que no este creado el usuario admin antes de crearlo
        self.cursor.execute("SELECT idusuario FROM usuario")
        usuario = self.cursor.fetchone()  

        if not usuario:
            self.cursor.execute('''INSERT INTO usuario (username, passwd, carnet, nombre, apellidos, activo)
		                                VALUES ('admin', 'gAAAAABhLkav5TpBeRcAbgmWjuJRxkb7RxHJTta-6zPZHRmAJY_b_GHZ2ceO7ZtYO1IM9STT05jxwqQL1GcwYiyvziPGxrPDIg==', '11111111111', 'Administrador', 'Estandar', 1)''')
            self.conn.commit()
        if usuario:
            self.cursor.execute("SELECT idusuario, username FROM usuario")
            usuarios = self.cursor.fetchall()  

            for user in usuarios:
                consulta = "UPDATE usuario SET username = ? WHERE idusuario = ?"
                self.cursor.execute(consulta, (user[1].lower(), user[0]))
                self.conn.commit()


        ### Inicializo algunos de los equipos a reparar
        self.cursor.execute("SELECT idequipo FROM equipo")
        equipo = self.cursor.fetchone()

        if not equipo:
            self.cursor.execute("INSERT INTO equipo (descripcion, activo) VALUES ('Impresora Laser', 1)")
            self.conn.commit()

            self.cursor.execute("INSERT INTO equipo (descripcion, activo) VALUES ('Impresora de Tinta', 1)")
            self.conn.commit()

            self.cursor.execute("INSERT INTO equipo (descripcion, activo) VALUES ('Impresora Matricial', 1)")
            self.conn.commit()

            self.cursor.execute("INSERT INTO equipo (descripcion, activo) VALUES ('Unidad Central', 1)")
            self.conn.commit()

            self.cursor.execute("INSERT INTO equipo (descripcion, activo) VALUES ('Monitor CRT', 1)")
            self.conn.commit()

            self.cursor.execute("INSERT INTO equipo (descripcion, activo) VALUES ('Monitor LED', 1)")
            self.conn.commit()

            self.cursor.execute("INSERT INTO equipo (descripcion, activo) VALUES ('Mouse', 1)")
            self.conn.commit()

            self.cursor.execute("INSERT INTO equipo (descripcion, activo) VALUES ('Teclado', 1)")
            self.conn.commit()

            self.cursor.execute("INSERT INTO equipo (descripcion, activo) VALUES ('UPS', 1)")
            self.conn.commit()

        ### Verifico que no esten creados los tipos de cobro antes de crearlos
        self.cursor.execute("SELECT idtipopago FROM tipopago")
        tipo = self.cursor.fetchone()  

        if not tipo:
            self.cursor.execute('''INSERT INTO tipopago (descripcion, activo)
		                                VALUES ('Cheque', 1)''')
            self.conn.commit()

            self.cursor.execute('''INSERT INTO tipopago (descripcion, activo)
		                                VALUES ('Trasferencia', 1)''')
            self.conn.commit()

            self.cursor.execute('''INSERT INTO tipopago (descripcion, activo)
		                                VALUES ('Efectivo', 1)''')
            self.conn.commit()

        ### Verifico que no esten creados los tipos de cobro antes de crearlos
        self.cursor.execute("SELECT idcargo FROM cargo")
        cargo = self.cursor.fetchone()  

        if not cargo:
            self.cursor.execute('''INSERT INTO cargo (descripcion)
		                                VALUES ('Director')''')
            self.conn.commit()

            self.cursor.execute('''INSERT INTO cargo (descripcion)
		                                VALUES ('Adjunto')''')
            self.conn.commit()

            self.cursor.execute('''INSERT INTO cargo (descripcion)
		                                VALUES ('Económico')''')
            self.conn.commit()

            self.cursor.execute('''INSERT INTO cargo (descripcion)
		                                VALUES ('Informático')''')
            self.conn.commit()
    
    
    def __del__(self):
        self.conn.close()

class BaseTaller:

    def abrir(self):
        conn = sqlite3.connect('taller.db')
        return conn
    
    def consultaOne(self, consulta):
        conn = self.abrir()
        cursor = conn.cursor()
        cursor.execute(consulta)
        return cursor.fetchone()

    def consultaAll(self, consulta):
        conn = self.abrir()
        cursor = conn.cursor()
        cursor.execute(consulta)
        return cursor.fetchall()

    def consultaBusqueda(self, consulta, datos):
        conn = self.abrir()
        cursor = conn.cursor()
        cursor.execute(consulta, datos)
        return cursor.fetchall()

    def consultaParametros(self, consulta, datos):
        conn = self.abrir()
        cursor = conn.cursor()
        cursor.execute(consulta, datos)
        return cursor.fetchone()

    def guardarEditar(self, consulta, datos):
        conn = self.abrir()
        cursor = conn.cursor()
        cursor.execute(consulta, datos)
        conn.commit()
        conn.close()
