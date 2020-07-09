import urllib2

file_name = "demo.pdf"

# for i in range(1,26):
#     try:
#         download_url = "http://www2.ensc.sfu.ca/~whitmore/courses/ensc305/projects/2016/"+str(i)+file_name
#         print download_url
#         response = urllib2.urlopen(download_url)
#         file = open(str(i)+file_name, 'wb')
#         file.write(response.read())
#         file.close()
#     except:
#         print("Fail")

# download_url = "http://www2.ensc.sfu.ca/~whitmore/courses/ensc305/projects/2017/a"+file_name
# response = urllib2.urlopen(download_url)
# file = open("a"+file_name, 'wb')
# file.write(response.read())
# file.close()
#
# download_url = "http://www2.ensc.sfu.ca/~whitmore/courses/ensc305/projects/2017/b"+file_name
# response = urllib2.urlopen(download_url)
# file = open("b"+file_name, 'wb')
# file.write(response.read())
# file.close()
#
#
# download_url = "http://www2.ensc.sfu.ca/~whitmore/courses/ensc305/projects/2017/c"+file_name
# response = urllib2.urlopen(download_url)
# file = open("c"+file_name, 'wb')
# file.write(response.read())
# file.close()
print("Completed")