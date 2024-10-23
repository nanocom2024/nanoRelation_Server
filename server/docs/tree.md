# tree

<pre>
.
├── Makefile
├── README.md
└── server
    ├── Makefile
    ├── README.md
    ├── __pycache__
    │   ├── main.cpython-311.pyc
    │   └── settings.cpython-311.pyc
    ├── nanorelation-firebase-adminsdk-5likk-6701336996.json
    ├── requirements.txt
    ├── src
    │   ├── Auth
    │   │   ├── UsersModel.py
    │   │   ├── __pycache__
    │   │   │   ├── Auth.cpython-311.pyc
    │   │   │   ├── UsersModel.cpython-311.pyc
    │   │   │   ├── firebase.cpython-311.pyc
    │   │   │   └── routes.cpython-311.pyc
    │   │   ├── firebase.py
    │   │   └── routes.py
    │   ├── Child
    │   │   ├── ChildrenModel.py
    │   │   ├── __pycache__
    │   │   │   ├── ChildrenModel.cpython-311.pyc
    │   │   │   └── routes.cpython-311.pyc
    │   │   └── routes.py
    │   ├── DB.py
    │   ├── LostChild
    │   │   ├── LogLostChildrenModel.py
    │   │   ├── LostChildrenModel.py
    │   │   ├── __pycache__
    │   │   │   ├── ChildrenModel.cpython-311.pyc
    │   │   │   ├── LogLostChildrenModel.cpython-311.pyc
    │   │   │   ├── LostChildrenModel.cpython-311.pyc
    │   │   │   └── routes.cpython-311.pyc
    │   │   └── routes.py
    │   ├── Notification
    │   │   ├── NotificationModel.py
    │   │   ├── __pycache__
    │   │   │   ├── NotificationModel.cpython-311.pyc
    │   │   │   └── routes.cpython-311.pyc
    │   │   └── routes.py
    │   ├── Pairing
    │   │   ├── PairingModel.py
    │   │   ├── __pycache__
    │   │   │   ├── PairingModel.cpython-311.pyc
    │   │   │   └── routes.cpython-311.pyc
    │   │   └── routes.py
    │   ├── StreetPass
    │   │   ├── NotificationModel.py
    │   │   ├── __pycache__
    │   │   │   ├── LostChildrenModel.cpython-311.pyc
    │   │   │   ├── NotificationModel.cpython-311.pyc
    │   │   │   └── routes.cpython-311.pyc
    │   │   └── routes.py
    │   ├── User
    │   │   ├── LogLostPassesModel.py
    │   │   ├── LogModel.py
    │   │   ├── LogNearOwnChildrenModel.py
    │   │   ├── LogOwnModel.py
    │   │   ├── LogPassesModel.py
    │   │   ├── __pycache__
    │   │   │   ├── LogLostPassesModel.cpython-311.pyc
    │   │   │   ├── LogModel.cpython-311.pyc
    │   │   │   ├── LogNearOwnChildrenModel.cpython-311.pyc
    │   │   │   ├── LogOwnModel.cpython-311.pyc
    │   │   │   ├── LogPassesModel.cpython-311.pyc
    │   │   │   └── routes.cpython-311.pyc
    │   │   └── routes.py
    │   ├── __pycache__
    │   │   ├── DB.cpython-311.pyc
    │   │   ├── handlers.cpython-311.pyc
    │   │   ├── init_server.cpython-311.pyc
    │   │   └── settings.cpython-311.pyc
    │   ├── crypto
    │   │   ├── __pycache__
    │   │   │   └── generate.cpython-311.pyc
    │   │   └── generate.py
    │   ├── dbManager
    │   │   ├── delete_collections_in_db.py
    │   │   ├── for_iBeacon_debug.py
    │   │   ├── for_lost_debug.py
    │   │   ├── showCollections.py
    │   │   ├── showDBs.py
    │   │   └── show_users.py
    │   ├── handlers.py
    │   ├── init_server.py
    │   ├── main.py
    │   └── settings.py
    └── tests
        ├── __pycache__
        │   ├── conftest.cpython-311-pytest-7.4.3.pyc
        │   ├── test_NotificationModel.cpython-311-pytest-7.4.3.pyc
        │   ├── test_auth.cpython-311-pytest-7.4.3.pyc
        │   ├── test_generate_keypair.cpython-311-pytest-7.4.3.pyc
        │   ├── test_hello.cpython-311-pytest-7.4.3.pyc
        │   ├── test_lost_child.cpython-311-pytest-7.4.3.pyc
        │   ├── test_notification.cpython-311-pytest-7.4.3.pyc
        │   ├── test_pairing.cpython-311-pytest-7.4.3.pyc
        │   └── test_streetpass.cpython-311-pytest-7.4.3.pyc
        ├── conftest.py
        ├── test_auth.py
        ├── test_generate_keypair.py
        ├── test_lost_child.py
        ├── test_notification.py
        ├── test_pairing.py
        └── test_streetpass.py
</pre>
