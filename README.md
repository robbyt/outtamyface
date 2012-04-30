OuttaMyFace
=============
This is an example of an in-memory graph database.


Working with this lib
-----------------------

### Run nosetests
```bash
$ nosetests
```

### Load up the demo data:
```python

import cPickle as pickle
from imyface import user, actions, connect

cons_file = 'demo_data/data4_connections__larger.dat.pickle'
users_file = 'demo_data/data4_faces__larger.dat.pickle'

fp_cons = open(cons_file)
fp_users = open(users_file)
users_list = pickle.load(fp_users)
cons_list = pickle.load(fp_cons)

user.enroll_list(users_list)
connect.connect_list(cons_list)
```

### Get a list of all users:
```python
print user.get_all_users()
# sorted list of users:
print user.get_all_users(sort_list=True)
```

### Enroll a new user:
```python
user.enroll(first_name='Charlos',
            last_name='Smith',
            user_id='csmith',
            password='god',)
```

### Connect two users:
```python
user = 'csmith'
# SRautela3 is included in the demo data
face = 'SRautela3'
connect.outta_my_face(user, face)
```

### Test to see if two users are connected:
```python
actions.is_outta_my_face('JLam2', 'JHinkes1')
# or test the reverse
actions.is_in_my_face('JLam2', 'JHinkes1')
```

### Return the path between two users:
```python
actions.find_path('ZLee1', 'ZNagy1')
# or find the shortest path:
actions.find_path('ZLee1', 'ZNagy1', find_shortest=True)
```

### Return the intersection between two users:
```python
actions.face_space('CFeinstein1', 'VKuchibhotla1')
```
