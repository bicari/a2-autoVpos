
def read_txt(path: str):
    with open(path, 'r') as file:
      for linea in file:
        if linea:
          data_list = linea.split(",")    
          yield [linea.replace('"', '') for linea in data_list]

          
# total_tc = 0
# total_td = 0

# for linea in read_txt(r'C:\Proyectos\Python\bot-vpos\downloads\Detalle1964Bancamiga20250203.txt'):
#     if linea[8] == '"TC"':
#        monto_linea = linea[12].strip('"')
#        print(monto_linea)
#        total_tc += float(monto_linea)
#     if linea[8] == '"TD"':
#        monto_linea = linea[12].strip('"')
#        total_td += float(monto_linea )
