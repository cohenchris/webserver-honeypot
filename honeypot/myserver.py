import os
from select import select
from socket import socket
import ssl
import sys
from stat import ST_SIZE
import threading
import time

from http_helper import parse_request, create_response, create_tcp_sock     # Function imports
from vars.constants import MAX_REQUEST, GREETING, HELP


"""
    Service socket connection
"""
def dispatch_connection(client_sock, client_addr):
    ##################################
    ##### RECEIVE CLIENT REQUEST #####
    ##################################
    # file_request = <command> <request_uri> <http_version>
    while True:
        # This infinite loop keeps handling requests until socket requested to close

        # Extract client request header (going to -2 leaves out last /r/n)
        try:
            client_request = client_sock.recv(MAX_REQUEST).decode().split("\r\n")[:-2]
        except Exception as e:
            print(f"ERROR recv(): {e}")
            break

        if not client_request:
            # If client_request is blank, nothing sent, client closed connection
            print("Terminating connection with address " + str(client_addr))
            break
        else:
            # TODO: enter request into database
            print("REQUEST =        " + str(client_request[0]))
            client_command, client_request_uri, headers = parse_request(client_request)            

        #############################################
        ##### CREATE HTTP RESPONSE AND GET DATA #####
        #############################################
        available_files = os.listdir("./Upload/")
        if client_command != "GET" and client_command != "HEAD":
            # Command is invalid, send 405 Not Allowed
            response, response_data = create_response(405, client_command, client_request_uri, headers)
        elif client_request_uri in available_files:
            # File is present in 'Upload' folder

            # Check if file has read permissions
            readable = os.access("./Upload/" + client_request_uri, os.R_OK)

            if readable:
                # File has correct permissions --> send 200 OK and file data
                file_size = os.stat("./Upload/" + client_request_uri).st_size
                response, response_data = create_response(200, client_command, client_request_uri, headers, file_size)
            else:
                # File does NOT have correct permissions --> send 403 Forbidden
                response, response_data = create_response(403, client_command, client_request_uri, headers)
        else:
            # File is not present in 'Upload' folder --> send 404
            response, response_data = create_response(404, client_command, client_request_uri, headers)

        client_sock.send(response.encode())
        
        if client_command != "HEAD":
            # 'HEAD' only sends headers, not data
            client_sock.send(response_data if type(response_data) is bytes else response_data.encode())

        if "Connection: close" in headers:
            # Last file requested
            break

    print("Terminating connection with address " + str(client_addr))



                                        ##########################
                                        ########## MAIN ##########
                                        ##########################
def main(args):
    if len(args) != 3:
        print(HELP)
    else:
        print(GREETING)
        server_sock, context = create_tcp_sock(args[1], int(args[2]))     # Creates server socket with IP and PORT specified in arguments

        # Infinite loop makes sure server doesn't terminate after accepting a connection
        while True:
            ssl_client_conn = None
            try:
                client_sock, client_addr = server_sock.accept()        # Accepts incoming connection
                ssl_client_conn = context.wrap_socket(client_sock, server_side=True)
                print(f"accepted connection with address {client_addr}")
                threading.Thread(target=dispatch_connection, args=(ssl_client_conn, client_addr)).start()
            except ssl.SSLError as e:
                print(f"ERROR: {e}")
            except OSError as e:
                print(f"SOCKET TIMEOUT: {e}")
                if client_sock:
                    print(f"Client socket {client_addr} closed...")
                    client_sock.close()
                    break

if __name__ == "__main__":
    main(sys.argv)
