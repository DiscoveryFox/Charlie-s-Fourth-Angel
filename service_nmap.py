import nmap
import dominate
import dominate.tags

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

    # create a dominate document
    doc = dominate.tags.div()
    # add the dpi as

    return feedback
