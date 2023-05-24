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


        print(f'Trying logging with:\n\n\tEmail: {self.google_email}\n\n\tPassword: ************\n\n\tPremium: {"Yes" if self.gpt_premium == True else "No"}')


        # Selenium Confgis
        self.url = 'https://chat.openai.com/'
        self.options = Options() # Instanciamos las configuraciones de Selenium.
        self.options.headless = self.debug  # Sin ventana?


        self.driver = uc.Chrome(options = self.options) # El navegador que se usará. Se inicia.
        self.driver.get(self.url) # Petición a la url de ChatGPT.
        self.driver.maximize_window()


        # | -------------------------- |


        # Click en el botón de login desde la página principal de OPENIA (es la página que aparece directamente al poner chat.openai.com). Esto lo hacemos porque cada que se da al botón genera un ID identificador. De lo contrario sería imposible iniciar sesión (Web de OA).
        to_login_button = WebDriverWait(self.driver, self.time_to_wait).until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn-primary'))) # Obtenemos el botón.
        to_login_button.click()


        # Click en logueo de Google (Web de OA).
        to_login_with_google = WebDriverWait(self.driver, self.time_to_wait).until(EC.element_to_be_clickable((By.CLASS_NAME, 'c1df4626c'))) # Obtenemos el botón.
        to_login_with_google.click()


        # Boton para pasar a poner la password (Web de Google).
        next_google_button = WebDriverWait(self.driver, self.time_to_wait).until(EC.element_to_be_clickable((By.CLASS_NAME, 'VfPpkd-LgbsSe-OWXEXe-k8QpJ'))) # Obtenemos el botón.

        
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
                print('There has been an error with the credentials. Try to check the credentials.')
                exit()


        except:
            pass

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
                print('There has been an error with the credentials. Try to check the credentials.')
                self.driver.close()
                exit()

        except:
            print('Logged!')


        # Acá nos redirige a la web de ChatGPT

        # Click en el botón de next si está disponible. Al parecer en las nuevas cuentas de OA pone un anuncio con info de la propia empresa. Lo que validaremos es si esta existe! (Web de OA).
        time.sleep(2)
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


        print('Ready To Talk, guys c:')

        
        time.sleep(3)  

        # Instanciamos el input para el texto y el botón de envío.
        self.input = self.driver.find_element(By.ID, 'prompt-textarea')
        self.send_button = self.driver.find_elements(By.CLASS_NAME, 'rounded-md')[14]



        # Para testeo:
        self.talk_in_actual_room('Que onda mi pana?')

        self.driver.save_screenshot('ui.png')
        time.sleep(600)



    # Envía un mensaje a ChatGPT.
    def talk_in_actual_room(self, message):
        """
        # Talk in the actual room with ChatGPT.


        # Args:
            - message (str): The message to ChatGPT-


        # Returns:
            - Dict with response.
        
        """


        self.input.send_keys(message) # Escribimos el mensaje en el input.

        # Envíamos el mensaje.
        self.send_button.click()
        
        print(f'Message "{message}" sended!')

        return {'host_message': message}




#! TESTS.
ChatGPT('chatgptscrap@gmail.com', 'XXXX', False)