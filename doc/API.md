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
- [/api/user](#apiuser)
    - GET
    - POST
    - DELETE
- [/api/group](#apigroup)
    - GET
    - POST

### /api/salt

#### GET
Request the salt for password hashing of an existing account

Client: 

?email=someuser@mail.com

Returns:

- "error": True | False (boolean value whether the request raised an error)
- "data": (A dictionary containing the resulting data, or a string containing the error message)
    - "salt": "" (The salt to be used for password hashing)

### /api/token

#### GET
Request a new token

Client:

- "data": (A dictionary containing the request data)
    - "email": "testuser@mail.com" (The user email)
    - "pw_hash": "" (The hashed user password)

Returns:

- "error": True | False (boolean value whether the request raised an error)
- "data": (A dictionary containing the resulting data, or a string containing the error message)
    - "token": "" (The token used to authenticate as the user)

#### DELETE
Invalidate a client token

Client:

- "data": (A dictionary containing the request data)
    - "token": "" (The token to be invalidated)

Returns:

- "error": True | False (boolean value whether the request raised an error)
- "data": (An empty dictionary, or a string containing the error message)

### /api/message

#### GET

Get a message that's already sent

Client:

GET /api/message/<message_id>

Returns:

- "error": True | False (boolean value whether the request raised an error)
- "data": (A dictionary containing the resulting data, or a string containing the error message)
    - [message](#message)

#### POST

Send a new message

Client:

- "data": (A dictionary containing the request data)
    - "sender_id": 51 (The user_id of the sender)
    - "receiver": (A dictionary of data about the receiver of the message)
        - "type": "user" (The type of message receiver, either "user" or "group")
        - "user_id": 92 (The id of the receiver, the key is either user_id or group_id)
    - "content": "6ekd980optak1" (The encrypted message content)

Returns:

- "error": True | False (boolean value whether the request raised an error)
- "data": (A dictionary containing the resulting data, or a string containing the error message)
    - "message_id": 89 (The id of the sent message)

### /api/user

#### GET

Request a user by id

Client:

GET /api/user/<user_id>

Returns:

- "error": True | False (boolean value whether the request raised an error)
- "data": (A dictionary containing the resulting data, or a string containing the error message)
    - [user](#user)

Request a user by email

Client:

GET /api/user/<email>

Returns:

- "error": True | False (boolean value whether the request raised an error)
- "data": (A dictionary containing the resulting data, or a string containing the error message)
    - [user](#user)

#### POST

Create a new user

Client:

- "data": (A dictionary containing the request data)
    - "username": "Test User" (The username)
    - "email": "testuser@mail.com" (The user email, has to be unique)
    - "pw_hash": "" (The hashed user password)
    - "salt": "" (The password hashing salt for the created user)

Returns:

- "error": True | False (boolean value whether the request raised an error)
- "data": (A dictionary containing the resulting data, or a string containing the error message)
    - "user_id": 15 (The id of the created user)

#### DELETE

Delete a user

Client:

DELETE /api/user/<user_id>

Returns:

- "error": True | False (boolean value whether the request raised an error)
- "data": (An empty dictionary, or a string containing the error message)

### /api/group

#### GET

Get an existing group by its id

Client:

GET /api/group/<group_id>

Returns:

- "error": True | False (boolean value whether the request raised an error)
- "data": (A dictionary containing the resulting data, or a string containing the error message)
    - [group](#group)

#### POST

Create a new group and add the user sending the request as an admin.

Client:

- "data": (A dictionary containing the request data)
    - "groupname": "TestGroup" (The name of the new group)
    - "description": "This is another test group" (The description of the new group, can be empty)
    - "user_id": 52 (The id of the user creating the group)

Returns:

- "error": True | False (boolean value whether the request raised an error)
- "data": (A dictionary containing the resulting data, or a string containing the error message)
    - "group_id": 89 (The id of the new group)

#### DELETE

Delete a group

Client:

DELETE /api/group/<group_id>

Returns:

- "error": True | False (boolean value whether the request raised an error)
- "data": (An empty dictionary, or a string containing the error message)
