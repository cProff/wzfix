import configparser

DEFAULT_SETTINGS = {'wzfolder': '', 'silence': 0}
SETTINGS = DEFAULT_SETTINGS

def save():
    config = configparser.ConfigParser()
    config['SETTINGS'] = SETTINGS
    with open('params.ini', 'w') as configfile:
        config.write(configfile)

def load():
    global SETTINGS
    res = DEFAULT_SETTINGS
    config = configparser.ConfigParser()
    try:
        config.read('params.ini')
        res.update(config['SETTINGS'])
        res['silence'] = int(res['silence'])
        SETTINGS.update(res)
    except Exception as e:
        print(e)
    return  res

def set_param(key, value):
    global SETTINGS
    if type(value) is bool:
        SETTINGS[key] = int(value)
    else:
        SETTINGS[key] = value
    save()