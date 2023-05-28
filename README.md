
# Welcome to GPTWrap

  

GPTWrap es una herramienta desarrollada para hacer Web Scraping en ChatGPT y sortear las limitaciones de la API. A OPEN AI es obvio que no le gusta, por tanto, usted se hace cargo del uso que pueda darle a la herramienta, ésta está hecha con fines educacionales y de aprendizaje personales!

Iniciamos un navegador con Selenium y con él navegamos hacia la página de ChatGPT. Allí iniciamos sesión con Google y llevamos al navegador hacia el chat. Una vez allí iniciamos un servidor de Flask para poder hacerle peticiones, el navegador las hará y nos devolverá una respuesta!

---

Esta APP está hecha íntegramente en **Python** y **NO** es necesario tener tecnologías externas a la del mismo Python ajenas a las que instalaremos con ayuda del mismo.

Las principales librerías para  cumplir con nuestro objetivo fueron:

- Flask, para la API a nivel de usuario.
- Selenium, para el webscrapping.

# Instalation


### Instalación de dependencias:
Como hacemos uso de otras librerías codeadas en Python, las instalaremos. Para ello, haremos uso de pip y su formato estándar para descargar estas dependencias (recomendamos usar entornos virtuales).

- Windows:
```bash
	$ py -m pip install -r requirements.txt
```

- Linux:
```bash
	$ python3 -m pip install -r requirements.txt
```


- Mac:
```bash
	$ python3 -m pip install -r requirements.txt
```


# API Configuration.
Una vez con las dependencias necesarias instaladas, pasaremos a configurar nuestra API.

Dentro del archivo ```Config.json``` se encuentran las configuraciones en un formato bastante claro pero leeremos cada sección para cubrir la mayor cantidad de dudas posible.

El ```Config.json``` tiene dos secciones:

- **AppConfig**
- **AuthKeys**


#### AppConfig:
AppConfig contiene las configuraciones principales y más importantes para el funcionamiento de la API. Ustedes deberán configurar cada campo según su uso personal.

- **secretKey**, la clave privada que usa *Flask*. Si no tiene idea de lo que es esto y no pretende tener una API pública, no la cambie.
- **port**, puerto en el que correrá la API de *Flask*. Déjela por defecto si no quiere molestarse en configurar más firewalls o si solo quiere hacer testeos.
- **debug**, modo en el que estará la API de *Flask*. Por defecto lo tenemos en false porque justamente no estamos en un entorno de desarrollo. Si quiere modificar la API, rastrear errores de la misma o cualquier cosa relacionada, deje esto en *true*.
- **credentials_json**, ruta del archivo local en el que se encuentran las credenciales de Google para loguearnos en la web de OpenAI. La estructura del archivo dejado en el```crendentials_json``` debe tener la siguiente estructura:
	```json
		{
			"google_credentials": {
			
				"email": "ggezopenai@retrokode.com",
				"password": "zzzzzzzzzzzz"
				
			}
		}
	``` 


#### AuthKeys:
Cuando creamos una API y queremos llevarla a nivel de producción, es necesario poder controlar quién tiene acceso a ella. Como consecuencia de ello, está el SENCILLO sistema de claves permitidas vía API. El usuario nos la pasará por el *Body* de la petición e idealmente cada usuario tendría uno. Usted le proporcionaría una clave a cada usuario. Las claves se componen de un nombre de usuario y la propia llave o contraseña. El usuario puede ser cualquiera y la clave también puede ser cualqueira, no tiene por qué ser SHA256, pero por fines estéticos, lo dejé así xd. El apartado de *AuthKeys* tendría el siguiente aspecto:

```json
"AuthKeys": {

	"ElHaban3ro": "a59440d7c4276be652c03546c9bba2c5c1665af1756d3689b591049fde5b8c25"

}
```

Si un usuario no pasa su llave pública, no puede acceder. Las **peticiones HTTP** las veremos en el siguiente apartado.


# Use
Para correr la API (y lo que ello conlleva) tenemos que ejecutar el archivo ```gptscrap.py```. Si ya tienes configurado e instalado todo lo necesario, esto tendría que iniciar tu navegador scrapeador y tu API para peticiones. Para correr la API se haría de la siguiente forma.

- Windows:
```bash
	$ py gptscrap
```

- Linux:
```bash
	$ python3 gptscrap.py
```


- Mac:
```bash
	$ python3 gptscrap.py
```


Una vez con esto, ya podemos hacer peticiones y hablar con *ChatGPT*  a través de una API gratuita. Ésta correría en ```localhost:port/API/```, donde ```port``` es el puerto configurado en el archivo ```Config.json```. 

Las URLS de la API y sus usos se muestran a continuación:

- ***Haz peticiones a ChatGPT. Recibe parámetros en su cuerpo.***
> Source: ***/API/Talk/*** 
> Body:
> > **AuthKey**, clave de autorización.
> > **message**, mensaje para enviar al chat.
> 
> Return:
> > **Json Response**, Su estructura tiene:
> >> **response_message**, la respuesta de ChatGPT a nuestra petición.
> >> **actual_time**, hora de la petición.


- ***Reciba un reporte con el estado de la API (una screenshot con la pantalla actual).***
> Source: ***/API/Report/*** 
> Body:
> > **AuthKey**, clave de autorización.
> 
> Return:
> > **Screenshot Image**, imagen de la página actual. Guárdala para mostrarle a tus compañeros o tener más detalle de la respuesta!




- ***Reinicia el navegador. Útil para cualquier circunstancia de error.***
> Source: ***/API/Restart/*** 
> Body:
> > **AuthKey**, clave de autorización.
> 
> Return:
> > **Restart State**, mensaje sobre el estado del reinicio. Bien, mal o panconjamon?

# Próximamente.

Local UI. Interfaz open source para que le des a tu ChatGPT el estilo más gamer de todos!