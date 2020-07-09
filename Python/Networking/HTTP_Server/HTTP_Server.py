import os, sys, time, datetime
import socket, socketserver, requests
import http.server


class HTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.wfile.write(b"<html><head><title>HTTP_Server</title></head><body>")
        self.wfile.write(b"<p>Path: " + self.path.encode('utf-8') + b"</p>")
        self.wfile.write(b"</body></html>")

    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_PUT(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_DELETE(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_COPY(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_PURGE(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
    

def get_ip_address():
    public_ip = requests.get("https://api.ipify.org?format=json").json()["ip"]
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(("8.8.8.8", 80))
    private_ip = sock.getsockname()[0]
    return private_ip, public_ip


def runServer(HostIP="0.0.0.0", HostPort=8080, handler=HTTPRequestHandler):
    print("HTTP Server Hosted at: " + HostIP + ":" + str(HostPort))
    server_class = http.server.HTTPServer
    httpd = server_class((HostIP, HostPort), handler)
    httpd.serve_forever()


if __name__ == "__main__":


    runServer()
