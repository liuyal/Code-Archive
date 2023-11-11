txt = '''session info: proto=17 proto_state=01 duration=101 expire=553 timeout=600 flags=00000000 socktype=0 sockport=0 av_idx=0 use=3
origin-shaper=
reply-shaper=
per_ip_shaper=
class_id=0 ha_id=1:0 policy_dir=0 tunnel=/hub_0 vlan_cos=0/255
state=may_dirty npu synced
statistic(bytes/packets/allow_err): org=60/2/1 reply=60/2/1 tuples=2
tx speed(Bps/kbps): 0/0 rx speed(Bps/kbps): 0/0
orgin->sink: org pre->post, reply pre->post dev=18->8/8->18 gwy=10.100.1.2/10.0.1.1
hook=pre dir=org act=noop 10.1.1.10:58424->12.1.1.10:9996(0.0.0.0:0)
hook=post dir=reply act=noop 12.1.1.10:9996->10.1.1.10:58424(0.0.0.0:0)
misc=0 policy_id=1 auth_info=0 chk_client_info=0 vd=1
serial=00007d2a tos=ff/ff app_list=0 app=0 url_cat=0
sdwan_mbr_seq=0 sdwan_service_id=0
rpdb_link_id=00000000 rpdb_svc_id=0 ngfwid=n/a
npu_state=0x2040001 no_offload
total session 1'''

func_temp = '''def get_session_AAA(self):
    start_index = self.raw_text.find("AAA=")
    end_index = self.raw_text.find(' ', start_index)
    if start_index != -1 and end_index != -1:
        self.AAA = self.raw_text[start_index:end_index].split('=')[-1]'''

txt2='''if=mgmt1 family=00 type=1 index=4 mtu=1500 link=0 master=0
ref=54 state=start present fw_flags=0 flags=up broadcast run multicast
Qdisc=mq hw_addr=e0:23:ff:33:10:96 broadcast_addr=ff:ff:ff:ff:ff:ff
stat: rxp=28233 txp=13433 rxb=4699731 txb=10165101 rxe=0 txe=0 rxd=0 txd=0 mc=1575 collision=0 @ time=1623951101
re: rxl=0 rxo=0 rxc=0 rxf=0 rxfi=0 rxm=0
te: txa=0 txc=0 txfi=0 txh=0 txw=0
misc rxc=0 txc=0
input_type=0 state=3 arp_entry=0 refcnt=54
'''

func_temp2 = '''def get_netlink_interface_AAA(self):
    start_index = self.raw_text.find("AAA=")
    end_index = self.raw_text.find(' ', start_index)
    if start_index != -1 and end_index != -1:
        self.AAA = self.raw_text[start_index:end_index].split('=')[-1]'''

def gen_function_member():
    for line in txt.split('\n'):
        if "hook" not in line and "orgin->sink" not in line:
            for word in line.split(' '):
                if '=' in word:
                    print()
                    print(func_temp.replace("AAA", word.split('=')[0]))
        else:
            if "orgin->sink" in line:
                for word in line.split(' '):
                    if '=' in word:
                        print()
                        print(func_temp.replace("AAA", word.split('=')[0]))
            elif "hook" in line:
                x = 1

    for line in txt.split('\n'):
        if "hook" not in line and "orgin->sink" not in line:
            for word in line.split(' '):
                if '=' in word:
                    print("self." + word.split('=')[0] + "=''")
        else:
            if "orgin->sink" in line:
                for word in line.split(' '):
                    if '=' in word:
                        print("self." + word.split('=')[0] + "=''")
            elif "hook" in line:
                x = 1

def gen_func_2():
    for line in txt2.split('\n'):
        for word in line.split(' '):
            if '=' in word:
                print()
                print(func_temp2.replace("AAA", word.split('=')[0]))

    for line in txt2.split('\n'):
        for word in line.split(' '):
            if '=' in word:
                print("self." + word.split('=')[0] + "=''")

if __name__ == "__main__":
    gen_function_member()
    gen_func_2()
