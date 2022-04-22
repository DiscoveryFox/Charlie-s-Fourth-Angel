import nmap

feedback = list()

nm = nmap.PortScanner()


# todo: set the path to the nmap directory

def usenmap(ip: str, port: str, json_output: bool = False):
    """
    :param ip: ip address
    :param port: port number
    :param json_output: json output
    :return feedback: dictionary or html like file
    """
    if json_output is True:
        return nm.scan(ip, port)

    result = nm.scan(ip, port)

    # render a html like file which contains the result prettified

    for host in result['scan']:
        for port in result['scan'][host]['tcp']:
            if result['scan'][host]['tcp'][port]['state'] == 'open':
                feedback.append(
                    f'{host}:{port}/{result["scan"][host]["tcp"][port]["name"]}')

    return feedback
