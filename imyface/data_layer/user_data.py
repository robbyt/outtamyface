import os
import persist

class UserData(object):
    data = {}
    def __init__(self):
        self.persist = os.path.dirname(__file__) + '/user_data.pickle'
        self.save_every = 3

    def load(self):
        try:
            UserData.data = persist.load(self.persist)
        except:
            UserData.data = {}

    def save(self):

        if self.save_every <= 1:
            persist.save(UserData.data, self.persist)
            self.save_every = 3
        else:
            self.save_every -= 1

    def reset(self):
        UserData.data = {}

#USER_DATA = UserData()
