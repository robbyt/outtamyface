#!/usr/bin/env python
from time import sleep
import logging
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
logging.debug("Setup logging")

from miniboa import TelnetServer

IDLE_TIMEOUT = 600
logging.debug("Timeout set to: %s" % (IDLE_TIMEOUT))

PRODUCT_NAME = "iMyFace"
CLIENT_LIST = []
CLIENT_STATE = {}
AUTH_DB = {}

SERVER_RUN = True
AUTH_RETRY = 2

def on_connect(client):
    """ handler for new connections
    """
    logging.info("Opened connection to %s" % client.addrport() )

    CLIENT_LIST.append(client)
    CLIENT_STATE[client] = {}
    client.send("")
    client.send("Welcome to the %s Server, %s.\n" % (PRODUCT_NAME, client.addrport()) )
    client.send("Enter your user_id, or type \"enroll\" to create a new account: ")


def on_disconnect(client):
    """ lost, or disconnected clients
    """
    logging.info("Lost connection to %s" % client.addrport() )
    CLIENT_LIST.remove(client)
    del(CLIENT_STATE[client])
    #broadcast('%s leaves the conversation.\n' % client.addrport() )


def kick_idle():
    """
    Looks for idle clients and disconnects them by setting active to False.
    """
    ## Who hasn't been typing?
    for client in CLIENT_LIST:
        if client.idle() > IDLE_TIMEOUT:
            logging.info('Kicking idle client %s' % client.addrport())
            client.active = False


def process_clients():
    """
    Check each client, if client.cmd_ready == True then there is a line of
    input available via client.get_command().
    """
    for client in CLIENT_LIST:
        if client.active and client.cmd_ready:
            logging.debug("Found a message, processing...")
            msg_processor(client)

def _enroll(client, msg):
    current_state = CLIENT_STATE[client]['auth_status']

    def get_user():
        client.send("New username: ")
        CLIENT_STATE[client]['auth_status'] = 'enroll_user'

    def enroll_user():
        if not AUTH_DB.has_key(msg):
            CLIENT_STATE[client]['user_id'] = msg
            CLIENT_STATE[client]['auth_status'] = 'enroll_pass'
            client.send("New password: ")
            client.password_mode_on()
        else:
            client.send("%s already taken, try something else: " % msg)
            CLIENT_STATE[client]['auth_status'] = 'enroll_user'

    def enroll_pass():
        CLIENT_STATE[client]['pass1'] = msg
        client.send("Please type your password again: ")
        CLIENT_STATE[client]['auth_status'] = 'enroll_pass2'

    def enroll_pass2():
        if CLIENT_STATE[client]['pass1'] == msg:
            client.password_mode_off()
            logging.debug("New password confirmed.")
            CLIENT_STATE[client]['temp_password'] = msg
            CLIENT_STATE[client]['auth_status'] = 'enroll_first_name'
            client.send("\nWhat is your first name: ")
        else:
            logging.debug("Running target state %s in enroll module" % current_state)
            CLIENT_STATE[client]['auth_status'] = 'enroll_pass'

    def enroll_first_name():
        if msg is not None or msg is not "":
            CLIENT_STATE[client]['first_name'] = msg
            CLIENT_STATE[client]['auth_status'] = 'enroll_last_name'
            client.send("What is your last name: ")

    def enroll_last_name():
        if msg is not None or msg is not "":
            CLIENT_STATE[client]['last_name'] = msg
            CLIENT_STATE[client]['auth_status'] = 'enroll_save'
            fn = CLIENT_STATE[client]['first_name']
            ln = CLIENT_STATE[client]['last_name']
            client.send("\nAbout to create new user: %s %s" % (fn, ln))
            client.send("\nType yes, and hit enter to continue: ")

    def enroll_save():
        if not msg.lower() == 'yes':
            CLIENT_STATE[client]['auth_status'] = 'startup'
            client.active = False
            return
        user_id = CLIENT_STATE[client]['user_id']
        password = CLIENT_STATE[client]['temp_password']
        first_name = CLIENT_STATE[client]['first_name']
        last_name = CLIENT_STATE[client]['last_name']
        AUTH_DB[user_id] = {'password': password, 'first_name': first_name, 'last_name': last_name}
        
        # cleanup password session vars
#        del(CLIENT_STATE[client]['temp_password'])
#        del(CLIENT_STATE[client]['pass1'])

        logging.debug("Saved user_id and password in auth_db")
        client.send("Your account has been created. \n")
        client.send("Please enter your new username: ")
        CLIENT_STATE[client]['auth_status'] = 'startup'
        process_clients()

    cmds = {'enroll_start': get_user,
            'enroll_user': enroll_user,
            'enroll_pass': enroll_pass,
            'enroll_pass2': enroll_pass2,
            'enroll_first_name': enroll_first_name,
            'enroll_last_name': enroll_last_name,
            'enroll_save': enroll_save,
            }
    
    if cmds.has_key(current_state):
        logging.debug("Running target state %s in enroll module" % current_state)
        cmds[current_state]()
    else:
        logging.warn("Can not find target state in enroll module")

def _set_user_id(client, msg):
    logging.debug("_set_user_id got message: " + msg)
    if msg == 'enroll':
        CLIENT_STATE[client]['auth_status'] = 'enroll_start'
        _enroll(client, msg)
    else:
        CLIENT_STATE[client]['user_id'] = msg
        logging.debug("Client set user_id to: " + msg)
        # next step:
        CLIENT_STATE[client]['auth_status'] = 'set_pass'
        client.password_mode_on()
        client.send("Enter your password: ")
        process_clients()

def _set_password(client, msg):
    CLIENT_STATE[client]['password'] = msg
    client.password_mode_off()
    logging.debug("Client set password to: " + msg)
    CLIENT_STATE[client]['auth_status'] = 'auth_lookup'
    msg_processor(client)

