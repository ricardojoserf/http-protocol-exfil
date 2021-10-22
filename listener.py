import sys
from http.server import BaseHTTPRequestHandler,HTTPServer
from urllib.parse import urlparse,urlsplit,parse_qs

file_bits = ""
send_data_path = "/"
generate_file_path = "/newfile"
debug = True

# https://stackoverflow.com/questions/32675679/convert-binary-string-to-bytearray-in-python-3
def bitstring_to_bytes(s):
    return int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='big')


def create_file(local_file_name, file_bits):
    file_bytes = bitstring_to_bytes(file_bits)
    f = open(local_file_name, "wb")
    f.write(file_bytes)
    f.close()


class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        global file_bits
        self._set_response()
        if self.path == send_data_path:
            version_digit = self.request_version.replace("HTTP/1.","")
            file_bits += version_digit
        elif self.path.startswith(generate_file_path):
            params = parse_qs(urlsplit(self.path).query)
            if 'f' in params and file_bits != "":
                local_file_name = (params['f'][0])
                create_file(local_file_name, file_bits)
                file_bits = ""

    def do_POST(self):
        self._set_response()

    def log_message(self, format, *args):
        if not debug:
            return


def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()


if __name__ == '__main__':
    if len(sys.argv) == 2:
        run(port=int(sys.argv[1]))
    else:
        run()