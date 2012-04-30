import logging
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
logging.debug("Setup logging")

from state import State
CLIENT_STATE = State()

def enroll(client, msg):
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

