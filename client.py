import socket
import sys
import methods
import os

cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv_addr = (sys.argv[1], int(sys.argv[2])) 
srv_addr_str = str(srv_addr)

try:
    print("--->Connecting to " + srv_addr_str + "... ")
    cli_sock.connect(srv_addr)
    print("--->Connected to server.\n--->Choose one of these options by entering the corresponding number: \n  1]Upload a file. \n  2]Download a file \n  3]List of directory contents. \n  4]Exit\n")
	
except Exception as e:
    print(e)
    exit(1)

try:
    while True:
        #Returns choice and sends choice to server, which is the user input that can only be 1,2,3,4.
        (choice, bytes_sent) = methods.int_to_socket(cli_sock)
        if bytes_sent == 0:
            print("--->Failed to send.")
            break
        #If user choice is 1, start uploading process
        if choice == "1\n":
            #Step 2: Receive the approval message which asks for input and print it
            bytes_read = methods.socket_to_screen(cli_sock)
            if bytes_read == 0:
                print("--->Connection lost.")
                break
            #Step 3: Get and send user input for file name
            (file_name, bytes_sent) = methods.up_filename_to_socket(cli_sock)
            if bytes_sent == 0:
                print("--->Failed to send.")
                break
            #Step 6: Receive the message and print 
            bytes_read = methods.socket_to_screen(cli_sock)
            if bytes_read == 0:
                print("--->Connection lost.")
                break
            #Step 7: Send file to the server
            bytes_sent = methods.cli_file_to_socket(cli_sock, file_name)
            #Close the client
            cli_sock.shutdown(socket.SHUT_WR)
            cli_sock.close()
            if bytes_sent == 0:
                print("--->Failed to send.")
                break
            exit(0)

        #If user choice is 2. start downloading process
        elif choice == "2\n":
            #Step 2: Receive the message which asks for input and print it
            bytes_read = methods.socket_to_screen(cli_sock)
            if bytes_read == 0:
                print("--->Connection lost.")
                break
            #Step 3: Get and send user input for file name
            (file_name, bytes_sent) = methods.down_filename_to_socket(cli_sock)
            if bytes_sent == 0:
                print("--->Failed to send.")
                break
            print("--->Expecting file %s..." % file_name)
            #Step 6: Receive file from server
            bytes_read = methods.cli_socket_to_file(cli_sock, file_name)
            if bytes_read == 0:
                print("--->Connection lost.")
                break
            #Close the client
            cli_sock.shutdown(socket.SHUT_WR)
            cli_sock.close()
            print("--->Done downloading the file.")
            exit(0)

        ##If user choice is 3, Send a list of directory contents of Server
        elif choice == "3\n":
            #Receive a list of directory contents of Server folder and prints them
            (file_list, bytes_read) = methods.socket_to_list(cli_sock)
            if bytes_read == 0:
                print("--->Connection lost.")
                break
            #Close the client
            cli_sock.close()
            exit(0)

        #If user choice is 4, Close the client    
        elif choice == "4\n":
            print("--->Have a nice day...")
            cli_sock.close()
            exit(0)
finally:
    cli_sock.close()

exit(0)
