import json


class Load:
    def __init__(self):
        # Configs vars.
        #! NO MODIFICAR ESTAS VARIABLES, ESTAS DE ASIGNAN DESDE EL ARCHIVO [Config.json]
        self.port = 0 # Puerto donde corre la app principal.
        self.secretKey = 'Zzzzzzzzzzzzzzzzzzzzzzz' # Clave de las API's de Flask.
        self.debug = False; # Estado de las API's.
        
        self.credentials = {}

        # Usuarios permitidos.
        self.authUsers = ['DONT PUT NOTHING HERE']


    
    def configurations(self): 
        # Leemos el archivo de configuraciones.
        with open('./Config.json') as f:
            auth = False # Variable que usaremos para validar si las configuraciones están bien
            data = json.load(f)

            # Validación de los campos básicos.
            MainKeys = list(data.keys())


            if 'AppConfig' in MainKeys and 'AuthKeys' in MainKeys:
                auth = True

            else:
                auth = False
                print("There seems to be something wrong with the configurations. Try downloading the project again from GitHub. (Error 01: Configuration error).")
                exit()


            # Obtenemos las configuraciones de la app.
            if (auth):
                config = data['AppConfig']
                
                # instanciamos las variables de configuración. 
                self.port = config['port']
                
                self.secretKey = config["secretKey"]
                self.debug = config["debug"]

                # Instnaciamos los usuarios permitidos.

                self.authUsers = data['AuthKeys']


                # Obtenemos la ruta de las credenciales, las abrimos y las guardamos.
                # Instnaciamos los usuarios permitidos.
                credentials_route = data['credentials_json']

                with open(credentials_route) as cred:
                    cred_data = json.load(cred)

                    self.credentials['google_email'] = cred_data['google_credentials']['email']
                    self.credentials['google_password'] = cred_data['google_credentials']['password']