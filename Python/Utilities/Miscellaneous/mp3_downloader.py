import urllib2

files = ["01 - Faith", "02 - Release", "03 - Birdman", "04 - Downtown District", "05 - Noah", "06 - Back in the Game", "07 - Icarus",
         "08 - Plastic", "09 - Savant", "10 - Gridnodes", "11 - Anchor District", "12 - Dogen", "13 - Benefactor", "14 - Raid", "15 - Flytrap",
         "16 - Sanctuary", "17 - Rebecca", "18 - Vive Le Resistance", "19 - Rezoning District", "20 - Aurore", "21 - Prisoner X", "22 - Aline",
         "23 - Kingdom", "24 - Kruger", "25 - Isabel", "26 - Family Matters", "27 - Tickets Please", "28 - The View District", "29 - Caitlyn",
         "30 - The Shard", "31 - Gabriel", "32 - Catalyst"]


for file_name in files:
    try:
        download_url = "http://23.237.126.42/ost/mirror-s-edge-catalyst/xokypvhaue/"+file_name.replace(' ','%20')+".mp3"
        print(download_url)
        response = urllib2.urlopen(download_url)
        file = open(file_name.replace("%20",''), 'wb')
        file.write(response.read())
        file.close()
    except:
        print("Fail")