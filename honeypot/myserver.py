import os
import ssl
import sys
import threading
import time
from select import select
from socket import socket
from stat import ST_SIZE

from vars.constants import (GREETING, HELP, HTTP_VERSION, INVALID_REQUESTS,
                            MAX_REQUEST, NEEDS_AUTHORIZATION, VALID_REQUESTS)
from vars.http_helper import (is_authorized, create_response, create_tcp_sock, get_filepath,
                              parse_request)


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
            client_command, filepath, version, headers = parse_request(client_request)

        #############################################
        ##### CREATE HTTP RESPONSE AND GET DATA #####
        #############################################
        if client_command is None and filepath is None and version is None and headers is None:
            # Client request has error --> 400 Bad Request
            response, response_data = create_response(400, client_command, filepath, headers)
        elif version != HTTP_VERSION:
            # HTTP Version invalid, send 505 HTTP Version Not Supported
            response, response_data = create_response(505, client_command, filepath, headers)
        elif client_command not in VALID_REQUESTS:
            if client_command not in INVALID_REQUESTS:
                # Command not recognized, send 501 Not Implemented
                response, response_data = create_response(501, client_command, filepath, headers)
            else:
                # Command is invalid, send 405 Not Allowed
                response, response_data = create_response(405, client_command, filepath, headers)

        elif filepath is not None:
            # Check if file has read permissions
            readable = os.access(filepath, os.R_OK)

            if readable:
                authorized = filepath not in NEEDS_AUTHORIZATION or is_authorized(headers)
                if not authorized:
                    # The client is not authorized to view the file at 'filename' --> send 401 Unauthorized
                    response, response_data = create_response(401, client_command, filepath, headers)
                else:
                    # File has correct permissions --> send 200 OK and file data
                    file_size = os.stat(filepath).st_size
                    response, response_data = create_response(200, client_command, filepath, headers, file_size)
            else:
                # File does NOT have correct permissions --> send 403 Forbidden
                response, response_data = create_response(403, client_command, filepath, headers)
        else:
            # File is not present in 'http_root' folder --> send 404
            response, response_data = create_response(404, client_command, filepath, headers)

        client_sock.send(response.encode())

        if client_command != "HEAD":
            # 'HEAD' only sends headers, not data
            client_sock.send(response_data if type(response_data) is bytes else response_data.encode())

        if headers and "Connection: close" in headers:
            # Last file requested
            break

    print("Terminating connection with address " + str(client_addr))



                                        ##########################
                                        ########## MAIN ##########
                                        ##########################
def main(args):
    args.append("127.0.0.1")
    args.append(12345)

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
                print(f"SSL ERROR: {e}")
            except OSError as e:
                print(f"SOCKET TIMEOUT: {e}")
                if client_sock:
                    print(f"Client socket {client_addr} closed...")
                    client_sock.close()
                    break

if __name__ == "__main__":
    main(sys.argv)
