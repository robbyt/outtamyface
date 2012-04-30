import logging
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

self.idle_timeout = 600
StateStore.client_list = []
CLIENT_STATE = {}

class ClientListAction(Exception):
    pass


class State(object):
    client_list = []
    client_state = []
    def __init__(self, client):
        self.idle_timeout = 120
        self.client = client

    ## cleanup task run in the main loop
    def kick_idle(self):
        """
        Looks for idle clients and disconnects them by setting active to False.
        """
        for client in State.client_list:
            if client.idle() > self.idle_timeout:
                logging.info('Kicking idle client %s' % client.addrport())
                client.active = False

    def in_client_list(self, client):
        return client in State.client_list

    ## client_list functions 
    def set_client_list(self, client):
        """ When a new client logs in, add a reference to their client object in
            the client_list so that we know everyone who is logged in.
        """
        if self.in_client_list(client):
            logging.warn("\
Error: Client %s already client list, cannot add." % str(client))
        else:
            StateStore.client_list.append(client)
            logging.debug("Added client %s to client list" % str(client))

    def prune_client_list(client):
        """ Used for removing client objects from the StateStore.client_list
        """
        try:
            StateStore.client_list.remove(client)
            logging.debug("Removed client %s from client list" % str(client))
        except ValueError:
            logging.warn("\
    Error: Client %s not found in client list, cannot remove." % str(client))

    def get_client_list(client=None):
        if client is None:
            logging.debug("Reading full client list")
            return StateStore.client_list
        else:
            logging.debug("Reading client list data for " + str(client))
            return StateStore.client_list[client]

    ## client_state private functions
    def _set_client_state(client, key, value):
        """ Private function for setting client state
        """
        try:
            CLIENT_STATE[client][key] = value
        except KeyError:
            logging.warn("Failed to update client state, client root key does not exist")

    def _get_client_state(client, key):
        """ Private function for looking up client state
        """
        return CLIENT_STATE[client].get(key, None)

    ## client_state public functions 
    def initialize_client_state(client):
        """ Used when a new client logs in, to setup a new root key, and reset
            any old state data that might be hanging around. 
        """
        CLIENT_STATE[client] = {}
        logging.debug("Initialized a new client state for %s" % str(client))

    def prune_client_state(client):
        """ Private function for pruning unused state records
        """
        try:
            del(CLIENT_STATE[client])
            logging.debug("Pruned client state for %s" % str(client))
        except KeyError:
            logging.warn("Failed to remove client state, client already pruned.")

    ## related to the client's <application>_state for various internal 'apps'
    def set_state(client, application, state):
        """ Used for updating the client's state. This is a very commonly used
            function in this application, since the user's state controls their
            location in the program.
        """
        logging.debug("Setting %s_state for %s" % (application, str(client)))
        _set_client_state(client, application + '_state', state)

    def get_state(client, application):
        """ Lookup and return the client's state. This is very common, since
            the state controls the user's location within the program.
        """
        logging.debug("Looking up %s_state for %s" % (application, str(client)))
        return _get_client_state(client,  application + '_state')

    def get_user_id(client):
        return get_state(client, 'user_id')

    def get_auth_state(client):
        return get_state(client, 'auth')

