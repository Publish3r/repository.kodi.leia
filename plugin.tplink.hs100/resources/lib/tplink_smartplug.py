#!/usr/bin/python

import socket
import argparse
from struct import pack

version = 0.2

# Check if hostname is valid
def validHostname(hostname):
	try:
		socket.gethostbyname(hostname)
	except socket.error:
		parser.error("Invalid hostname.")
	return hostname

# Check if port is valid
def validPort(port):
        try:
            port = int(port)
        except ValueError:
            parser.error("Invalid port number.")

        if ((port <= 1024) or (port >65535)) :
            parser.error("Invalid port number.")

        return port


# Predefined Smart Plug Commands
# For a full list of commands, consult tplink_commands.txt
commands = {		'info'     : '{"system":{"get_sysinfo":{}}}',
			'on'       : '{"system":{"set_relay_state":{"state":1}}}',
			'off'      : '{"system":{"set_relay_state":{"state":0}}}',
	        	'ledoff'   : '{"system":{"set_led_off":{"off":1}}}',
			'ledon'    : '{"system":{"set_led_off":{"off":0}}}',
			'cloudinfo': '{"cnCloud":{"get_info":{}}}',
			'wlanscan' : '{"netif":{"get_scaninfo":{"refresh":0}}}',
			'time'     : '{"time":{"get_time":{}}}',
			'schedule' : '{"schedule":{"get_rules":{}}}',
			'countdown': '{"count_down":{"get_rules":{}}}',
			'antitheft': '{"anti_theft":{"get_rules":{}}}',
			'reboot'   : '{"system":{"reboot":{"delay":1}}}',
			'reset'    : '{"system":{"reset":{"delay":1}}}',
			'energy'   : '{"emeter":{"get_realtime":{}}}'
}

# Encryption and Decryption of TP-Link Smart Home Protocol
# XOR Autokey Cipher with starting key = 171
def encrypt(string):
	key = 171
	result = pack('>I', len(string))
	for i in string:
		a = key ^ ord(i)
		key = a
		result += chr(a)
	return result

def decrypt(string):
	key = 171
	result = ""
	for i in string:
		a = key ^ ord(i)
		key = ord(i)
		result += chr(a)
	return result

# Parse commandline arguments
parser = argparse.ArgumentParser(description="TP-Link Wi-Fi Smart Plug Client v" + str(version))
parser.add_argument("-t", "--target", metavar="<hostname>", required=True, help="Target hostname or IP address", type=validHostname)
parser.add_argument("-p", "--port", metavar="<port>", default=9999, required=False, help="Target port", type=validPort)
parser.add_argument("-q", "--quiet", dest='quiet', action='store_true', help="Only show result")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-c", "--command", metavar="<command>", help="Preset command to send. Choices are: "+", ".join(commands), choices=commands)
group.add_argument("-j", "--json", metavar="<JSON string>", help="Full JSON string of command to send")
args = parser.parse_args()


# Set target IP, port and command to send
ip = args.target
port = args.port
if args.command is None:
	cmd = args.json
else:
	cmd = commands[args.command]



# Send command and receive reply
try:
	sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock_tcp.connect((ip, port))
	sock_tcp.send(encrypt(cmd))
	data = sock_tcp.recv(2048)
	sock_tcp.close()

	decrypted = decrypt(data[4:])

	if args.quiet:
		print decrypted
	else:
		print "Sent:     ", cmd
		print "Received: ", decrypted

except socket.error:
	quit("Cound not connect to host " + ip + ":" + str(port))