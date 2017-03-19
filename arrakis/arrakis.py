# Funzioni di utilita' per project-arrakis

def parseInput(input, delimiter='|'):
    """Parsing dell'input dalla lettura sensori"""
    return input.split(delimiter)

def dictInput(input, delimiter='|'):
    tokens = parseInput(input, delimiter)
    dataRead = dict()
    dataRead['device']=tokens[0]
    dataRead['deviceType']=tokens[1]
    dataRead['sensor']=tokens[2]
    dataRead['sensorType']=tokens[3]
    dataRead['value']=tokens[4]
    return dataRead
