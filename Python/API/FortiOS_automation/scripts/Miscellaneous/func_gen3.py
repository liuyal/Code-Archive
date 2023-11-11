
txt = """dev=1 attached=0 tunnel=2 proxyid=1 sa=1 conc=0 up=1 fenc=0 fdec=0 fasm=0 crypto_work=0 crypto_work_dropped=0
mr_grps=0 mr_children=0 mr_flood_list=0 mr_fw_list=0"""

temp = """def get_tunnel_stat_<M>(self):
    start_index = self.raw_text.find("<M>=")
    end_index = self.raw_text.find(" ", start_index)
    if start_index != -1 and end_index != -1:
        self.<M> = self.raw_text[start_index + len("<M>="):end_index]
"""


# for item in txt.split(): print("self." + item.split('=')[0].strip() + "=-1")


for item in txt.split():

    print(temp.replace("<M>",item.split('=')[0].strip()))