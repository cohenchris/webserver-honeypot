        ##### PERSONAL WEBSITE DETAILS #####
USERNAME = ""
PASSWORD = ""
DATABASE = ""
WEBSITE_URL = ""
        ####################################





        ##### BASIC SERVER STUFF #####
MAX_REQUEST = 1024
MAX_URI = 128
MAX_SIZE = 104857600          # Max file size is 100MB
HTTP_VERSION = "HTTP/1.1"
ROOT = "server_root"

VALID_REQUESTS = ["GET", "HEAD"]
INVALID_REQUESTS = ["POST", "PUT", "DELETE", "TRACE", "OPTIONS", "CONNECT", "PATCH"]
        ##############################

        ##### DATABASE STUFF #####
TABLE = "logfile"
COLUMNS = "(username, ip, port, request)"
BLACKLIST = "vars/blacklist.txt"
DB_CONFIG = {
        'user': f'{USERNAME}',
        'password': f'{PASSWORD}',
        'host': '127.0.0.1',
        'database': f'{DATABASE}}',
        'auth_plugin': 'mysql_native_password'
}
KNOWN_USERS = {
    "127.0.0.1"     :   "localhost",
}
IGNORED_REQUESTS = ["/icons"]           # Hacky fix to eliminate the excessive requests logged for each of the displayed icons
        ##########################

        ##### SECURITY STUFF #####
AUTH_FILE = "vars/keys/auth.txt"
SSL_CERT = "vars/keys/fullchain.pem"
SSL_KEY = "vars/keys/privkey.pem"

NEEDS_AUTHORIZATION = ["server_root/cgi-bin/server_logs.py"]
        ##########################

GREETING = r"""
  _    _  ____  _   _ ________     _______   ____ _______ 
 | |  | |/ __ \| \ | |  ____\ \   / /  __ \ / __ \__   __|
 | |__| | |  | |  \| | |__   \ \_/ /| |__) | |  | | | |   
 |  __  | |  | | . ` |  __|   \   / |  ___/| |  | | | |   
 | |  | | |__| | |\  | |____   | |  | |    | |__| | | |   
 |_|  |_|\____/|_| \_|______|  |_|  |_|     \____/  |_|   
                                                    
"""

HELP = """\
Usage:\tpython3.8 honeypot_server.py <IP> <PORT>

AVAILABLE COMMANDS:
- GET
- HEAD\
"""

# Credit goes to https://github.com/bocajspear1/honeyhttpd in the file 'honeyhttpd/servers/TestServer.py   # IMPLEMENTED (14)
CODES = {                                                                                                  # -----------
        100: ('Continue', 'Request received, please continue'),                                            # 
        101: ('Switching Protocols', 'Switching to new protocol; obey Upgrade header'),                    # 
        
        200: ('OK', 'Request fulfilled, document follows'),                                                #    200
        201: ('Created', 'Document created, URL follows'),                                                 # 
        202: ('Accepted', 'Request accepted, processing continues off-line'),                              # 
        203: ('Non-Authoritative Information', 'Request fulfilled from cache'),                            # 
        204: ('No Content', 'Request fulfilled, nothing follows'),                                         # 
        205: ('Reset Content', 'Clear input form for further input.'),                                     # 
        206: ('Partial Content', 'Partial content follows.'),                                              # 

        300: ('Multiple Choices', 'Object has several resources -- see URI list'),                         # 
        301: ('Moved Permanently', 'Object moved permanently -- see URI list'),                            #    301
        302: ('Found', 'Object moved temporarily -- see URI list'),                                        # 
        303: ('See Other', 'Object moved -- see Method and URL list'),                                     # 
        304: ('Not Modified', 'Document has not changed since given time'),                                # 
        305: ('Use Proxy', 'You must use proxy specified in Location to access this resource.'),           # 
        307: ('Temporary Redirect', 'Object moved temporarily -- see URI list'),                           # 

        400: ('Bad Request', 'Bad request syntax or unsupported method'),                                  #    400
        401: ('Unauthorized', 'No permission -- see authorization schemes'),                               #    401
        402: ('Payment Required', 'No payment -- see charging schemes'),                                   # 
        403: ('Forbidden', 'Request forbidden -- authorization will not help'),                            #    403
        403.6: ('Forbidden', 'IP address rejected'),                                                       #    403.6
        404: ('Not Found', 'The requested resource is not available.'),                                    #    404
        405: ('Method Not Allowed', 'Specified method is invalid for this resource.'),                     #    405
        406: ('Not Acceptable', 'URI not available in preferred format.'),                                 # 
        407: ('Proxy Authentication Required', 'You must authenticate with this proxy before proceeding.'),# 
        408: ('Request Timeout', 'Request timed out; try again later.'),                                   # 
        409: ('Conflict', 'Request conflict.'),                                                            # 
        410: ('Gone', 'URI no longer exists and has been permanently removed.'),                           # 
        411: ('Length Required', 'Client must specify Content-Length.'),                                   # 
        412: ('Precondition Failed', 'Precondition in headers is false.'),                                 # 
        413: ('Request Entity Too Large', 'Entity is too large.'),                                         #    413
        414: ('Request-URI Too Long', 'URI is too long.'),                                                 #    414
        415: ('Unsupported Media Type', 'Entity body in unsupported format.'),                             # 
        416: ('Requested Range Not Satisfiable', 'Cannot satisfy request range.'),                         # 
        417: ('Expectation Failed', 'Expect condition could not be satisfied.'),                           # 
        
        500: ('Internal Server Error', 'Server got itself in trouble'),                                    #    500
        501: ('Not Implemented', 'Server does not support this operation'),                                #    501
        502: ('Bad Gateway', 'Invalid responses from another server/proxy.'),                              #
        503: ('Service Unavailable', 'The server cannot process the request due to a high load'),          # 
        504: ('Gateway Timeout', 'The gateway server did not receive a timely response'),                  #    504
        505: ('HTTP Version Not Supported', 'Cannot fulfill request.')                                     #    505
}
