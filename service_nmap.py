import re
from pprint import pprint

import nmap
import dominate
import dominate.tags
import socket

import typing  # todo: remove this with typing.Union() and replace it with the |(pipe) operator.

feedback = list()

nm = nmap.PortScanner()


# todo: set the path to the nmap directory

def get_ip(ip):
    """
    :param ip: ip address
    :return: ip address
    """
    try:
        socket.inet_aton(ip)
        return ip
    except socket.error:
        return socket.gethostbyname(ip)


# noinspection PyGlobalUndefined
def usenmap(ip: str, port: typing.Union[str, list] = None, json_output: bool = False):
    """
    :param ip: ip address
    :param port: port number
    :param json_output: json output
    :return feedback: dictionary or html like file
    """
    global right_ip

    ipv4_regex = re.compile(
        r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$")

    ipv6_regex = re.compile(
        r"(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))")

    # check if only one port is given or if the port is a range
    if port is list:
        single_port = False
    else:
        single_port = True

    if json_output is True:
        if not port:
            return nm.scan(ip, port)
        else:
            return nm.scan(ip)

    if ipv6_regex.match(ip):
        result = nm.scan(ip, port, arguments='-6')
    else:
        result = nm.scan(ip, port)

    # if ip is not a valid ip address print("Invalid IP address")
    # use regex to check if ip is valid.
    # an ip should look like this:
    # xxx.xxx.xxx.xxx
    # xxx is a number between 0 and 255
    # xxx.xxx.xxx.xxx is a valid ip address
    # if ip is not valid print("Invalid IP address")

    # create a regex pattern for an ipv6 address
    # and ipv6 address looks like this:
    # xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx
    # xxxx is a number between 0 and 65535 it can contain chars
    # xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx is a valid ipv6 address

    if not ipv4_regex.match(ip) and not ipv6_regex.match(ip):
        ip = get_ip(ip)

    # create a dominate document
    gdoc = dominate.tags.div()
    doc = dominate.tags.div(cls='popup')
    doc.add(dominate.tags.a('×', href='#', cls='close'))

    if result['nmap']['scanstats']['downhosts'] == '1':
        doc.add(dominate.tags.h2(f'Nmap scan results for {ip}'))
        doc.add(dominate.tags.p(f'Host is down no scan available.'))
        gdoc.add(doc)
        return {"content": gdoc.render()}

    doc.add(dominate.tags.h2(f'Nmap scan results for '
                             f'{result["scan"][ip]["addresses"]["ipv4"]}'))
    try:
        doc.add(dominate.tags.p(f'Hostname: {result["scan"][ip]["hostnames"][0]["name"]}'))
        doc.add(dominate.tags.p(f'Type: {result["scan"][ip]["hostnames"][0]["type"]}'))
        # doc.add(dominate.tags.p(f'Hostname of target: {socket.gethostbyaddr(ip)[0]} '))
    except Exception as e:
        print(e.__traceback__.tb_frame.f_globals["__file__"])
        doc.add(dominate.tags.p(f'Target IP: {ip}'))

    doc.add(dominate.tags.p(f'Time to scan: {result["nmap"]["scanstats"]["elapsed"]}s'))
    doc.add(dominate.tags.p(f'Date of scan: {result["nmap"]["scanstats"]["timestr"]}'))
    if single_port is True:
        doc.add(dominate.tags.p(f'Server: {result["scan"][ip]["status"]["state"]}'))
        doc.add(dominate.tags.p(f'Method to check Server: {result["scan"][ip]["status"]["reason"]}'))
        doc.add(dominate.tags.p(f'Port {port} is {result["scan"][ip]["tcp"][int(port)]["state"]}'))
        doc.add(dominate.tags.p(f'Reason: {result["scan"][ip]["tcp"][int(port)]["reason"]}'))
        doc.add(dominate.tags.p(f'Service: {result["scan"][ip]["tcp"][int(port)]["name"]}'))
        if result["scan"][ip]["tcp"][int(port)]["product"]:
            doc.add(dominate.tags.p(f'Product: {result["scan"][ip]["tcp"][int(port)]["product"]}'))
        if result["scan"][ip]["tcp"][int(port)]["version"]:
            doc.add(dominate.tags.p(f'Version: {result["scan"][ip]["tcp"][int(port)]["version"]}'))
        if result["scan"][ip]["tcp"][int(port)]["extrainfo"]:
            doc.add(dominate.tags.p(f'Extra Info: {result["scan"][ip]["tcp"][int(port)]["extrainfo"]}'))
        if result["scan"][ip]["tcp"][int(port)]["cpe"]:
            doc.add(dominate.tags.p(f'CPE: {result["scan"][ip]["tcp"][int(port)]["cpe"]}'))
    else:
        for singled_port in port:
            doc.add(dominate.tags.p(
                f'Port: {singled_port} is {result["scan"][ip]["tcp"][int(singled_port)]["state"]}'))
    gdoc.add(doc)
    return {"content": gdoc.render()}


def main():
    pprint(usenmap('8.8.8.8', '22'))


if __name__ == '__main__':
    main()
