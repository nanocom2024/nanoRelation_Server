# tree

<pre>
.
├── Makefile
├── README.md
└── server
    ├── Makefile
    ├── README.md
    ├── nanorelation-firebase-adminsdk-5likk-6701336996.json
    ├── requirements.txt
    ├── src
    │   ├── Auth
    │   │   ├── UsersModel.py
    │   │   ├── firebase.py
    │   │   └── routes.py
    │   ├── Child
    │   │   ├── ChildrenModel.py
    │   │   └── routes.py
    │   ├── DB.py
    │   ├── LostChild
    │   │   ├── LogLostChildrenModel.py
    │   │   ├── LostChildrenModel.py
    │   │   └── routes.py
    │   ├── Notification
    │   │   ├── NotificationModel.py
    │   │   └── routes.py
    │   ├── Pairing
    │   │   ├── PairingModel.py
    │   │   └── routes.py
    │   ├── StreetPass
    │   │   ├── NotificationModel.py
    │   │   └── routes.py
    │   ├── User
    │   │   ├── LogLostPassesModel.py
    │   │   ├── LogModel.py
    │   │   ├── LogNearOwnChildrenModel.py
    │   │   ├── LogOwnModel.py
    │   │   ├── LogPassesModel.py
    │   │   └── routes.py
    │   ├── crypto
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
        ├── conftest.py
        ├── test_auth.py
        ├── test_generate_keypair.py
        ├── test_lost_child.py
        ├── test_notification.py
        ├── test_pairing.py
        └── test_streetpass.py
</pre>
