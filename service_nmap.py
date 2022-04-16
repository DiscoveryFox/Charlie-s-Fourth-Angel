import nmap

feedback = list()

nm = nmap.PortScanner()


# todo: set the path to the nmap directory

def usenmap(ip: str, port: str):
    return nm.scan(ip, port)
