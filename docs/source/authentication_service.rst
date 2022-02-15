
Authentication service
======================

In the authentication service, the identity of users is checked for providing the access to the system. 

Endpoints
---------------------

..  http:example:: curl wget httpie python-requests

    POST /login
    Host: host
    Accept: application/json
    Payload: {"email":"example@email.com", "password":"funtimes"}

..  http:example:: curl wget httpie python-requests
    POST /google_login
    Host: host
    Accept: application/json
    Payload: {"email":"example@email.com", "password":"funtimes"}

..  http:example:: curl wget httpie python-requests

    POST /facebook_login
    Host: host
    Accept: application/json
    Payload: {"email":"example@email.com", "password":"funtimes"}

..  http:example:: curl wget httpie python-requests

    POST /logout
    Host: host
    Accept: application/json
    Payload: {"email":"example@email.com", "password":"funtimes"}