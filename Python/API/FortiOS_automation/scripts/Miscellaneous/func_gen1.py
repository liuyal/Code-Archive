txt = """Version: FortiGate-101F v7.0.0,build0066,210330 (GA)
Firmware Signature: certified
Virus-DB: 87.00811(2021-07-22 08:26)
Extended DB: 87.00811(2021-07-22 08:25)
AV AI/ML Model: 2.01604(2021-07-22 08:45)
IPS-DB: 6.00741(2015-12-01 02:30)
IPS-ETDB: 0.00000(2001-01-01 00:00)
APP-DB: 6.00741(2015-12-01 02:30)
INDUSTRIAL-DB: 6.00741(2015-12-01 02:30)
IPS Malicious URL Database: 3.00078(2021-07-22 08:46)
Serial-Number: FG101FTK20005517
BIOS version: 05000020
System Part-Number: P24605-04
Log hard disk: Available
Hostname: FG101FTK20005517
Private Encryption: Disable
Operation Mode: NAT
Current virtual domain: root
Max number of virtual domains: 10
Virtual domains status: 2 in NAT mode, 0 in TP mode
Virtual domain configuration: multiple
FIPS-CC mode: disable
Current HA mode: standalone
Branch point: 0066
Release Version Information: GA
System time: Thu Jul 22 10:49:35 2021
Last reboot reason: power cycle

Version: FortiGate-VM64 v7.0.0,build0066,210330 (GA)
Virus-DB: 87.00812(2021-07-22 09:26)
Extended DB: 87.00812(2021-07-22 09:25)
Extreme DB: 1.00000(2018-04-09 18:07)
AV AI/ML Model: 2.01604(2021-07-22 08:45)
IPS-DB: 6.00741(2015-12-01 02:30)
IPS-ETDB: 18.00125(2021-07-22 00:07)
APP-DB: 18.00123(2021-07-20 00:45)
INDUSTRIAL-DB: 18.00123(2021-07-20 00:45)
IPS Malicious URL Database: 3.00078(2021-07-22 08:46)
Serial-Number: FGVM04TM21001957
License Status: Valid
License Expiration Date: 2022-04-08
VM Resources: 2 CPU/4 allowed, 2007 MB RAM
Log hard disk: Available
Hostname: FGVM04TM21001957
Private Encryption: Disable
Operation Mode: NAT
Current virtual domain: root
Max number of virtual domains: 10
Virtual domains status: 3 in NAT mode, 0 in TP mode
Virtual domain configuration: multiple
FIPS-CC mode: disable
Current HA mode: standalone
Branch point: 0066
Release Version Information: GA
FortiOS x86-64: Yes
System time: Thu Jul 22 10:50:03 2021
Last reboot reason: warm reboot

Version: FortiGate-VM64 v7.0.0,build0066,210330 (GA)
Virus-DB: 87.00812(2021-07-22 09:26)
Extended DB: 87.00812(2021-07-22 09:25)
Extreme DB: 1.00000(2018-04-09 18:07)
AV AI/ML Model: 2.01605(2021-07-22 09:45)
IPS-DB: 6.00741(2015-12-01 02:30)
IPS-ETDB: 6.00741(2015-12-01 02:30)
APP-DB: 6.00741(2015-12-01 02:30)
INDUSTRIAL-DB: 6.00741(2015-12-01 02:30)
IPS Malicious URL Database: 3.00078(2021-07-22 08:46)
Serial-Number: FGVM04TM21002381
License Status: Valid
License Expiration Date: 2022-04-23
VM Resources: 2 CPU/4 allowed, 2007 MB RAM
Log hard disk: Available
Hostname: FGVM04TM21002381
Private Encryption: Disable
Operation Mode: NAT
Current virtual domain: root
Max number of virtual domains: 10
Virtual domains status: 2 in NAT mode, 0 in TP mode
Virtual domain configuration: multiple
FIPS-CC mode: disable
Current HA mode: a-p, primary
Cluster uptime: 46 seconds
Cluster state change time: 2021-07-22 10:59:01
Branch point: 0066
Release Version Information: GA
FortiOS x86-64: Yes
System time: Thu Jul 22 10:59:45 2021
Last reboot reason: power cycle

Version: FortiGate-1500D v7.0.0,build0066,210330 (GA)
Virus-DB: 1.00000(2018-04-09 18:07)
Extended DB: 1.00000(2018-04-09 18:07)
Extreme DB: 1.00000(2018-04-09 18:07)
AV AI/ML Model: 2.01209(2021-06-27 02:45)
IPS-DB: 6.00741(2015-12-01 02:30)
IPS-ETDB: 6.00741(2015-12-01 02:30)
APP-DB: 6.00741(2015-12-01 02:30)
INDUSTRIAL-DB: 6.00741(2015-12-01 02:30)
IPS Malicious URL Database: 1.00001(2015-01-01 01:01)
Serial-Number: FG1K5D3I14800678
BIOS version: 04000006
System Part-Number: P12917-05
Log hard disk: Available
Hostname: 1500D-UP
Private Encryption: Disable
Operation Mode: NAT
Current virtual domain: root
Max number of virtual domains: 10
Virtual domains status: 2 in NAT mode, 0 in TP mode
Virtual domain configuration: multiple
FIPS-CC mode: disable
Current HA mode: standalone
Cluster uptime: 2 days, 0 hours, 43 minutes, 20 seconds
Cluster state change time: 2021-07-20 18:12:48
Branch point: 0066
Release Version Information: GA
FortiOS x86-64: Yes
System time: Thu Jul 22 11:27:29 2021
Last reboot reason: warm reboot
"""

item_list = []
item_list2 = []

for item in txt.split('\n'):
    attr = item.split(':')[0].lower().replace(' ', "_").replace('-', "_").replace('/', "_")
    if attr not in item_list and len(item) > 1:
        item_list.append(attr)
        item_list2.append((item.split(':')[0], attr))

for item, attr in item_list2:
    print("self.fgt_status['" + attr + "'] = ''")
    print(repr("self.fgt_get_system_status_helper(sys_status, '" + item + ":', '\n', '" + attr + "')").replace('"',''))
    print()
