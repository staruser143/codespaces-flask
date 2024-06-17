from http.server import SimpleHTTPRequestHandler
import socketserver

PORT = 8051

Handler = SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()