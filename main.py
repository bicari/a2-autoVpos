from descargar_correo import download_mail
from insert_data import insert_data_bank



def entry_main():
    

    result = download_mail()
    if result :
        insert_data_bank()


if __name__ == '__main__':
    entry_main()