def _auth_lookup(client, msg):
    def login_failed():
        client.send("\nUser_id or password incorrect, enter your user_id again: ")
        CLIENT_STATE[client]['auth_retry'] += 1
        CLIENT_STATE[client]['auth_status'] = 'startup'

    user_id = CLIENT_STATE[client]['user_id']
    client_password = CLIENT_STATE[client]['password']
    if AUTH_DB.has_key(user_id):
        if AUTH_DB[user_id]['password'] == client_password:
            logging.debug("auth_db lookup success for: " + user_id)
            CLIENT_STATE[client]['auth_status'] = 'auth_success'
            broadcast(client, '%s just connected.\n' % user_id )
            msg_processor(client)
        else:
            login_failed()
    else:
        login_failed()
        
def auth(client, msg):
#    msg = str(client.get_command())
    logging.debug('Auth for %s:%s' % (client.addrport(), msg))

    auth_status = CLIENT_STATE[client].get('auth_status', 'startup')
    logging.debug("The auth status for %s is %s" % (str(client), auth_status))

    command_dict = {'startup': _set_user_id,
                    'set_pass': _set_password,
                    'auth_lookup': _auth_lookup,
                    'enroll_start': _enroll,
                    'enroll_user': _enroll,
                    'enroll_pass': _enroll,
                    'enroll_pass2': _enroll,
                    'enroll_first_name': _enroll,
                    'enroll_last_name': _enroll,
                    'enroll_save': _enroll,
                    }

    if auth_status == 'auth_success':
        return True
    else:
        cmd = command_dict[auth_status]
        logging.debug("Running auth function: " + str(cmd))
        cmd(client, msg)

def broadcast(client, msg):
    """
    Send msg to every client.
    """
    for client_target in CLIENT_LIST:
        if client_target != client:
            client_target.send(msg)

def _whos_online(client, msg):
    client.send("\nList of people who are currently online:\n")
    for client_name in CLIENT_LIST:
        user_id = CLIENT_STATE[client_name]['user_id']
        first_name = AUTH_DB[user_id]['first_name']
        last_name = AUTH_DB[user_id]['last_name']
        client.send("\n-")
        client.send(" ".join([first_name, last_name]))
    client.send("\n\n")

def _new_post(client, msg):
    pass

def _facedup(client, msg):
    pass

def _inmyface(client, msg):
    pass

def _outtamyface(client, msg):
    pass

def _about_me(client, msg):
    user_id = CLIENT_STATE[client]['user_id']
    fn = AUTH_DB[user_id]['first_name']
    ln = AUTH_DB[user_id]['last_name']
    client.send("\nYour user_id is: " + user_id)
    client.send("\nYour Name is: %s %s" % (fn, ln))
    client.send("\n")

def _read_posts(client, msg):
    pass

def _quit(client, msg):
    client.active = False

def _draw_main_menu(client, commands):
    """pass the client, and the list of commands, to draw the main menu page
    """
    client.send("\n")
    client.send_wrapped("~=" * 20)
    client.send(" " * 16 +"Welcome to " + PRODUCT_NAME + "\n")
    client.send_wrapped("~=" * 20)
    client.send("\n")
    client.send(" | ".join(commands))
    client.send("\n")

def _main_menu(client, msg):
    logging.debug("Client %s at main menu" % (CLIENT_STATE[client]['user_id']))
    commands = {'whos_online':_whos_online,
                'new_post':_new_post,
                'facedup': _facedup,
                'inmyface': _inmyface,
                'outtamyface': _outtamyface,
                'about_me': _about_me,
                'read_posts': _read_posts,
                'quit': _quit,
                }

    _draw_main_menu(client, commands.keys())

    if commands.has_key(msg):
        cmd = commands.get(msg)
        cmd(client, msg)
    else:
        client.send("Please enter a command: ")

def msg_processor(client):
    """
    """
    global SERVER_RUN
    msg = client.get_command()
    logging.debug('%s says, "%s"' % (client.addrport(), msg))

    print CLIENT_STATE

    if msg == "":
        return

    if msg == 'debug':
        print CLIENT_STATE
        print AUTH_DB
        print CLIENT_LIST
        return


    if not CLIENT_STATE[client].has_key('auth_retry'):
        CLIENT_STATE[client]['auth_retry'] = 0

    if auth(client, msg):
        logging.info("Client %s logged in." % (CLIENT_STATE[client]['user_id']))
        _main_menu(client, msg)
    else:
        logging.debug("Client not logged in")
        if CLIENT_STATE[client]['auth_retry'] > AUTH_RETRY:
            logging.debug("Kicked %s for too many login attempts." % (client.addrport()))
            client.active = False



#    for guest in CLIENT_LIST:
#        if guest != client:
#            guest.send('%s says, %s\n' % (client.addrport(), msg))
#        else:
#            guest.send('You say, %s\n' % msg)
#    ## bye = disconnect
#    if cmd == 'bye':
#        client.active = False
#    ## shutdown == stop the server
#    elif cmd == 'shutdown':
#        SERVER_RUN = False


#------------------------------------------------------------------------------
#       Main
#------------------------------------------------------------------------------

if __name__ == '__main__':

    telnet_server = TelnetServer(
        port=7777,
        address='',
        on_connect=on_connect,
        on_disconnect=on_disconnect,
        timeout = .05
        )

    logging.info("Listening for connections on port %d.  CTRL-C to break."
        % telnet_server.port)

    ## Server Loop
    while SERVER_RUN:
        telnet_server.poll()        ## Send, Recv, and look for new connections
        kick_idle()                 ## Check for idle clients
        process_clients()           ## Check for client input
        sleep(0.1)

    logging.info(">> Server shutdown.")
