from ship import Ship

def create_ship(filename):
    '''Input filename of manifest, parses file contents. Returns ship object.'''
    # https://www.pythontutorial.net/python-basics/python-read-text-file/
    with open(filename) as f:
        contents = [line for line in f.readlines()]
    ret = Ship(contents)
    return ret

if __name__=='__main__':
    create_ship('ShipCase1.txt')