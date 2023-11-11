
txt = '''
config firewall address
    edit "none"
        set uuid e0c9fb8c-999b-51eb-cf60-54ed14ab6983
        set subnet 0.0.0.0 255.255.255.255
    next
    edit "all"
        set uuid e1c30fa6-999b-51eb-91b3-ffb6c2892d0d
    next
    edit "FIREWALL_AUTH_PORTAL_ADDRESS"
        set uuid e1c311ae-999b-51eb-1c53-e7befca5d60e
    next
    edit "FABRIC_DEVICE"
        set uuid e1c31366-999b-51eb-40f0-2be6a62d8316
        set comment "IPv4 addresses of Fabric Devices."
    next
    edit "SSLVPN_TUNNEL_ADDR1"
        set uuid e1c3b19a-999b-51eb-beeb-136d7c5f6643
        set type iprange
        set start-ip 10.212.134.200
        set end-ip 10.212.134.210
    next
    edit "FCTEMS_ALL_FORTICLOUD_SERVERS"
        set uuid 94f4fec4-9ba7-51eb-acbf-5d2685a0fee6
        set type dynamic
        set sub-type ems-tag
    next
    edit "fctems3938134078_critical"
        set uuid a006f074-06b4-51ec-1d64-618d4cbe482b
        set type dynamic
        set sub-type ems-tag
    next
    edit "mac_fctems3938134078_critical"
        set uuid a0070d02-06b4-51ec-56e8-512a772a209c
        set type dynamic
        set sub-type ems-tag
        set obj-type mac
    next
    edit "fctems3938134078_high"
        set uuid a0071bf8-06b4-51ec-0428-978191ad1a7e
        set type dynamic
        set sub-type ems-tag
    next
    edit "mac_fctems3938134078_high"
        set uuid a0072814-06b4-51ec-abab-0d073b65b382
        set type dynamic
        set sub-type ems-tag
        set obj-type mac
    next
    edit "fctems3938134078_ioc suspicious"
        set uuid a00733e0-06b4-51ec-2960-94d19cf227d7
        set type dynamic
        set sub-type ems-tag
    next
    edit "mac_fctems3938134078_ioc suspicious"
        set uuid a0073f48-06b4-51ec-b72b-de55807d40c5
        set type dynamic
        set sub-type ems-tag
        set obj-type mac
    next
    edit "fctems3938134078_low"
        set uuid a0074ac4-06b4-51ec-ca48-cf8a66e871bc
        set type dynamic
        set sub-type ems-tag
    next
    edit "mac_fctems3938134078_low"
        set uuid a00755be-06b4-51ec-6684-2062bc59678c
        set type dynamic
        set sub-type ems-tag
        set obj-type mac
    next
    edit "fctems3938134078_medium"
        set uuid a0076126-06b4-51ec-0b0b-4d0f361acccf
        set type dynamic
        set sub-type ems-tag
    next
    edit "mac_fctems3938134078_medium"
        set uuid a0076c34-06b4-51ec-8ca2-144a5fa15050
        set type dynamic
        set sub-type ems-tag
        set obj-type mac
    next
    edit "fctems3938134078_test"
        set uuid a0077a4e-06b4-51ec-285f-b0477f53583f
        set type dynamic
        set sub-type ems-tag
    next
    edit "mac_fctems3938134078_test"
        set uuid a00786c4-06b4-51ec-0581-f54250667e2a
        set type dynamic
        set sub-type ems-tag
        set obj-type mac
    next
    edit "fctems3938134078_zero-day detections"
        set uuid a0079286-06b4-51ec-9b4d-a3900fd6a9cb
        set type dynamic
        set sub-type ems-tag
    next
    edit "mac_fctems3938134078_zero-day detections"
        set uuid a0079dda-06b4-51ec-4739-92b821ae757b
        set type dynamic
        set sub-type ems-tag
        set obj-type mac
    next
    edit "fctems3938134078_all_registered_clients"
        set uuid 52718326-0752-51ec-5a51-221928c573b4
        set type dynamic
        set sub-type ems-tag
    next
    edit "mac_fctems3938134078_all_registered_clients"
        set uuid 52719ec4-0752-51ec-99dc-f275ecfc8eac
        set type dynamic
        set sub-type ems-tag
        set obj-type mac
    next
    edit "fctems8821005851_critical"
        set uuid 302eba0c-0768-51ec-cc83-e592e90733da
        set type dynamic
        set sub-type ems-tag
    next
    edit "mac_fctems8821005851_critical"
        set uuid 302ed618-0768-51ec-e54b-05d5a1076349
        set type dynamic
        set sub-type ems-tag
        set obj-type mac
    next
    edit "fctems8821005851_high"
        set uuid 302ee716-0768-51ec-2667-75816e0548fd
        set type dynamic
        set sub-type ems-tag
    next
    edit "mac_fctems8821005851_high"
        set uuid 302ef67a-0768-51ec-8467-a52251028228
        set type dynamic
        set sub-type ems-tag
        set obj-type mac
    next
    edit "fctems8821005851_ioc suspicious"
        set uuid 302f0642-0768-51ec-bbe5-6877d8993d1d
        set type dynamic
        set sub-type ems-tag
    next
    edit "mac_fctems8821005851_ioc suspicious"
        set uuid 302f1538-0768-51ec-6d4d-fe3741bad179
        set type dynamic
        set sub-type ems-tag
        set obj-type mac
    next
    edit "fctems8821005851_low"
        set uuid 302f2528-0768-51ec-f60d-680988462048
        set type dynamic
        set sub-type ems-tag
    next
    edit "mac_fctems8821005851_low"
        set uuid 302f3432-0768-51ec-75e5-c5be7fa357f6
        set type dynamic
        set sub-type ems-tag
        set obj-type mac
    next
    edit "fctems8821005851_medium"
        set uuid 302f4378-0768-51ec-2e7a-25d7e23c79c5
        set type dynamic
        set sub-type ems-tag
    next
    edit "mac_fctems8821005851_medium"
        set uuid 302f5250-0768-51ec-7a82-9b636de08abf
        set type dynamic
        set sub-type ems-tag
        set obj-type mac
    next
    edit "fctems8821005851_test"
        set uuid 302f6484-0768-51ec-340f-ccb4c6f6d615
        set type dynamic
        set sub-type ems-tag
    next
    edit "mac_fctems8821005851_test"
        set uuid 302f75aa-0768-51ec-5a52-d900c91b931b
        set type dynamic
        set sub-type ems-tag
        set obj-type mac
    next
    edit "fctems8821005851_zero-day detections"
        set uuid 302f8568-0768-51ec-7d3d-9bee46093adf
        set type dynamic
        set sub-type ems-tag
    next
    edit "mac_fctems8821005851_zero-day detections"
        set uuid 302f94c2-0768-51ec-d418-6806f7af74f4
        set type dynamic
        set sub-type ems-tag
        set obj-type mac
    next
    edit "fctems8821005851_linux"
        set uuid 49998164-10c0-51ec-0c49-b2616cd43638
        set type dynamic
        set sub-type ems-tag
    next
    edit "mac_fctems8821005851_linux"
        set uuid 4999a16c-10c0-51ec-baa2-3d4500c22324
        set type dynamic
        set sub-type ems-tag
        set obj-type mac
    next
    edit "fctems8821005851_mac"
        set uuid 4999b5ee-10c0-51ec-012c-10e86e0f4c30
        set type dynamic
        set sub-type ems-tag
    next
    edit "mac_fctems8821005851_mac"
        set uuid 4999c778-10c0-51ec-dad8-46f6ec959b09
        set type dynamic
        set sub-type ems-tag
        set obj-type mac
    next
    edit "fctems8821005851_win"
        set uuid 4999db3c-10c0-51ec-13a3-7db9c0a5b2b2
        set type dynamic
        set sub-type ems-tag
    next
    edit "mac_fctems8821005851_win"
        set uuid 4999ebd6-10c0-51ec-f5fc-4afb1fad7a82
        set type dynamic
        set sub-type ems-tag
        set obj-type mac
    next
    edit "fctems8821005851_all_registered_clients"
        set uuid 041e936c-10c6-51ec-c415-33f0cdb325a9
        set type dynamic
        set sub-type ems-tag
    next
    edit "mac_fctems8821005851_all_registered_clients"
        set uuid 041eb496-10c6-51ec-6db4-15eb6cf3e89c
        set type dynamic
        set sub-type ems-tag
        set obj-type mac
    next
    edit "fqdn_test"
        set uuid 00ff0ec4-10de-51ec-f3ce-6f3b4c6201b9
        set type iprange
        set start-ip 20.70.1.1
        set end-ip 20.70.1.150
    next
    edit "fqdn_test2"
        set uuid 7c49f6b6-10de-51ec-1176-8e9e5f1fbd07
        set type fqdn
        set fqdn "*.fortinet.com"
    next
    edit "login.microsoftonline.com"
        set uuid b11ad5ac-10ea-51ec-6d73-7fa9f799ca8e
        set type fqdn
        set fqdn "login.microsoftonline.com"
    next
    edit "login.microsoft.com"
        set uuid c1eaa88a-10ea-51ec-e2a7-a6f453a76f95
        set type fqdn
        set fqdn "login.microsoft.com"
    next
    edit "login.windows.net"
        set uuid c1eb3034-10ea-51ec-f301-224e15005efc
        set type fqdn
        set fqdn "login.windows.net"
    next
    edit "gmail.com"
        set uuid c1ebd94e-10ea-51ec-43cb-e64bfae7ad00
        set type fqdn
        set fqdn "gmail.com"
    next
    edit "wildcard.google.com"
        set uuid c1ec9488-10ea-51ec-46d0-30342053ef9f
        set type fqdn
        set fqdn "*.google.com"
    next
    edit "wildcard.dropbox.com"
        set uuid c1ed4de2-10ea-51ec-fc5f-3ad25cafb523
        set type fqdn
        set fqdn "*.dropbox.com"
    next
end
'''

for line in txt.split('\n'):
    if 'edit' in line:
        print('del ' + line.split('edit')[-1])