# DuckTalk API

This file documents how to use the API and what requests are available. 

## Common patterns

All common patterns are from the clients' perspective.

### User creation

- Ask user for email/password
- Create salt
- hash password using salt
- send the email, hashed password and salt to the server using a [user](#apiuser) POST request

### User login

- Ask user for email/password
- Request the users salt from the server using a [salt](#apisalt) GET request
- hash the password using the salt
- Request a token from the server, using the email and hashed password in a [token](#apitoken) GET request
- Save the received token, because it is needed for all further requests

### User logout

- Send a [token](#apitoken) DELETE request for token deletion to the server
- Delete the saved token
- Return to the login page

## Data objects

### Message

- "message_id": 15 (The unique id of the message)
- "sender_id": 225 (The id of the message sender)
- "receiver": (A dictionary of data about the receiver of the message)
    - "type": "user" (The type of message receiver, either "user" or "group")
    - "user_id": 92 (The id of the receiver, the key is either user_id or group_id)
- "content": "6ekd980optak1" (The encrypted message content)

### User

- "user_id": 52 (The unique id of the user)
- "username": "TestUser" (The username chosen by the user)
- "publickey": "MIIBIjANBgkqhkiG9w0BAQEFAA" (The public key of the user used to encrypt messages sent to the user)

### Group

- "group_id": 14 (The unique id of the group)
- "groupname": "TestGroup" (The name of the group)
- "description": "A group for testing purposes" (The description of the group)
- "members": (A dictionary of group member ids)
    - 0: (A dictionary representating a group members)
        - "user_id": 42 (The user id of a group member)
        - "admin": False (A boolean value whether the user has admin rights in the group)
    - 1: (A dictionary representating a group members)
        - "user_id": 73 (The user id of a group member)
        - "admin": True (A boolean value whether the user has admin rights in the group)
    - 2: (A dictionary representating a group members)
        - "user_id": 61 (The user id of a group member)
        - "admin": False (A boolean value whether the user has admin rights in the group)

## REST API

### Overview

- [/api/salt](#apisalt)
    - GET
- [/api/token](#apitoken)
    - GET
    - DELETE
- [/api/message](#apimessage)
    - GET
    - POST
    - DELETE
- [/api/user](#apiuser)
    - GET
    - POST
    - DELETE
- [/api/group](#apigroup)
    - GET
    - POST
    - DELETE

### /api/salt

#### GET

Client: 

- "type": "salt" (Defines what is requested)
- "data": (A dictionary containing the request data)
    - "email": "testuser@mail.com" (The user email)

Returns:

- "error": True | False (boolean value whether the request raised an error)
- "data": (A dictionary containing the resulting data, or a string containing the error message)
    - "salt": "" (The salt to be used for password hashing)

### /api/token

#### GET

Client:

- "type": "token" (Defines what is requested)
- "auth": (A dictionary containing authentification data)
    - "type": "password" (The type of authentification)
    - "email": "testuser@mail.com" (The user email)
    - "pw_hash": "" (The hashed user password)

Returns:

- "error": True | False (boolean value whether the request raised an error)
- "data": (A dictionary containing the resulting data, or a string containing the error message)
    - "token": "" (The token used to authentificate as the user)

#### DELETE

Client:

- "type": "token" (Defines what is requested)
- "auth": (A dictionary containing the request data)
    - "type": "token" (The type of authentification)
    - "token": "" (The token to be invalidated)

Returns:

- "error": True | False (boolean value whether the request raised an error)
- "data": (An empty dictionary, or a string containing the error message)

### /api/message

#### GET

Client:

- "type": "message" (Defines what is requested)
- "auth": (A dictionary containing authentification data)
    - "type": "token" (The type of authentification)
    - "token": "" (The token that was received before)
- "data": (A dictionary containing the request data)
    - "message_id": 15 (The id of the requested message)

Returns:

- "error": True | False (boolean value whether the request raised an error)
- "data": (A dictionary containing the resulting data, or a string containing the error message)
    - "message": [message](#message)

#### POST

Sends a new message.

Client:

- "type": "message" (Defines what is requested)
- "auth": (A dictionary containing authentification data)
    - "type": "token" (The type of authentification)
    - "token": "" (The token that was received before)
- "data": (A dictionary containing the request data)
    - "receiver": (A dictionary of data about the receiver of the message)
        - "type": "user" (The type of message receiver, either "user" or "group")
        - "user_id": 92 (The id of the receiver, the key is either user_id or group_id)
    - "content": "6ekd980optak1" (The encrypted message content)

Returns:

- "error": True | False (boolean value whether the request raised an error)
- "data": (A dictionary containing the resulting data, or a string containing the error message)
    - "message_id": 89 (The id of the sent message)

#### DELETE

Client:

- "type": "message" (Defines what is requested)
- "auth": (A dictionary containing authentification data)
    - "type": "token" (The type of authentification)
    - "token": "" (The token that was received before)
- "data": (A dictionary containing the request data)
    - "message_id": 38 (The id of the message to be deleted)

Returns:

- "error": True | False (boolean value whether the request raised an error)
- "data": (An empty dictionary, or a string containing the error message)

### /api/user

#### GET

Client:

- "type": "user" (Defines what is requested)
- "auth": (A dictionary containing authentification data)
    - "type": "token" (The type of authentification)
    - "token": "" (The token that was received before)
- "data": (A dictionary containing the request data)
    - "user_id": 15 (The id of the requested user)

Returns:

- "error": True | False (boolean value whether the request raised an error)
- "data": (A dictionary containing the resulting data, or a string containing the error message)
    - "user": [user](#user)

#### POST

Client:

- "type": "user" (Defines what is requested)
- "data": (A dictionary containing the request data)
    - "username": "Test User" (The username)
    - "email": "testuser@mail.com" (The user email, has to be unique)
    - "pw_hash": "" (The hashed user password)
    - "salt": "" (The password hashing salt for the created user)

Returns:

- "error": True | False (boolean value whether the request raised an error)
- "data": (An empty dictionary, or a string containing the error message)

#### DELETE

Client:

- "type": "user" (Defines what is requested)
- "auth": (A dictionary containing authentification data)
    - "type": "token" (The type of authentification)
    - "token": "" (The token that was received before)

Returns:

- "error": True | False (boolean value whether the request raised an error)
- "data": (An empty dictionary, or a string containing the error message)

### /api/group

#### GET

Client:

- "type": "group" (Defines what is requested)
- "auth": (A dictionary containing authentification data)
    - "type": "token" (The type of authentification)
    - "token": "" (The token that was received before)
- "data": (A dictionary containing the request data)
    - "group_id": 38 (The id of the requested group)

Returns:

- "error": True | False (boolean value whether the request raised an error)
- "data": (A dictionary containing the resulting data, or a string containing the error message)
    - "group": [group](#group)

#### POST

Creates a new group and adds the user sending the request as an admin.

Client:

- "type": "group" (Defines what is requested)
- "auth": (A dictionary containing authentification data)
    - "type": "token" (The type of authentification)
    - "token": "" (The token that was received before)
- "data": (A dictionary containing the request data)
    - "groupname": "TestGroup" (The name of the new group)
    - "description": "This is another test group" (The description of the new group, can be empty)

Returns:

- "error": True | False (boolean value whether the request raised an error)
- "data": (A dictionary containing the resulting data, or a string containing the error message)
    - "group_id": 89 (The id of the new group)

#### DELETE

Client:

- "type": "group" (Defines what is requested)
- "auth": (A dictionary containing authentification data)
    - "type": "token" (The type of authentification)
    - "token": "" (The token that was received before)
- "data": (A dictionary containing the request data)
    - "group_id": 38 (The id of the group to be deleted)

Returns:

- "error": True | False (boolean value whether the request raised an error)
- "data": (An empty dictionary, or a string containing the error message)
