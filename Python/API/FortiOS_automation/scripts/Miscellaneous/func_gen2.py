txt = '''status: up
npu: n
flush: n
asic helper: y
ports: 2
link-up-delay: 50ms
min-links: 1
ha: master
distribution algorithm: L4
LACP mode: passive
LACP speed: slow
LACP HA: enable
aggregator ID: 1
actor key: 17
actor MAC address: 00:0c:29:d4:a4:3e
partner key: 17
partner MAC address: 00:0c:29:5d:15:25
'''

temp = '''
    def get_redundant_<N>(self):
        start_index = self.raw_text.find("<M>:")
        end_index = self.raw_text.find("\ n", start_index)
        if start_index != -1 and end_index != -1:
            self.<N> = self.raw_text[start_index:end_index].split(':')[-1].strip()'''

# for line in list(filter(None, txt.split('\n'))):
#     print("self." + line.split(':')[0].lower().replace(' ', '_').replace('-', '_') + "=''")
#
# for line in list(filter(None, txt.split('\n'))):
#     N = line.split(':')[0].lower().replace(' ', '_').replace('-', '_')
#     M = line.split(':')[0]
#     print(temp.replace('<N>', N).replace('<M>', M))
#
# print()

txt2 = '''index: 0
  link status: up
  link failure count: 0
  permanent MAC addr: 00:0c:29:d4:a4:3e
  LACP state: negotiating
  actor state: PSAIDD
  actor port number/key/priority: 1 17 255
  partner state: ASAOEE
  partner port number/key/priority: 2 17 255
  partner system: 34944 00:0c:29:5d:15:25
  aggregator ID: 1
  speed/duplex: 1000 1
  RX state: CURRENT 6
  MUX state: ATTACHED 3
  '''

temp2 = '''start_index = self.raw_text.find("<M>:")
end_index = self.raw_text.find("\ n", start_index)
if start_index != -1 and end_index != -1:
    slave['<N>'] = self.raw_text[start_index:end_index].split(':')[-1].strip()'''

for line in list(filter(None, txt2.split('\n'))):
    line = line.strip()
    print("slave['" + line.split(':')[0].lower().replace(' ', '_').replace('-', '_') + "']=''")
    N = line.split(':')[0].lower().replace(' ', '_').replace('-', '_').replace('/', '')
    M = line.split(':')[0]
    print(temp2.replace('<N>', N).replace('<M>', M), '\n')
