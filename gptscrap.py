# Clase y métodos usados para hacer scraping en https://chat.openai.com/

        # Imports.

# - Selenium.
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# To undetected.
import undetected_chromedriver as uc

# Others.
import time
import random
import datetime
import sqlite3
from html import unescape


# Librerías para la API.
from flask import Flask, request, jsonify, send_file
from markupsafe import escape
from werkzeug.utils import secure_filename


# Importamos nuestra clase para cargar las configuraciones y demás.
from load import Load




# Cargamos las configuraciones.
load = Load()
lConfig = load.configurations()

# Instanciando la app de Flask.
app = Flask(__name__)
app.config.from_mapping(

    SECRET_KEY = load.secretKey,

)




class ChatGPT:
    def __init__(self, google_email: str, google_password: str, gpt_premium = False, debug = False, time_to_wait = 5):

        """
        # Usa chatGPT sin limitaciones. Es necesario loguear con google.

        DONT USE YOUR PERSONAL ACCOUNT, PLEASE! 🤖

        # Args:
            - google_email (str): Your google email.
            - google_password (str): Your google password.
            - gpt_premium (bool): If you have GPT+ buying.
            - debug (bool): Debug mode?
            - time_to_wait (float): The time you will wait between pages to click on the buttons. We should ideally make sure that the page is fully loaded, and this can vary by computer, so no one knows your computer better than you.


        # Returns:
            - None: none.
        
        """



        # Personal Configs
        self.google_email = google_email
        self.google_password = google_password
        self.gpt_premium = gpt_premium
        self.debug = debug
        self.time_to_wait = time_to_wait
        self.is_busy = False
        self.responses = []

        self.cola = [] # Cola de mensajes.


        print(f'[{datetime.datetime.now().time()}] Trying logging with:\n\n\tEmail: {self.google_email}\n\n\tPassword: ************\n\n\tPremium: {"Yes" if self.gpt_premium == True else "No"}\n\n')


        # Selenium Confgis
        self.url = 'https://chat.openai.com/'
        self.options = Options() # Instanciamos las configuraciones de Selenium.
        self.options.headless = self.debug  # Sin ventana?


        self.driver = uc.Chrome(options = self.options) # El navegador que se usará. Se inicia.
        self.driver.get(self.url) # Petición a la url de ChatGPT.
        self.driver.maximize_window()


        # | -------------------------- |

        # Conexión a la base de datos donde estará el hisyorial.
        conn = sqlite3.connect('history.db')
        cursor = conn.cursor()

        try:
            cursor.execute("""
            
            CREATE TABLE history (
            
                from, message, time

            )
            
            """)

        except:
            pass


        # Click en el botón de login desde la página principal de OPENIA (es la página que aparece directamente al poner chat.openai.com). Esto lo hacemos porque cada que se da al botón genera un ID identificador. De lo contrario sería imposible iniciar sesión (Web de OA).
        to_login_button = WebDriverWait(self.driver, self.time_to_wait).until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn-primary'))) # Obtenemos el botón.
        to_login_button.click()


        # Click en logueo de Google (Web de OA).
        to_login_with_google = WebDriverWait(self.driver, self.time_to_wait).until(EC.element_to_be_clickable((By.CLASS_NAME, 'c1df4626c'))) # Obtenemos el botón.
        to_login_with_google.click()


        # Boton para pasar a poner la password (Web de Google).
        next_google_button = WebDriverWait(self.driver, self.time_to_wait).until(EC.element_to_be_clickable((By.CLASS_NAME, 'VfPpkd-LgbsSe-OWXEXe-k8QpJ'))) # Obtenemos el botón.

        
        print(f'[{datetime.datetime.now().time()}] In google login... Writing the email.')

        
        # Tomamos el input del correo (Web de Google).
        email_google_input = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'whsOnd'))) # Obtenemos el botón.
        email_google_input.send_keys(self.google_email)
        
        # Siguiente página: password.
        next_google_button.click()

        time.sleep(5)
        

        # intentamos valdiar si está bien la contraseña. Si falla es porque estpa bien la password.
        try:
            result = self.driver.find_elements(By.CLASS_NAME, 'Jj6Lae')[0].text.lower()
            if ('email' in result or 'cuenta' in result or 'account' in result): # Validamos si introdujo bien la contraseña.
                print(result)
                self.driver.close()
                print(f'[{datetime.datetime.now().time()}] There has been an error with the credentials. Try to check the credentials.')
                exit()


        except:
            pass

        print(f'[{datetime.datetime.now().time()}] In google login... Writing the password.')
        # Ponemos la password.
        password_google_input = WebDriverWait(self.driver, 7).until(EC.element_to_be_clickable((By.CLASS_NAME, 'whsOnd'))) # Obtenemos el botón.
        password_google_input.send_keys(self.google_password)

        next_google_button = WebDriverWait(self.driver, self.time_to_wait).until(EC.element_to_be_clickable((By.CLASS_NAME, 'VfPpkd-LgbsSe-OWXEXe-k8QpJ'))) # Obtenemos el botón.

        # Click en siguiente. (termina?)
        next_google_button.click()

        time.sleep(5)

        # intentamos valdiar si está bien la contraseña. Si falla es porque estpa bien la password.
        try:
            result = self.driver.find_elements(By.CLASS_NAME, 'OyEIQ')[0].find_elements(By.XPATH, '//div/span')[2]
            if ('password' in result.text or 'contraseña' in result.text): # Validamos si introdujo bien la contraseña.
                print(f'[{datetime.datetime.now().time()}] There has been an error with the credentials. Try to check the credentials.')
                self.driver.close()
                exit()

        except:
            print(f'[{datetime.datetime.now().time()}] Logged!')


        # Acá nos redirige a la web de ChatGPT

        # Click en el botón de next si está disponible. Al parecer en las nuevas cuentas de OA pone un anuncio con info de la propia empresa. Lo que validaremos es si esta existe! (Web de OA).
        time.sleep(2)

        try:
            to_next_button = WebDriverWait(self.driver, self.time_to_wait).until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn-neutral'))) # Obtenemos el botón.

            if (to_next_button != None):
                to_next_button.click()
            
                time.sleep(1)
                # Saltamos ahora la siguente ventana de anuncio.
                to_next_button = self.driver.find_elements(By.CLASS_NAME, 'btn-neutral')[1]
                to_next_button.click()
            
                time.sleep(1)
                # Damos ahora en "Done"!
                to_dones_button = self.driver.find_elements(By.CLASS_NAME, 'btn-primary')[1]
                to_dones_button.click()

        except:
            pass

        print(f'[{datetime.datetime.now().time()}] Ready To Talk, guys c:')

        
        time.sleep(3)  

        # Instanciamos el input para el texto y el botón de envío.
        self.input = self.driver.find_element(By.ID, 'prompt-textarea')
        self.send_button = self.driver.find_elements(By.CLASS_NAME, 'rounded-md')[-1]

        # Running API
        print(f'[{datetime.datetime.now().time()}] Running API...')


        @app.route("/API/Talk/", methods = ["POST"])
        def talk():
            # Validamos si nos están pasando una clave de acceso.
            if 'AuthKey' in request.form:
                AuthKey = request.form['AuthKey'] # Clave de acceso pasada.
                auth = False


                # Valdidamos la clave.
                for username in load.authUsers:
                    if AuthKey == load.authUsers[username]:
                        auth = True
                        break

                    else:
                        auth = False
                        return "You are not authorized to use the API. Contact your system administrator or try again."


                # Si está autorizado. Pasamos a la siguiente fase: Recibir el audio.
                if (auth):
                    
                    if 'message' in request.form:

                        message = request.form['message']
                        res = self.talk_in_actual_room(message) # Hacemos la petición de generar una respuesta.


                        return res

                    else:
                        message = 'De donde proviene la frase "pan con jamón"? Mis compañeros dijeron que era del filosofo griego Alquimedes.'

                else:
                    return "You are not authorized on the API side. Contact the developer to get access to the API."
                
            else:
                return "It appears that you are not passing an authorization key. Make sure you are passing the 'AuthKey' parameter."


        @app.route("/API/Report", methods = ['POST'])
        def report():
            # Validamos si nos están pasando una clave de acceso.
            if 'AuthKey' in request.form:
                AuthKey = request.form['AuthKey'] # Clave de acceso pasada.
                auth = False


                # Valdidamos la clave.
                for username in load.authUsers:
                    if AuthKey == load.authUsers[username]:
                        auth = True
                        break

                    else:
                        auth = False
                        return "You are not authorized to use the API. Contact your system administrator or try again."


                # Si está autorizado. Pasamos a la siguiente fase: Recibir el audio.
                if (auth):
                    
                    
                    screenshot = self.api_report()
                    screenshot_route = screenshot['screenshot_url']

                    return send_file(screenshot_route, mimetype='image/jpg')


                else:
                    return "You are not authorized on the API side. Contact the developer to get access to the API."
                
            else:
                return "It appears that you are not passing an authorization key. Make sure you are passing the 'AuthKey' parameter."


        @app.route("/API/Restart", methods = ['POST'])
        def restart():
            # Validamos si nos están pasando una clave de acceso.
            if 'AuthKey' in request.form:
                AuthKey = request.form['AuthKey'] # Clave de acceso pasada.
                auth = False


                # Valdidamos la clave.
                for username in load.authUsers:
                    if AuthKey == load.authUsers[username]:
                        auth = True
                        break

                    else:
                        auth = False
                        return "You are not authorized to use the API. Contact your system administrator or try again."


                # Si está autorizado. Pasamos a la siguiente fase: Recibir el audio.
                if (auth):
                    
                    print('Restarting inference API...')

                    print(f'[{datetime.datetime.now().time()}] Trying logging with:\n\n\tEmail: {self.google_email}\n\n\tPassword: ************\n\n\tPremium: {"Yes" if self.gpt_premium == True else "No"}\n\n')


                    try:
                        # Selenium Confgis
                        self.url = 'https://chat.openai.com/'
                        self.options = Options() # Instanciamos las configuraciones de Selenium.
                        self.options.headless = self.debug  # Sin ventana?


                        self.driver = uc.Chrome(options = self.options) # El navegador que se usará. Se inicia.
                        self.driver.get(self.url) # Petición a la url de ChatGPT.
                        self.driver.maximize_window()


                        # | -------------------------- |

                        # Conexión a la base de datos donde estará el hisyorial.
                        conn = sqlite3.connect('history.db')
                        cursor = conn.cursor()

                        try:
                            cursor.execute("""
                            
                            CREATE TABLE history (
                            
                                from, message, time

                            )
                            
                            """)

                        except:
                            pass


                        # Click en el botón de login desde la página principal de OPENIA (es la página que aparece directamente al poner chat.openai.com). Esto lo hacemos porque cada que se da al botón genera un ID identificador. De lo contrario sería imposible iniciar sesión (Web de OA).
                        to_login_button = WebDriverWait(self.driver, self.time_to_wait).until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn-primary'))) # Obtenemos el botón.
                        to_login_button.click()


                        # Click en logueo de Google (Web de OA).
                        to_login_with_google = WebDriverWait(self.driver, self.time_to_wait).until(EC.element_to_be_clickable((By.CLASS_NAME, 'c1df4626c'))) # Obtenemos el botón.
                        to_login_with_google.click()


                        # Boton para pasar a poner la password (Web de Google).
                        next_google_button = WebDriverWait(self.driver, self.time_to_wait).until(EC.element_to_be_clickable((By.CLASS_NAME, 'VfPpkd-LgbsSe-OWXEXe-k8QpJ'))) # Obtenemos el botón.

                        
                        print(f'[{datetime.datetime.now().time()}] In google login... Writing the email.')

                        
                        # Tomamos el input del correo (Web de Google).
                        email_google_input = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'whsOnd'))) # Obtenemos el botón.
                        email_google_input.send_keys(self.google_email)
                        
                        # Siguiente página: password.
                        next_google_button.click()

                        time.sleep(5)
                        

                        # intentamos valdiar si está bien la contraseña. Si falla es porque estpa bien la password.
                        try:
                            result = self.driver.find_elements(By.CLASS_NAME, 'Jj6Lae')[0].text.lower()
                            if ('email' in result or 'cuenta' in result or 'account' in result): # Validamos si introdujo bien la contraseña.
                                print(result)
                                self.driver.close()
                                print(f'[{datetime.datetime.now().time()}] There has been an error with the credentials. Try to check the credentials.')
                                exit()


                        except:
                            pass

                        print(f'[{datetime.datetime.now().time()}] In google login... Writing the password.')
                        # Ponemos la password.
                        password_google_input = WebDriverWait(self.driver, 7).until(EC.element_to_be_clickable((By.CLASS_NAME, 'whsOnd'))) # Obtenemos el botón.
                        password_google_input.send_keys(self.google_password)

                        next_google_button = WebDriverWait(self.driver, self.time_to_wait).until(EC.element_to_be_clickable((By.CLASS_NAME, 'VfPpkd-LgbsSe-OWXEXe-k8QpJ'))) # Obtenemos el botón.

                        # Click en siguiente. (termina?)
                        next_google_button.click()

                        time.sleep(5)

                        # intentamos valdiar si está bien la contraseña. Si falla es porque estpa bien la password.
                        try:
                            result = self.driver.find_elements(By.CLASS_NAME, 'OyEIQ')[0].find_elements(By.XPATH, '//div/span')[2]
                            if ('password' in result.text or 'contraseña' in result.text): # Validamos si introdujo bien la contraseña.
                                print(f'[{datetime.datetime.now().time()}] There has been an error with the credentials. Try to check the credentials.')
                                self.driver.close()
                                exit()

                        except:
                            print(f'[{datetime.datetime.now().time()}] Logged!')


                        # Acá nos redirige a la web de ChatGPT

                        # Click en el botón de next si está disponible. Al parecer en las nuevas cuentas de OA pone un anuncio con info de la propia empresa. Lo que validaremos es si esta existe! (Web de OA).
                        time.sleep(2)

                        try:
                            to_next_button = WebDriverWait(self.driver, self.time_to_wait).until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn-neutral'))) # Obtenemos el botón.

                            if (to_next_button != None):
                                to_next_button.click()
                            
                                time.sleep(1)
                                # Saltamos ahora la siguente ventana de anuncio.
                                to_next_button = self.driver.find_elements(By.CLASS_NAME, 'btn-neutral')[1]
                                to_next_button.click()
                            
                                time.sleep(1)
                                # Damos ahora en "Done"!
                                to_dones_button = self.driver.find_elements(By.CLASS_NAME, 'btn-primary')[1]
                                to_dones_button.click()

                        except:
                            pass

                        print(f'[{datetime.datetime.now().time()}] Ready To Talk, guys c:')

                        
                        time.sleep(3)  

                        # Instanciamos el input para el texto y el botón de envío.
                        self.input = self.driver.find_element(By.ID, 'prompt-textarea')
                        self.send_button = self.driver.find_elements(By.CLASS_NAME, 'rounded-md')[-1]

                        print('The inference source was restarted.')

                        return 'The inference source was restarted.'

                    except:
                        print('An error while we are restarting...')
                        
                        return 'An error while we are restarting...'


                else:
                    return "You are not authorized on the API side. Contact the developer to get access to the API."
                
            else:
                return "It appears that you are not passing an authorization key. Make sure you are passing the 'AuthKey' parameter."




        print(f'[{datetime.datetime.now().time()}] API Runned.')
        # Configuración básica de la app. Esto es bueno tenerlo claro para el desplegue.
        app.run(port = load.port, debug = load.debug)

        


    # Envía un mensaje a ChatGPT.
    def talk_in_actual_room(self, message, behaviour = 'Recuerda comportarte como si fueses un bot de discord que busca ayudar a los usuarios y te llamas RetroAssistant, aquí mi texto: '):
        """
        # Talk in the actual room with ChatGPT.


        # Args:
            - message (str): The message to ChatGPT-


        # Returns:
            - Dict with response.
        
        """

        while True:
            if self.is_busy != False:
                # Conexión a la base de datos donde estará el hisyorial.
                conn = sqlite3.connect('history.db')

                cursor = conn.cursor()
                self.is_busy = True


                # Bot presset. His behaviour.
                
                message = behaviour + message

                self.input.send_keys(message) # Escribimos el mensaje en el input.

                # Envíamos el mensaje.
                self.send_button = self.driver.find_elements(By.CLASS_NAME, 'rounded-md')[-1] # Lo volvemos a instanciar porque al parecer causa errores.
                self.send_button.click()
                
                
                cursor.execute(f"""
                
                    INSERT INTO history VALUES('@Uwu', '{message}', '{datetime.datetime.now().time()}')
                
                """)

                conn.commit()

                
                while True:
                    # btn[1]
                    # flex
                    
                    # Regenerate response button (or generating...)
                    time.sleep(2)
                    
                    try:
                        generating_button = self.driver.find_elements(By.CLASS_NAME, 'btn')[1]
                        generating_button = generating_button.find_element(By.CLASS_NAME, 'flex')
                    
                        if generating_button.text == 'Stop generating':
                            print(f'[{datetime.datetime.now().time()}] Generating response...')

                        elif generating_button.text == 'Regenerate response':
                            print(f'[{datetime.datetime.now().time()}] We recive a response!')
                            break

                        else:
                            print('Algo ha ocurrido :/')


                    except:
                        time.sleep(3) # Si falla, quiere decir que da la opción de seguir generando, quizás esto nos interese después.
                        generating_button = self.driver.find_elements(By.CLASS_NAME, 'btn')[1]
                        generating_button = generating_button.find_element(By.CLASS_NAME, 'flex')

                        if generating_button.text == 'Stop generating':
                            print(f'[{datetime.datetime.now().time()}] Generating response...')

                        elif generating_button.text == 'Regenerate response':
                            print(f'[{datetime.datetime.now().time()}] We recive a response!')
                            break

                        else:
                            print('Algo ha ocurrido :/')
                    
                response = self.driver.find_elements(By.CLASS_NAME, 'markdown') # Obtenemos el último mensaje.

                if isinstance(response, list):
                    self.responses.append(unescape(response[-1].text))

                else:
                    self.responses.append(unescape(response.text))
                    
                print(self.responses[-1])

                cursor.execute(f"""
                
                    INSERT INTO history VALUES ('GPT', '{self.responses[-1]}', '{datetime.datetime.now().time()}')
                
                """)


                conn.commit()

                print(f'[{datetime.datetime.now().time()}] Message "{message}" sended!')

                self.api_report()
                self.is_busy = False

                return jsonify({'response_message': self.responses[-1], 'actual_time': f'[{datetime.datetime.now().time()}]'}), 200, {'Content-Type': 'application/json; charset=utf-8'}

            else:
                time.sleep(2)



    # Obtén un reporte de la API.
    def api_report(self):
        """
        # Get a report about the API.


        # Args:
            - Nothing.


        # Returns:
            - Dict with response.
        
        """
        
        # Tomamos una captura.
        screenshot_route = f'./reports/[GTPWrap] {random.randint(0, 200)} - {random.randint(0, 10)}.png'
        self.driver.save_screenshot(screenshot_route)
        
        print(f'API is Busy: {self.is_busy}\nScreenshot: TODO, GENERATE A LINK WITH FLASK')

        return {'is_busy': self.is_busy, 'screenshot_url': screenshot_route}


#! TESTS.
ChatGPT(load.credentials['google_email'], load.credentials['google_password'], False)