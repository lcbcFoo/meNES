from collections import namedtuple

#Se pc + 1 for maior ou igual ao tamanho da pagina, passamos
class Absolute():
    def __init__(self):
        AbsoluteADC = namedtuple('6D')
        AbsoluteAND = namedtuple('2D')
        AbsoluteASL = namedtuple('0E')
        AbsoluteBIT = namedtuple('2C')
        AbsoluteCMP = namedtuple('CD')
        AbsoluteCPX = namedtuple('EC')
        AbsoluteCPY = namedtuple('CC')
        AbsoluteDEC = namedtuple('CE')
        AbsoluteEOR = namedtuple('4D')
        AbsoluteINC = namedtuple('EE')
        AbsoluteJMP = namedtuple('4C')
        AbsoluteJSR = namedtuple('20')
        AbsoluteLDA = namedtuple('AD')
        AbsoluteLDX = namedtuple('AE')
        AbsoluteLDY = namedtuple('AC')
        AbsoluteLSR = namedtuple('4E')
        AbsoluteORA = namedtuple('0D')
        AbsoluteROL = namedtuple('2E')
        AbsoluteROR = namedtuple('6E')
        AbsoluteSBC = namedtuple('ED')
        AbsoluteSTA = namedtuple('8D')
        AbsoluteSTX = namedtuple('8E')
        AbsoluteSTY = namedtuple('8C')
}