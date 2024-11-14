# https_server.py
import http.server
import ssl

server_address = ('0.0.0.0', 8000)
handler = http.server.SimpleHTTPRequestHandler
httpd = http.server.HTTPServer(server_address, handler)

# Create an SSL context
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')

# Wrap the server's socket with SSL
httpd.socket = ssl_context.wrap_socket(httpd.socket, server_side=True)

print("Serving on https://0.0.0.0:8000")
httpd.serve_forever()

