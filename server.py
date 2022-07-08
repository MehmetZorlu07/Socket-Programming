import socket
import sys
import methods
import os

srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    srv_sock.bind(("0.0.0.0", int(sys.argv[1]))) 
    srv_sock.listen(5)
    cwd = os.getcwd()
    print("--->IP address: " , srv_sock.getsockname()[0])
    print("--->Port number: " , srv_sock.getsockname()[1])
    print("--->Working directory: " , cwd)
	
except Exception as e:
    print(e)
    exit(1)

while True:
    try:
        while True:
            print("\n*******************************************************************")
            print("--->Waiting for new client... ")
            cli_sock, cli_addr = srv_sock.accept()
            cli_addr_str = str(cli_addr) 
            print("--->Client " + cli_addr_str + " connected.\n--->Waiting for a request...")
            #Receives user choice from client and returns it
            (choice, bytes_read) = methods.socket_to_int(cli_sock)
            choice = int(choice.strip("\n"))
            if bytes_read == 0:
                print("--->Connection lost.")
                break
            #If user choice is 1, start uploading process
            if choice == 1:
                print("--->Client requested to upload a file.")
                #Step 1: Send an approval message which will ask the client to enter file name
                cli_sock.sendall(str.encode("--->Please enter a file name: \n"))
                #Step 4: Receive the file name
                (file_name, bytes_read) = methods.socket_to_filename(cli_sock)
                if bytes_read == 0:
                    print("--->Connection lost.")
                    break
                print("--->Expecting file %s..." % file_name)
                #Step 5: Send approval message
                cli_sock.sendall(str.encode("--->Uploading file %s... \n" % file_name))
                #Step 8: Receive file from client
                bytes_read = methods.svr_socket_to_file(cli_sock, file_name)
                #Close client socket
                cli_sock.close()
                print("--->Done uploading")
                if bytes_read == 0:
                    print("--->Connection lost.")
                    break
                print("--->Client closed the connection.")

            #If user choice is 2, start downloading process
            if choice == 2:
                print("--->Client requested to download a file.")
                #Step 1: Send an approval message which will ask for a file name
                cli_sock.sendall(str.encode("--->Please enter a file name: \n"))
                #Step 4: Receive the file name
                (file_name, bytes_read) = methods.socket_to_filename(cli_sock)
                if bytes_read == 0:
                    print("--->Connection lost.")
                    break
                print("--->Sending file %s..." % file_name)
                #Step 5: Send file to client
                bytes_sent = methods.svr_file_to_socket(cli_sock, file_name)
                #Close client socket
                cli_sock.close()
                if bytes_sent == 0:
                    print("--->Failed to send.")
                    break
                print("--->Client closed the connection.")

            #If user choice is 3, Send a list of directory contents of Server
            if choice == 3:
                print("--->Client requested a list of directory contents.")
                #Send a list of directory contents of Server folder
                bytes_sent = methods.list_to_socket(cli_sock)
                if bytes_sent == 0:
                    print("--->Failed to send.")
                    break
                print("--->Client closed the connection.")

            #If user choice is 4, close the client socket
            if choice == 4:
                print("--->Client requested exit.")
                cli_sock.close()
                print("--->Client closed the connection.")

    finally:
        cli_sock.close()

srv_sock.close()
exit(0)
