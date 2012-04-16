import os
import persist

class FaceData(object):
    data = {}
    def __init__(self):
        self.persist = os.path.dirname(__file__) + '/face_data.pickle'
        self.save_every = 3

    def load(self):
        try:
            FaceData.data = persist.load(self.persist)
        except:
            FaceData.data = {}

    def save(self):

        if self.save_every <= 1:
            persist.save(FaceData.data, self.persist)
            self.save_every = 3
        else:
            self.save_every -= 1

    def reset(self):
        FaceData.data = {}

    def init_user(self, user_id):
        return FaceData.data.setdefault((user_id,), {})

