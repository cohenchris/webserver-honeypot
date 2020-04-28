        ##### PERSONAL WEBSITE DETAILS #####
WEBSITE_URL = ""
        ####################################



        ##### BASIC SERVER STUFF #####
MAX_REQUEST = 1024
MAX_URI = 128
MAX_SIZE = 104857600          # Max file size is 100MB
HTTP_VERSION = "HTTP/1.1"
ROOT = "htdocs"

VALID_REQUESTS = ["GET", "HEAD"]
INVALID_REQUESTS = ["POST", "PUT", "DELETE", "TRACE", "OPTIONS", "CONNECT", "PATCH"]
        ##############################

        ##### SECURITY STUFF #####
AUTH_FILE = "vars/keys/auth.txt"
SSL_CERT = "vars/keys/cert.pem"
SSL_KEY = "vars/keys/key.pem"

NEEDS_AUTHORIZATION = []
        ##########################

GREETING = r"""
   _____  _____ _  _ ___  ___   __          __  _        _____                          
  / ____|/ ____| || |__ \|__ \  \ \        / / | |      / ____|                         
 | |    | (___ | || |_ ) |  ) |  \ \  /\  / /__| |__   | (___   ___ _ ____   _____ _ __ 
 | |     \___ \|__   _/ /  / /    \ \/  \/ / _ \ '_ \   \___ \ / _ \ '__\ \ / / _ \ '__|
 | |____ ____) |  | |/ /_ / /_     \  /\  /  __/ |_) |  ____) |  __/ |   \ V /  __/ |   
  \_____|_____/   |_|____|____|     \/  \/ \___|_.__/  |_____/ \___|_|    \_/ \___|_|   
                                                                                                                                            
"""

HELP = """\
Usage:\tpython3 myserver.py <IP> <PORT>

AVAILABLE COMMANDS:
- GET
- HEAD\
"""

# Credit goes to https://github.com/bocajspear1/honeyhttpd in the file 'honeyhttpd/servers/TestServer.py   # IMPLEMENTED (13)
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
