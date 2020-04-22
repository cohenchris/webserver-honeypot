import math
import ssl
import subprocess
import time
from os import getcwd, listdir, path, stat, walk
from socket import AF_INET, SO_REUSEADDR, SOCK_STREAM, SOL_SOCKET, socket

from .constants import (AUTH_FILE, BLACKLIST, CODES, HTTP_VERSION, ROOT,
                        SSL_CERT, SSL_KEY)


"""
    Checks /var/blacklist.txt to see if the given IP is present
"""
def get_blacklist():
    banned_ips = []
    with open(BLACKLIST, "r") as blacklist:
        [banned_ips.append(line.strip()) for line in blacklist]

    return banned_ips


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
        client_request_uri = file_request[1]                  # REQUEST_URI
        if client_request_uri == "/" or client_request_uri == "/index.html":  # / --> /index.html for HTTP servers
            client_request_uri = "/htdocs/index.html"
        if client_request_uri[-1] == "/":
            client_request_uri = client_request_uri[:-1]      # If there's a trailing '/' (like for a directory listing), get rid of it
        if "%20" in client_request_uri:                       # Catches corner case for file with space in name - %20 used instead of space in URLs
            client_request_uri = client_request_uri.replace("%20", " ")
        if file_exists(ROOT + client_request_uri):
            filepath = ROOT + client_request_uri
        else:
            filepath = None
        version = file_request[2]
        headers = client_request[1:]

        return client_request_uri, client_command, filepath, version, headers

    except Exception as e:
        print(e)
        # Something went wrong while parsing - 400 Error
        return None, None, None, None, None


"""
    Gets the file extension for the requested file in the server
"""
def get_content_type(path, code=200):
    if code != 200:
        return None, "text/html"

    file_extension = path.split('.')[-1]
    if file_extension == "txt":
        filetype = "text/plain"
    elif file_extension == "png" or file_extension == "jpg" or file_extension == "gif":
        filetype = "image/" + file_extension
    elif file_extension == "svg" or file_extension == "xml":
        filetype = "image/svg+xml"
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
def file_exists(uri):
    if uri is None:
        return None
    directory = uri.strip("/")
    directory = '/'.join((uri).split("/")[:-1])
    target = uri.split("/")[-1]
    try:
        dir_files = listdir(directory)
    except Exception:
        return False

    return True if target in dir_files else False

"""
    Gets data in a readable format for the requested URI on the server
"""
def get_data(filepath, file_size, code):
        if file_size == 0:
            return create_response_html(code), "text/html"

        # Open file and get data
        filetype, content_type = get_content_type(filepath, code)
        if filetype == "py":
            # File is executable - execute and return output
            cmd = "python3 " + path.join(getcwd(), filepath)
            data = subprocess.check_output(cmd, shell=True)
        else:
            # File isn't an executable file - read as normal
            read_mode = "r" if content_type == "text/plain" else "rb"       # rb for images, r for text
            try:
                if filepath == ROOT + "/htdocs/index.html":
                    filepath = ROOT
                    raise IsADirectoryError
                with open(filepath, read_mode) as requested_file:
                    data = requested_file.read(file_size)
            except IsADirectoryError:
                # Requested filepath is a directory - print directory html!
                data = get_directory_html(filepath)
                content_type = "text/html"
        return data, content_type

"""
    Returns the path of some icon in http_root/icons - used for directory listing
"""
def get_file_icon(filepath):
    content_type = str(get_content_type(filepath))
    if path.isdir(filepath):
        return "/icons/folder.gif"
    elif "image" in content_type:
        return "/icons/image.gif"
    elif "text" in content_type:
        return "/icons/text.gif"
    else:
        return "/icons/unknown.gif"


"""
    Gets size of a file and converts it into the largest reasonable unit
"""
def get_size(filepath):
    sizes = ["B", "K", "M", "G"]
    original_size = stat(filepath).st_size
    size = original_size
    count = 0
    while size >= 1024 and count <= 3:
        size /= 1024
        count = count + 1
    
    return original_size, (str(math.trunc(size * 100) / 100)) + sizes[count]


"""
    Prints html for a directory
"""
def get_directory_html(filepath):
    html_filepath = filepath + "/"
    if html_filepath.split("/")[0] == ROOT:
        html_filepath = "/" + '/'.join(html_filepath.split("/")[1:])
    files = listdir(filepath)
    file_html = []

    # Parent directory (if not at root)
    if html_filepath != "/":
        parent_dir = "/".join(html_filepath.split("/")[:-2])
        if parent_dir == "":
            parent_dir = "/"
        file_html.append(f'<tr><td valign="top"><img src="/icons/back.gif"></td><td><a href="{parent_dir}">Parent Directory</a></td><td align="right"></td><td align="right"></td></tr>')

    for f in files:
        dir_file = (filepath + "/" + f).strip("/")
        file_created = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stat(dir_file).st_mtime))
        file_size = get_size(dir_file)[1]
        if path.isdir(dir_file):
            f = f + "/"
        file_html.append(f'<tr><td valign="top"><img src={get_file_icon(dir_file)}></td><td><a href="{html_filepath}{f}">{f}</a></td><td align="right">{file_created}</td><td align="right">  {file_size}</td></tr>')

    file_html = "\n".join(file_html)

    return f"""
    <!DOCTYPE HTML PUBLIC>
    <html>
        <head>
            <title>Index of {html_filepath}</title>
        </head>
        <body>
            <h1>Index of {html_filepath}</h1>
            <table>
                <tr><th valign="top"></th><th>Name</th><th>Last modified</th><th>Size</th>
                <tr><th colspan="5"><hr></th></tr>
                    {file_html}
                <tr><th colspan="5"><hr></th></tr>
            </table>
            <p>
                <a href="/">HOME</a>
            </p>
        </body>
    </html>
    """


"""
    Create HTTP response with following format:
    <HTTP_VERSION> <code> <reason_phrase>
    <headers>
    ...
    <response_data>
"""
def create_response(code, command, filepath, response_headers, file_size=0):
    response_data, content_type = get_data(filepath, file_size, code)               # Data to send
    if response_data == "504".encode():
        code = 504
        file_size = 0                                                               # Set back to zero, otherwise it will return the contents of the script!
        response_data, content_type = get_data(filepath, file_size, code)
    
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
            <h1>{code} {CODES[code][0]}</h1>
            <h2>{CODES[code][1]}</h2>
            <br/>
            <br/>
        </body>
    </html>
    """


"""
    Creates and binds a TCP socket that is listening for connections on the specified port number
    Lots of help setting this up from 'https://speakerdeck.com/markush/ssl-all-the-things-pycon-nz-2016?slide=18'
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
