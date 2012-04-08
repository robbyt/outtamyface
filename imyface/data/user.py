import os
import persist

PERSIST_DATA = os.path.dirname(__file__) + '/user.mp'

try:
    USER_DATA = persist.load(PERSIST_DATA)

except:
    USER_DATA = {}

finally:
    persist.save(USER_DATA, PERSIST_DATA)

