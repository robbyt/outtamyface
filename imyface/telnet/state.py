import logging
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

CLIENT_LIST = []
CLIENT_STATE = {}

class ClientListAction(Exception):
    pass

class WrongType(Exception):
    pass

def connect(telnet_client):
    global CLIENT_LIST
    global CLIENT_STATE
    client = Client(telnet_client)
    CLIENT_LIST.append(client)
    CLIENT_STATE[client] = {}
    logging.debug("Added client %s to client list" % str(client))
    return client

def disconnect(client):
    global CLIENT_LIST
    global CLIENT_STATE
    if isinstance(client, Client):
        client.client.active = False
        try:
            CLIENT_LIST.remove(client)
            del(CLIENT_STATE[client])
        except ValueError:
            logging.warn("\
Error: Client %s not found in client list, cannot remove." % str(client))
    else:
        logging.debug("Disconnect was sent a non-client object")
        raise WrongType
    
def kick_idle():
    """
    Looks for idle clients and disconnects them by setting active to False.
    """
    for c in CLIENT_LIST:
        if c.client.idle() > c.idle_timeout:
            logging.info('Kicking idle client %s' % c.client.addrport())
            disconnect(c)

def in_client_list(client):
    return client in CLIENT_LIST


class Client(object):
    def __init__(self, client, state=None, timeout=600):
        self.client = client
        self.idle_timeout = timeout
        self.user_id = None
        self.auth_retry = 0

        if state is None:
            self.state = {}
        else:
            self.state = state

    def __str__(self):
        if self.user_id is None:
            return str(self.client)
        else:
            return str(self.user_id)

    def _set_state(self, application, state):
        """ Used for updating the client's state. This is a very commonly used
            function in this application, since the user's state controls their
            location in the program.
        """
        logging.debug("Setting %s_state for %s" % (application, str(self.client)))
        self.state[application + '_state'] = state

    def _get_state(self, application):
        """ Lookup and return the client's state. This is very common, since
            the state controls the user's location within the program.
        """
        logging.debug("Looking up %s_state for %s" % (application, str(self.client)))
        return self.state.get(application + '_state', None)

    def initialize_client_state(self):
        """ Used when a new client logs in, to setup a new root key, and reset
            any old state data that might be hanging around. 
        """
        self.state = {}
        logging.debug("Initialized a new client state for %s" % str(self.client))

    def set_auth_state(self, state):
        states = ['startup', 'set_pass', 'auth_lookup', 'enroll_start', 
                  'enroll_user', 'enroll_pass', 'enroll_pass2', 
                  'enroll_first_name', 'enroll_last_name', 'enroll_save',
                  'auth_success']

        if state in states:
            self._set_state("auth_status", state)

    def get_auth_state(self):
        return self.get_state('auth_status')

