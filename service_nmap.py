import nmap

feedback = list()

nm = nmap.PortScanner()


def usenmap(ip: str, port: str):
    nm.scan(ip, port)
    feedback.append(nm.scaninfo())
    feedback.append(nm.all_hosts())
    feedback.append(nm.csv())
    feedback.append(nm[ip].state())
    feedback.append(nm[ip].all_protocols())
    feedback.append(nm[ip]['tcp'].keys())
    feedback.append(nm)
