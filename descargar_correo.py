import imaplib
import email
import os
import time
from read_ini import read_ini
from email.header import decode_header
from logs import logger
import re
# 📌 Configuración de Gmail


def download_mail():

    IMAP_SERVER = "imap.gmail.com"
    USER = read_ini('CONFIG', 'MAIL')[0]
    PASSWORD = read_ini('CONFIG', 'PASSWORD')[0]
    FORMA_OPERACION =  read_ini('CONFIG', 'DETALLAR_OPERACIONES')[0]
    log = logger()
   
    DOWNLOAD_FOLDER = "downloads"
    if not os.path.exists(DOWNLOAD_FOLDER):
        os.makedirs(DOWNLOAD_FOLDER)

    PATRON_DETALLE = re.compile(r"^Conciliacion Merchant - Archivo:Detalle1964.*", re.IGNORECASE)
    PATRON_LOTE = re.compile(r"^Conciliacion Merchant - Archivo:Lote1964.*", re.IGNORECASE)
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(USER, PASSWORD)
        mail.select("inbox")  # Seleccionar la bandeja de entrada
    except imaplib.IMAP4.error as e:
        log.error(e)   
        time.sleep(15)
   
    status, email_ids = mail.search(None, 'UNSEEN')
    email_ids = email_ids[0].split()
    print('largo emails',len(email_ids))

    for e_id in email_ids:
        status, msg_data = mail.fetch(e_id, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)
        
    # Decodificar el asunto del correo
        subject = decode_header(msg["Subject"])[0][0]
        if isinstance(subject, bytes):
            subject = subject.decode()

    # Verificar si el asunto coincide con la expresión regular
        if FORMA_OPERACION:
            if PATRON_DETALLE.match(subject):
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        for part in msg.walk():
                            filename = part.get_filename()
                            if filename and filename.endswith(".zip"):
                                file_path = os.path.join(DOWNLOAD_FOLDER, filename)
                                with open(file_path , 'wb') as file:
                                    file.write(part.get_payload(decode=True))
                                log.info(f'Archivo guardado {file_path}')
                log.info(f'Descarga finalizada')                   
            else:
                log.warning(f'El asunto {subject} no coincide con la expresión {PATRON_DETALLE}') 
                
        else:
            if PATRON_LOTE.match(subject):
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        for part in msg.walk():
                            filename = part.get_filename()
                            if filename and filename.endswith(".zip"):
                                file_path = os.path.join(DOWNLOAD_FOLDER, filename)
                                with open(file_path , 'wb') as file:
                                    file.write(part.get_payload(decode=True))
                                log.info(f'Archivo guardado {file_path}')   
                log.info(f'Descarga finalizada')                
            else:
               log.warning(f'El asunto {subject} no coincide con la expresión {PATRON_LOTE}')   
    

    # 📤 Cerrar sesión
    mail.logout()
    return True

