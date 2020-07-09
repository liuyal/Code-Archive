import requests, http, random, time

response = requests.get('http://192.168.14.31:9191')

url = r'https://www.google.com/'
response = requests.get(url)
print(response.status_code)
if response.status_code == 200: print('Success!')
elif response.status_code == 404: print('Not Found.')
print(response.content)


r = requests.get(url,params="")

rand_sleep = random.randint(15*60, 30*60)
print("Sleep for " + str(rand_sleep/60) + " mintues")
time.sleep(rand_sleep)

print(rand_sleep)