import pyodbc
from read_file import read_txt
from read_ini import read_ini
from querys import insertDataDetalle, insertDataLote
from logs import logger
import os
from zipfile import ZipFile

import re

import os


def extract_file(path_file:str, path_extraction:str):
    try:
        with ZipFile(path_file) as zip:
            zip.extractall(path_extraction)
        return True    
    except Exception as e:
        print(e)    


def insert_data_bank():
    log = logger()
    
    zip_files =  os.listdir('downloads')
    log.info(str(zip_files))
    try:
        if read_ini('CONFIG', 'DETALLAR_OPERACIONES')[0]:
            log.info('Iniciando Descompresion de archivos detallados')
            patron_detalle = re.compile(r"^Detalle1964.*.zip", re.IGNORECASE)
            for file in zip_files:
                if patron_detalle.match(file):
                    extract_file(f'downloads\\{file}', 'detalle')
                    log.info('Descompresion de archivos detallados finalizada')
                    
            for txt_file in os.listdir('detalle'):
                patron = re.compile(r'^Detalle\d+(.+?)\d+\.txt$')
                banco = patron.match(txt_file)
                if banco.group(1) in read_ini('CONFIG', 'BANCOS')[0].keys():
                    log('Insertando en banco', {'type': 'info'})
                    for linea in read_txt('txt\\{file}'.format(file=txt_file)):
                        insertDataDetalle(linea)
                    os.remove(f'detalle\\{txt_file}')
                    log('Insercion finalizada con éxito', {'type': 'info'})
                else:
                    log(f'Archivo de banco:{banco.group(1)} no encontrado o no configurado', {'type': 'warning'})        
        else:
            log.info('Iniciando Descompresion de archivos en lote')
            patron_lote = re.compile(r"^Lote1964.*.zip", re.IGNORECASE)
            for file in zip_files:
                if patron_lote.match(file):
                    extract_file(f'downloads\\{file}', 'lote')
                    log.info(f"Descompresion de archivo:{file} en lote finalizada")

            for txt_file in os.listdir('lote'):
                patron = re.compile(r'^Lote\d+(.+?)\d+\.txt$')
                banco = patron.match(txt_file)
                
                if banco.group(1) in read_ini('CONFIG', 'BANCOS')[0].keys():
                    log.info(f"Insertando en banco archivo:{txt_file} en lote")
                    for linea in read_txt('lote\\{file}'.format(file=txt_file)):
                        insertDataLote(linea, banco.group(1))        
                    os.remove(f'lote\\{txt_file}')
                    os.remove(f'downloads\\{txt_file[:-4]}.zip')
                    log.info(f"Insercion de archivo:{txt_file} finalizada con éxito")
                else:
                   log.warning(f'Archivo de banco:{banco.group(1)} no encontrado o no configurado')    
        
                
    except FileNotFoundError as e:
        print(e, 'Archivo no encontrado')        


