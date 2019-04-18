import struct
import sys
import socket
import subprocess


def with_dots(arr):
    arr = str(arr[0]) + '.' + str(arr[1]) + '.' + str(arr[2]) + '.' + str(arr[3])
    return arr


def ip_is_private(ip_address):
    if ip_address[0] == '10' or (ip_address[0] == '192' and ip_address[1] == '168') or (
            ip_address[0] == '172' and '16' <= ip_address[1] <= '31'):
        return True
    else:
        return False


def klasa_ip(network_address):
    if network_address[0] == 0:
        return "A"
    elif network_address[1] == 0:
        return "B"
    elif network_address[2] == 0:
        return "C"
    elif network_address[3] == 0:
        return "D"
    else:
        return "E"


def cidr_to_netmask(cidr):
    host_bits = 32 - int(cidr)
    netmask = socket.inet_ntoa(struct.pack('!I', (1 << 32) - (1 << host_bits)))
    return netmask


def get_mask(ip):
    config = subprocess.Popen('ipconfig', stdout=subprocess.PIPE)
    while True:
        line = config.stdout.readline()
        if ip.encode() in line:
            break
    ip_mask = config.stdout.readline().split(b':')[-1].replace(b' ', b'').decode()
    return ip_mask


def dec_to_bin(tab):
    i = 0
    for x in tab:
        tab[i] = bin(x)[2:].zfill(8)
        i += 1
    return tab


def split_octets(tab):
    tab_list = []
    for j in range(0, len(tab)):
        for i in range(0, len(tab[j])):
            tab_list.append(tab[j][i])
            i += 1
        j += 1
    return tab_list


def to_octets(tab_list):
    tab = ["", "", "", ""]
    for j in range(0, 8):
        tab[0] += str(tab_list[j])
    for j in range(8, 16):
        tab[1] += str(tab_list[j])
    for j in range(16, 24):
        tab[2] += str(tab_list[j])
    for j in range(24, 32):
        tab[3] += str(tab_list[j])
    return tab


def binary_to_decimal(binary_arr):
    dec_arr = [int(binary_arr[0], 2), int(binary_arr[1], 2), int(binary_arr[2], 2), int(binary_arr[3], 2)]
    return dec_arr;


def negation(arr):
    neg_array = list()
    for x in arr:
        if x == '0':
            neg_array.append('1')
        else:
            neg_array.append('0')
    return neg_array


# WCZYTYWANIE IP

data = ['', '']
if len(sys.argv) == 1:
    data[0] = socket.gethostbyname(socket.gethostname())
    ip = data[0].split(".")
    data[1] = get_mask(data[0])[:-2]
    mask = data[1].split(".")
    arg = data[0] + '/' + data[1]
else:
    data = str(sys.argv[1])
    data = data.split("/")
    ip = data[0].split(".")
    mask = data[1].split(".")
    arg = str(sys.argv[1])

file = open("calc_result.txt", 'w')
print(f'Argument:  {arg}\n')
file.write(f'Argument: {arg}\n')

# IP TO BIN
try:
    i = 0
    for x in ip:
        ip[i] = int(x)
        i += 1
except ValueError:
    print("Valid ip")
    sys.exit()

if len(sys.argv) != 1:
    if len(ip) != 4 or len(mask) != 1:
        print("valid input")
        sys.exit()
    mask[0] = int(mask[0])
    for x in ip:
        if x < 0 or 255 < x:
            print("valid input")
            sys.exit()
    if mask[0] < 0 or mask[0] > 24:
        print("valid input")
        sys.exit()

# Private/Public
if ip_is_private(ip):
    print("IP is private")
    file.write("IP is private")
else:
    print("IP is public")
    file.write("IP is public")

ip = dec_to_bin(ip)
if len(mask) == 1:
    mask = cidr_to_netmask(mask[0])
    mask = mask.split(".")
print(f"\nMask decimal: {with_dots(mask)}")
file.write(f"\nMask decimal: {with_dots(mask)}")

i = 0
for x in mask:
    mask[i] = int(x)
    i += 1
mask = dec_to_bin(mask)

print(f"Mask binary:{with_dots(mask)}\n")
file.write(f"\nMask binary: {with_dots(mask)}\n")

print(f"IP binary:{with_dots(ip)}")
file.write(f"IP binary:{with_dots(ip)}\n ")

print(f"IP decimal:{data[0]}")
file.write(f"IP decimal:{data[0]} ")

# OCTETS TO CHAR
ip_list = split_octets(ip)
mask_list = split_octets(mask)

# NETWORK
network = []
for x, y in zip(ip_list, mask_list):
    network.append(int(x, 2) & int(y, 2))

network_octets = to_octets(network)
network_decimal = binary_to_decimal(network_octets)
print(f"\nNetwork binary:{with_dots(network_octets)}")
file.write(f"\nNetwork binary:{with_dots(network_octets)} ")

print(f"Network decimal: {with_dots(network_decimal)}")
file.write(f"Network decimal: {with_dots(network_decimal)}")

# KLASA IP

print(f"Network class: {klasa_ip(network)}")
file.write(f"\nNetwork class: {klasa_ip(network)}")

# BROADCAST
broadcast = []
for x, y in zip(ip_list, negation(mask_list)):
    broadcast.append(int(x) | int(y))

print(f"\nBroadcast binary: {with_dots(to_octets(broadcast))}")
file.write(f"\n\nBroadcast binary: {with_dots(to_octets(broadcast))}")
print(f"Broadcast decimal: {with_dots(binary_to_decimal(to_octets(broadcast)))}")
file.write(f"\nBroadcast decimal: {with_dots(binary_to_decimal(to_octets(broadcast)))}")

# FIRST HOST
first_host = network
if first_host[-1] == 0:
    first_host[-1] = 1
else:
    first_host[-1] = 0

# LAST HOST
last = broadcast
if last[-1] == 0:
    last[-1] = 1
else:
    last[-1] = 0

first_host = to_octets(first_host)
last = to_octets(last)
dd = to_octets(broadcast)

print(f"\nFirst host binary:{with_dots(first_host)}")
file.write(f"\nFirst host binary: {with_dots(first_host)}")

print(f"First host decimal:{with_dots(binary_to_decimal(first_host))}")
file.write(f"\nFirst host decimal:{with_dots(binary_to_decimal(first_host))}")

print(f"\nLast host binary:{with_dots(last)}")
file.write(f"\nLast host binary:{str(last)}")

print(f"Last host decimal:{with_dots(binary_to_decimal(last))}")
file.write(f"\nLast host decimal: {with_dots(binary_to_decimal(last))}")

# MAX HOSTS
hosts = binary_to_decimal(last)[3] - binary_to_decimal(first_host)[3] + 1

print(f"\nMax hosts: {hosts}")
file.write(f"\nMax hosts: {hosts}")

file.close()

# PING
ip_host = data[0].split('.')

if int(first_host[3], 2) <= int(ip_host[3]) <= int(last[3], 2):
    ping_choose = input("Do you want to ping this IP? (y=yes, n=no): ")
    ping_choose = ping_choose.upper()
    if ping_choose == 'Y':
        command = ['ping', data[0]]
        subprocess.call(command)
