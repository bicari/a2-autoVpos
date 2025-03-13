import os

from datetime import datetime

with os.scandir(r'downloads') as ficheros:
    for fichero in ficheros:
        if datetime.now().strftime("%Y%m%d") in fichero.name:
            print(fichero.name)
                