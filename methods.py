import sys
import socket
import os

#Recieves the client input integer number from socket and returns it as choice
def socket_to_int(socket):
        data = bytearray(1)
        bytes_read = 0
        while len(data) > 0 and "\n" not in data.decode():
                data = socket.recv(4096)
                choice = ""
                choice += data.decode()
                bytes_read += len(data)
        return (choice, bytes_read)

#Sends the user input integer number, 1-4, to the socket and returns the user input
def int_to_socket(socket):
        user_input = ""
        while user_input not in ["1\n","2\n","3\n","4\n"]:
            user_input = sys.stdin.readline()
            if user_input not in ["1\n","2\n","3\n","4\n"]:
                print("--->Invalid input. Enter one of 1,2,3,4.\n", end="")
        bytes_sent = socket.sendall(str.encode(user_input))
        return (user_input, bytes_sent)

#Sends the list of directory contents in Server to the socket as a string with a '*' between each file.
def list_to_socket(socket):
        cwd = os.getcwd() + "\\Server"
        dir_cont = os.listdir(cwd)
        str_list = ""
        for element in dir_cont:
                str_list += element
                str_list += "*"
        bytes_sent = socket.sendall(str.encode(str_list + "\n"))
        socket.close()
        return bytes_sent

#Receives the data from socket and prints it on screen.
def socket_to_screen(socket):
        data = bytearray(1)
        bytes_read = 0
        while len(data) > 0 and "\n" not in data.decode():
                data = socket.recv(4096)
                print(data.decode(), end="")
                bytes_read += len(data)
        return bytes_read

#Receives the list of directory contents from socket as a string, turns it into a list
#and prints each element in the list in an appropriate format. 
def socket_to_list(socket):
        data = bytearray(1)
        bytes_read = 0
        while len(data) > 0 and "\n" not in data.decode():
                data = socket.recv(4096)
                str_list = ""
                str_list += data.decode()
                file_list = str_list.strip("*").split("*")[:-1]
                print("--->The list of directory contents: ")
                for file in file_list :
                        print (">"+file)
                bytes_read += len(data)
        return (file_list,bytes_read)

#User inputs a filename for uploading, checks if user input is null, checks if file exists in client's folder to upload
#and checks if file exists in server's folder to not overwrite it. Returns the file name.
def up_input_to_filename(socket):
        user_input = sys.stdin.readline().strip()+"\n"
        while user_input == "\n":
            print("--->File name cannot be null.")
            print("--->Please enter a file name:")
            user_input = sys.stdin.readline().strip()+"\n"
        if (os.path.exists(os.path.join(os.getcwd()+"\\Client", user_input.strip("\n"))) == False):
            print("--->File does not exist")
            print("--->Closing the connection.")
            socket.close()
            exit(1)
        if (os.path.exists(os.path.join(os.getcwd()+"\\Server", user_input.strip("\n")))):
            print("--->File already exists in server.")
            print("--->Closing the connection.")
            socket.close()
            exit(1)
        return user_input

#User inputs a filename for downloading, checks if user input is null, checks if file exists in server's folder to download
#and checks if file exists in client's folder to not overwrite it. Returns the file name.
def down_input_to_filename(socket):
        user_input = sys.stdin.readline().strip()+"\n"
        while user_input == "\n":
            print("--->File name cannot be null.")
            print("--->Please enter a file name:")
            user_input = sys.stdin.readline().strip()+"\n"
        if (os.path.exists(os.path.join(os.getcwd()+"\\Server", user_input.strip("\n"))) == False):
            print("--->File does not exist")
            print("--->Closing the connection.")
            socket.close()
            exit(1)
        if (os.path.exists(os.path.join(os.getcwd()+"\\Client", user_input.strip("\n")))):
            print("--->File already exists in client.")
            print("--->Closing the connection.")
            socket.close()
            exit(1)
        return user_input

#Sends the filename to the socket for uploading part and returns filename
def up_filename_to_socket(socket):
        file_name = up_input_to_filename(socket)
        bytes_sent = socket.sendall(str.encode(file_name))
        return (file_name.strip("\n"), bytes_sent)

#Sends the filename to the socket for downloding part and returns filename
def down_filename_to_socket(socket):
        file_name = down_input_to_filename(socket)
        bytes_sent = socket.sendall(str.encode(file_name))
        return (file_name.strip("\n"), bytes_sent)

#Receives the filename from socket decodes it and returns it
def socket_to_filename(socket):
        data = bytearray(1)
        bytes_read = 0
        while len(data) > 0 and "\n" not in data.decode():
                data = socket.recv(4096)
                file_name = ""
                file_name += data.decode()
                bytes_read += len(data)
        return (file_name.strip("\n"), bytes_read)

#Sends the file in Client folder to the socket for uploading
def cli_file_to_socket(temp_socket, file_name):
        file = open(os.path.join(os.getcwd()+"\\Client", file_name), "rb")
        data = file.read(1024)
        bytes_sent = len(data)
        while data:
                temp_socket.send(data)
                data = file.read(1024)
                bytes_sent += len(data)
        file.close()
        print("--->Sending is done")
        return bytes_sent

#Sends the file in Server folder to the socket for downloading
def svr_file_to_socket(temp_socket, file_name):
        file = open(os.path.join(os.getcwd()+"\\Server", file_name), "rb")
        data = file.read(1024)
        bytes_sent = len(data)
        while data:
                temp_socket.send(data)
                data = file.read(1024)
                bytes_sent += len(data)
        file.close()
        print("--->Sending is done")
        return bytes_sent

#Receives the file from socket and writes it into client folder, part of downloading.
def cli_socket_to_file(socket, file_name ):
        file = open(os.path.join(os.getcwd()+"\\Client", file_name), "wb")
        data = bytearray(1)
        bytes_read = len(data)
        while True:
                data = socket.recv(1024)
                bytes_read += len(data)
                if not data:
                        break
                file.write(data)
        file.close()
        return bytes_read

#Receives the file from socket and writes it into server folder, part of uploading.
def svr_socket_to_file(socket, file_name ):
        file = open(os.path.join(os.getcwd()+"\\Server", file_name), "wb")
        data = bytearray(1)
        bytes_read = len(data)
        while True:
                data = socket.recv(1024)
                bytes_read += len(data)
                if not data:
                        break
                file.write(data)
        file.close()
        return bytes_read
