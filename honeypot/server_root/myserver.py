import os
import ssl
import sys
import threading
import time
from select import select
from socket import socket
from stat import ST_SIZE

from vars.constants import (GREETING, HELP, HTTP_VERSION, INVALID_REQUESTS,
                            MAX_REQUEST, MAX_SIZE, MAX_URI,
                            NEEDS_AUTHORIZATION, VALID_REQUESTS)
from vars.http_helper import (create_response, create_tcp_sock, get_size,
                              is_authorized, parse_request)

LOG = True

"""
    Service socket connection
"""
def dispatch_connection(client_sock, client_addr):
    ##################################
    #     RECEIVE CLIENT REQUEST     #
    ##################################
    try:
        # file_request = <command> <request_uri> <http_version>
        # This infinite loop keeps handling requests until socket requested to close
        while True:
            # Extract client request header (going to -2 leaves out last /r/n)
            try:
                client_request = client_sock.recv(MAX_REQUEST).decode().split("\r\n")[:-2]
            except Exception as e:
                print(f"RECV(): {e}")
                break

            if not client_request:
                # If client_request is blank, nothing sent, client closed connection
                print(f"ERROR - client closed connection")
                break
            else:
                client_request_uri, client_command, filepath, version, headers = parse_request(client_request)
                if LOG:
                    threading.Thread(target=log, args=(client_addr[0], client_addr[1], client_request[0])).start()  # LOGGING

            #######################################################################
            #                        HTTP RESPONSE CREATION                       #
            #######################################################################
            update_blacklist()
            banned_ips = get_blacklist()
            banned = False
            if client_addr[0] in banned_ips:
                # 403.6 IP Address Rejected     -->     IP Address is blacklisted
                response, response_data = create_response(403.6, client_command, filepath, headers)
                banned = True
            elif client_command is None and filepath is None and version is None and headers is None:
                # 400 Bad Request   -->     Client request has error
                response, response_data = create_response(400, client_command, filepath, headers)
            elif version != HTTP_VERSION:
                # 505 HTTP Version Not Supported    -->     HTTP Version invalid
                response, response_data = create_response(505, client_command, filepath, headers)
            elif client_command not in VALID_REQUESTS:
                if client_command not in INVALID_REQUESTS:
                    # 501 Not Implemented   -->     Command not recognized
                    response, response_data = create_response(501, client_command, filepath, headers)
                else:
                    # 405 Not Allowed   -->     Command is invalid
                    response, response_data = create_response(405, client_command, filepath, headers)
            elif len(client_request_uri) > MAX_URI:
                # 414 Request URI Too Large     -->     Request URI is greater than MAX_REQUEST
                response, response_data = create_response(414, client_command, filepath, headers)
            elif filepath is not None:
                # Check if file has read permissions
                readable = os.access(filepath, os.R_OK)
                if readable:
                    authorized = filepath not in NEEDS_AUTHORIZATION or is_authorized(headers)
                    if not authorized:
                        # 401 Unauthorized      -->     Client is unauthorized to view file, can view with authorizatiom
                        response, response_data = create_response(401, client_command, filepath, headers)
                    elif get_size(filepath)[0] > MAX_SIZE:
                        # 413 Request Entity Too Large      -->     Requested file is greater than MAX_SIZE bytes
                        response, response_data = create_response(413, client_command, filepath, headers)
                    else:
                        # 200 OK    -->     File exists and user is authorized to read it
                        file_size = get_size(filepath)[0]
                        response, response_data = create_response(200, client_command, filepath, headers, file_size)
                else:
                    # 403 Forbidden    -->     Client cannnot view file even with authorization
                    response, response_data = create_response(403, client_command, filepath, headers)
            else:
                # 404 Not Found     -->     Requested file does not exist
                response, response_data = create_response(404, client_command, filepath, headers)
            #######################################################################

            send_to_client(client_sock, client_addr, client_command, response, response_data)
            if headers and "Connection: close" in headers:
                # Last file requested
                break
            if banned:
                send_to_client(client_sock, client_addr, client_command, response, response_data)
                break

        print("Terminating connection with address " + str(client_addr))
        client_sock.close()
    except Exception as e:
        # 500 Internal Server Error     -->     The program crashed while dealing with the request
        response, response_data = create_response(500, None, None, None)
        send_to_client(client_sock, client_addr, None, response, response_data)


"""
    Sends response + data to client_sock
"""
def send_to_client(client_sock, client_addr, client_command, response, response_data):
    try:
        client_sock.send(response.encode())
        if client_command != "HEAD":
            # 'HEAD' only sends headers, not data
            client_sock.send(response_data if type(response_data) is bytes else response_data.encode())
    except:
        print(f"Client socket {client_addr} is no longer active")


                                        ##########################
                                        #          MAIN          #
                                        ##########################
def main(args):
    if len(args) != 2:
        print(HELP)
    else:
        print(GREETING)
        #                                       IP          PORT
        server_sock, context = create_tcp_sock(args[0], int(args[1]))

        # Infinite loop makes sure server doesn't terminate after accepting a connection
        while True:
            ssl_client_conn = None
            try:
                client_sock, client_addr = server_sock.accept()        # Accepts incoming connection

                #ssl_client_conn = context.wrap_socket(client_sock, server_side=True)
                print(f"accepted HTTPS connection with address {client_addr}")
                threading.Thread(target=dispatch_connection, args=(client_sock, client_addr)).start()
            except ssl.SSLError as e:
                print(f"SSLError: {e}")
                # 301 Moved Permanently - HTTP Connection Received
                client_sock, client_addr = server_sock.accept()        # If it messes up, need to re-accept connection
                response, response_data = create_response(301, None, None, None)
                send_to_client(client_sock, client_addr, None, response, response_data)
            except Exception as e:
                print(f"MISC ERROR: {e}")
                if client_sock:
                    print(f"Client socket {client_addr} closed...")
                    client_sock.close()
                
                

if __name__ == "__main__":
    main(sys.argv[1:])
