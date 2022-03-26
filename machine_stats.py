import psutil
import getip


# get cpu usage in percentage
def get_cpu_usage():
    return psutil.cpu_percent(interval=1)


# get cpu usage in percentage

# get memory usage in percentage
def get_memory_usage():
    return psutil.virtual_memory( ).percent


# available memory in megabytes rounded to 2 decimal places
def get_available_memory():
    return round(psutil.virtual_memory( ).available / 1024 / 1024, 0)


# get disk usage in percentage
def get_disk_usage():
    return psutil.disk_usage('/').percent


# get network usage in percentage round to 2 decimal places
def get_network_usage():
    return round(psutil.net_io_counters( ).bytes_sent / 1024 / 1024, 2)


def get_bandwith_usage():
    return round(psutil.net_io_counters( ).bytes_sent / 1024 / 1024, 2)


# get all stats
def get_stats():
    return {
        'cpu_usage': get_cpu_usage( ),
        'memory_usage': get_memory_usage( ),
        'available_memory': get_available_memory( ),
        'disk_usage': get_disk_usage( ),
        'network_usage': get_network_usage( ),
        'ip_address': getip.getip( ),
        'bandwith_usage': get_bandwith_usage( )
    }


print(get_stats( ))
