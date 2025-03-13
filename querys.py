import pyodbc
import os
from datetime import datetime
from read_ini import read_ini
from logs import logger

def insertDataDetalle(linea: list):
    RUTA_A2_DATA = os.environ.get('RUTA_A2')
    BANCOS = read_ini('CONFIG', 'BANCOS')[0]
    CUENTAS_CONTABLES_BANCOS = read_ini('CONFIG', 'BANCOS_CUENTAS_CONTABLES')[0] 
    CUENTA_CAJA = read_ini('CONFIG', 'CAJA')[0]
    CONCEPTO = read_ini('CONFIG', 'CONCEPTO')[0]
    connection = None
    log = logger()
    try:
        connection= pyodbc.connect(r'DSN=A2GKC;CatalogName={a2}'.format(a2=RUTA_A2_DATA))
        cursor = connection.cursor()
        nro_nc = cursor.execute("SELECT NO_COMPROBANTECREDITO FROM SSISTEMA").fetchone()[0]
        trans_banco = f"""INSERT INTO STRANSBANCO (FTB_BANCO, 
                                                     FTB_TIPO, 
                                                     FTB_FECHA, 
                                                     FTB_FECHALIBERACION, 
                                                     FTB_DOCUMENTO, 
                                                     FTB_MONTO,
                                                     FTB_CONCEPTO,
                                                     FTB_NROCOMPROBANTE)
                               VALUES('{BANCOS[linea[7]]}', 
                                        3, 
                                        '{datetime.strptime(linea[2], "%d%m%Y").strftime("%Y-%m-%d")}',
                                        '{datetime.strptime(linea[2], "%d%m%Y").strftime("%Y-%m-%d")}', 
                                        '{linea[6]}', 
                                        {float(linea[12])},
                                        'Detalle:{CONCEPTO}',
                                        '{str(nro_nc).rjust(8,"0")}'

                                        )"""
        linea1 = f"""INSERT INTO STRANSCUENTAS (FE_CODECUENTA, FE_OPERACIONAUTOINC, FE_NOLINEA, FE_BANCOORIGEN, FE_MONTO, FE_TIPOOPERACION, FE_TIPOTRANSACCION, FE_VISIBLE) 
                                    VALUES('{CUENTAS_CONTABLES_BANCOS[linea[7]]}', LASTAUTOINC('STRANSBANCO'), 0, '{BANCOS[linea[7]]}',
                                            {float(linea[12])}, 3, 0, 1)"""
                    
        linea2 = f"""INSERT INTO STRANSCUENTAS (FE_CODECUENTA, FE_OPERACIONAUTOINC, FE_NOLINEA, FE_BANCOORIGEN, FE_MONTO, FE_TIPOOPERACION, FE_TIPOTRANSACCION, FE_VISIBLE) 
                                    VALUES('{CUENTA_CAJA}', LASTAUTOINC('STRANSBANCO'), 1, '{BANCOS[linea[7]]}', 
                                            {float(linea[12])* -1}, 3, 0, 1)"""
        
        update_ssistema = "UPDATE SSISTEMA SET NO_COMPROBANTECREDITO = {nro} WHERE DUMMYKEY = '' ".format(nro= int(nro_nc) + 1 )
        querys = [trans_banco, linea1, linea2, update_ssistema]
        for query in querys:
            cursor.execute(query)
        #filter(lambda query: cursor.execute(query), querys)
        cursor.commit()
             
            
    except Exception as e:
        log.error(str(e))
        if connection:
            connection.rollback()   
    finally:
        if connection:
            connection.close()     

