###Find all devices on the IP_RANGE and print IP, MAC, and hostname
from scapy.all import ARP, Ether, srp
import socket

target_ip = "{{ .IP_RANGE }}"
arp = ARP(pdst=target_ip)
ether = Ether(dst="ff:ff:ff:ff:ff:ff")
packet = ether / arp

result = srp(packet, timeout=3, verbose=0)[0]

clients = []

for sent, received in result:
    ip = received.psrc
    mac = received.hwsrc
    try:
        hostname = socket.gethostbyaddr(ip)[0]
    except socket.herror:
        hostname = "N/A"
    clients.append({'ip': ip, 'mac': mac, 'hostname': hostname})

print("Found devices on the network:")
print("{:<16} {:<20} {}".format("IP", "MAC", "HOSTNAME"))
for client in clients:
    print("{:<16} {:<20} {}".format(client['ip'], client['mac'], client['hostname']))
