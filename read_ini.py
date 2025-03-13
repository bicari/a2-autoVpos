import tomllib


def read_ini(section: str, *args, **kwargs):
    try:
        
        with open('config.toml', 'rb') as file:
            data = tomllib.load(file)
        if section.upper() in data.keys() and args:
            config = []
            for arg in args:
                config.append(data[section][arg])
            return config    
        
        elif section.upper() in data.keys() and kwargs:
            for key, value in kwargs.items():
                if value in data[section][key].keys():
                    return data[section][key][value]
              
        else:
            raise Exception("La seccion indicada no pudo ser encontrada el archivo de configuracion")    

    except Exception as e:    
        return e
    