def insertDataLote(linea: list, banco: str):
    RUTA_A2_DATA = os.environ.get('RUTA_A2')
    BANCOS = read_ini('CONFIG', 'BANCOS')[0]
    CUENTAS_CONTABLES_BANCOS = read_ini('CONFIG', 'BANCOS_CUENTAS_CONTABLES')[0] 
    CUENTA_CAJA = read_ini('CONFIG', 'CAJA')[0]
    CONCEPTO = read_ini('CONFIG', 'CONCEPTO')[0]
    connection = None
    log = logger()
    try:
        connection= pyodbc.connect(r'DSN=A2GKC;CatalogName={a2}'.format(a2=RUTA_A2_DATA))
        cursor = connection.cursor()
        nro_nc = cursor.execute("SELECT NO_COMPROBANTECREDITO FROM SSISTEMA").fetchone()[0]
        trans_banco = f"""INSERT INTO STRANSBANCO (FTB_BANCO, 
                                                     FTB_TIPO, 
                                                     FTB_FECHA, 
                                                     FTB_FECHALIBERACION, 
                                                     FTB_DOCUMENTO, 
                                                     FTB_MONTO,
                                                     FTB_CONCEPTO,
                                                     FTB_FACTORORIGINAL,
                                                     FTB_IMPUESTO,
                                                     FTB_ORIGENBENEFICIARIO,
                                                     FTB_NROCOMPROBANTE,
                                                     FTB_MONEDAORIGINAL,
                                                     FTB_CONTABILIZADO,
                                                     FTB_HORAOPERACION)
                               VALUES('{BANCOS[banco]}', 
                                        3, 
                                        '{datetime.strptime(linea[3], "%d%m%Y").strftime("%Y-%m-%d")}',
                                        '{datetime.strptime(linea[3], "%d%m%Y").strftime("%Y-%m-%d")}', 
                                        '{str(nro_nc).rjust(8, "0")}', 
                                        {float(linea[6])},
                                        'Lote:{CONCEPTO}',
                                        1,
                                        0,
                                        0,
                                        '{str(nro_nc).rjust(8, "0")}',
                                        '1',
                                        0,
                                        '{datetime.time(datetime.now()).isoformat('seconds')}' 

                                        )"""
        linea1 = f"""INSERT INTO STRANSCUENTAS (FE_CODECUENTA, 
                                                FE_OPERACIONAUTOINC, 
                                                FE_NOLINEA, 
                                                FE_BANCOORIGEN, 
                                                FE_MONTO, 
                                                FE_TIPOOPERACION, 
                                                FE_TIPOTRANSACCION, 
                                                FE_VISIBLE) 
                                    VALUES('{CUENTAS_CONTABLES_BANCOS[banco]}', 
                                            LASTAUTOINC('STRANSBANCO'), 
                                            0, 
                                            '{BANCOS[banco]}',
                                            {float(linea[6])}, 
                                            3, 
                                            0, 
                                            1)"""
                    
        linea2 = f"""INSERT INTO STRANSCUENTAS (FE_CODECUENTA, 
                                                FE_OPERACIONAUTOINC, 
                                                FE_NOLINEA, 
                                                FE_BANCOORIGEN, 
                                                FE_MONTO, 
                                                FE_TIPOOPERACION, 
                                                FE_TIPOTRANSACCION, 
                                                FE_VISIBLE) 
                                    VALUES('{CUENTA_CAJA}', 
                                            LASTAUTOINC('STRANSBANCO'), 
                                            1, 
                                            '{BANCOS[banco]}', 
                                            {float(linea[6])* -1}, 
                                            3, 
                                            0, 
                                            1)"""
        update_ssistema = "UPDATE SSISTEMA SET NO_COMPROBANTECREDITO = {nro} WHERE DUMMYKEY = '' ".format(nro= int(nro_nc) + 1 )
        querys = [trans_banco, linea1, linea2, update_ssistema]
        for query in querys:
            cursor.execute(query)
        #filter(lambda query: cursor.execute(query), querys)
        cursor.commit()
        
             
            
    except Exception as e:
        log.error(str(e))
        if connection:
            connection.rollback()   
    finally:
        if connection:
            connection.close()     