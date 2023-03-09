# DuckTalk API

This file documents how to use the API and what requests are available. 

## Common patterns

All common patterns are from the clients' perspective.

### User creation

- Ask user for email/password
- Create salt
- hash password using salt
- send the email, hashed password and salt to the server using a [PUT](#create-a-user) request

### User login

- Ask user for email/password
- Request the users salt from the server using a [GET](#request-salt) request
- hash the password using the salt
- Request a token from the server, using the email and hashed password in a [GET](#request-token) request
- Save the received token, because it is needed for all further requests

### User logout

- Send a [PUT](#delete-token) request for token deletion to the server
- Delete the saved token
- Return to the login page

## REST API

### Data objects

#### Message

- "id": 15 (The unique id of the message)
- "sender_id": 225 (The id of the message sender)
- "receiver_ids": (A dictionary of receiver ids, only has one element for private messages)
    - 0: (A dictionary containing a receiver user id)
        - "receiver_id": 42 (The id of a message receiver)
    - 1: (A dictionary containing a receiver user id)
        - "receiver_id": 73 (The id of a message receiver)
    - 2: (A dictionary containing a receiver user id)
        - "receiver_id": 61 (The id of a message receiver)
- "content": "6ekd980optak1" (The encrypted message content)

### GET

#### Request salt

Client: 

- "request": "GET" (Defines the type of request)
- "type": "salt" (Defines what is requested)
- "data": (A dictionary containing the request data)
    - "email": "testuser@mail.com" (The user email)

Returns:

- "error": True | False (boolean value whether the request raised an error)
- "data": (A dictionary containing the resulting data, or a string containing the error message)
    - "salt": "" (the salt to be used for password hashing)

#### Request token

Client:

- "request": "GET" (Defines the type of request)
- "type": "token" (Defines what is requested)
- "auth": (A dictionary containing authentification data)
    - "type": "password" (the type of authentification)
    - "email": "testuser@mail.com" (The user email)
    - "pw_hash": "" (the hashed user password)

Returns:

- "error": True | False (boolean value whether the request raised an error)
- "data": (A dictionary containing the resulting data, or a string containing the error message)
    - "token": "" (the token used to authentificate as the user)

#### Request message

Client:

- "request": "GET" (Defines the type of request)
- "type": "message" (Defines what is requested)
- "auth": (A dictionary containing authentification data)
    - "type": "token" (the type of authentification)
    - "token": "" (the token that was received before)
- "data": (A dictionary containing the request data)
    - "message_id": 15 (the id of the requested message)

Returns:

- "error": True | False (boolean value whether the request raised an error)
- "data": (A dictionary containing the resulting data, or a string containing the error message)
    - "message": [message](#message)

### PUT

#### Create a user

Client:

- "request": "PUT" (Defines the type of request)
- "type": "user" (Defines what is requested)
- "data": (A dictionary containing the request data)
    - "email": "testuser@mail.com" (The user email)
    - "pw_hash": "" (the hashed user password)
    - "salt": "" (the password hashing salt for the created user)

Returns:

- "error": True | False (boolean value whether the request raised an error)
- "data": (An empty dictionary, or a string containing the error message)

### DELETE

#### Delete token

Client:

- "request": "PUT" (Defines the type of request)
- "type": "token" (Defines what is requested)
- "auth": (A dictionary containing the request data)
    - "type": "token" (the type of authentification)
    - "token": "" (the token to be invalidated)

Returns:

- "error": True | False (boolean value whether the request raised an error)
- "data": (An empty dictionary, or a string containing the error message)
