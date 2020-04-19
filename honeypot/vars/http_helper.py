import ssl
from os import walk, path, getcwd
from socket import AF_INET, SO_REUSEADDR, SOCK_STREAM, SOL_SOCKET, socket
import subprocess
from .constants import (AUTH_FILE, CODES, HTTP_VERSION, MAX_REQUEST, MAX_SIZE, ROOT,
                        SSL_CERT, SSL_KEY)


"""
    Checks headers for request and determines if the client is authorized to view the file or not
"""
def is_authorized(headers):
    auth_entry = [h for h in headers if "Authorization: Basic " in h]

    if not auth_entry:
        return False

    client_auth = auth_entry[0].split()[-1].strip()
    with open(AUTH_FILE, 'r') as auth:
        server_auth = auth.readline().strip()

    return server_auth == client_auth
"""
    Parses incoming client request from the socket and returns necessary information
"""
def parse_request(client_request):
    try:
        file_request = client_request[0].split()
        client_command = file_request[0]                      # COMMAND
        client_request_uri = file_request[1].split('/')[1]    # REQUEST_URI
        if client_request_uri == "":                          # / --> /index.html for HTTP servers
            client_request_uri = "index.html"
        filepath = get_filepath(client_request_uri)
        version = file_request[2]
        headers = client_request[1:]

        return client_command, filepath, version, headers
    except:
        # Something went wrong while parsing - 400 Error
        return None, None, None, None


"""
    Gets the file extension for the requested file in the server
"""
def get_content_type(code, path):
    if code != 200:
        return None, "text/html"

    file_extension = path.split('.')[-1]
    if file_extension == "txt":
        filetype = "text/plain"
    elif file_extension == "png" or file_extension == "jpg":
        filetype = "image/" + file_extension
    elif file_extension == "html":
        filetype = "text/html"
    elif file_extension == "py":
        filetype = "text/plain"
    else:
        filetype = "text/plain"

    return file_extension, filetype


"""
    Walks http_root directory and returns the filepath for the requested URI (or None if not present)
"""
def get_filepath(uri):
    if uri is None:
        return None
    for root, dirs, files in walk(ROOT):
        if uri in files:
            return f"{root}/{uri}"
    return None

"""
    Gets data in a readable format for the requested URI on the server
"""
def get_data(filepath, file_size, code):
        if file_size == 0:
            return create_response_html(code)

        # Open file and get data
        filetype, content_type = get_content_type(code, filepath)
        if filetype == "py":
            # File is executable - execute and return output
            cmd = "python3 " + path.join(getcwd(), filepath)
            data = subprocess.check_output(cmd, shell=True)
        else:
            # File isn't an executable file - read as normal
            read_mode = "r" if content_type == "text/plain" else "rb"       # rb for images, r for text
            with open(filepath, read_mode) as requested_file:
                data = requested_file.read(file_size)
        return data


"""
    Create HTTP response with following format:
    <HTTP_VERSION> <code> <reason_phrase>
    <headers>
    ...
    <response_data>
"""
def create_response(code, command, filepath, response_headers, file_size=0):
    filetype, content_type = get_content_type(code, filepath)                                 # Content type of msg to send
    response_data = get_data(filepath, file_size, code)                             # Data to send
    
    response = HTTP_VERSION + " " + str(code) + " " + CODES[code][0] + "\r\n"       # HTTP/1.1 <code> <reason_phrase>
    if code == 401:
            # 401 Unauthorized response must include Authorization Header
            response += 'WWW-Authenticate: Basic realm="ChrisCohen-Webserver"'
    response += "Content-Length: " + str(len(response_data)) + "\r\n"               # Content-Length: <len>
    response += f"Content-Type: {content_type}\r\n\r\n"                             # Content-Type: <type>
    
    
    return response, response_data


"""
    Creates html version of HTTP response
"""
def create_response_html(code):
    return f"""
    <!DOCTYPE HTML PUBLIC>
    <html>
        <head>
            <title>My Web Server</title>
        </head>
        <body>
            <h1>{code} - {CODES[code][0]}</h1>
            <h2>{CODES[code][1]}</h2>
            <br/>
            <br/>
        </body>
    </html>
    """


"""
    Creates and binds a TCP socket that is listening for connections on the specified port number
"""
def create_tcp_sock(host, port):
    server_sock = socket(AF_INET, SOCK_STREAM)                              # Creates a TCP socket ready for use
    server_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)                     # Makes used port immediately available after termination of server
    #server_sock.settimeout(15)                                              # Makes socket raise SocketTimeout after 30 seconds of inactivity
    server_sock.bind((host, port))                                          # Binds the TCP socket for use from any address
    server_sock.listen(5)                                                   # Listens for connections on socket

    # SSL
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=SSL_CERT, keyfile=SSL_KEY)
    context.set_ciphers('EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH')

    print(f"Listening on {host}:{port}...")
    return server_sock, context
