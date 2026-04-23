#Linux Stop Isolation - nftables
#Stops isolation Linux hosts that are running the new nftables configuration.
#RHEL/CentOS6+
#Rocky/Alma 8+
#Debian 10+
#Ubuntu 18+

import os

os.system("nft flush ruleset")
os.system("nft -f /root/nftables_currentstate")
os.remove("/root/nftables_currentstate")
