# Flask-JWT-File-Upload

[![Build Status](https://travis-ci.com/bera5186/Flask-JWT-File-Upload.svg?branch=master)](https://travis-ci.com/bera5186/Flask-JWT-File-Upload)

A flask web application for uploading file with following features in it's backend API

* JWT based authentication system where token expires in 20 minutes

* User registration using MongoDb
* Only registered user will be able to get token
* The upload route '/upload' is protected and you need to have an access token to upload file
* API rate limiting is also done on '/upload' route with limit of 5 calls per minute
* Passwords are stored in encrypted way

Fire the command in command line
```python
 python app.py
```
this will run the server at http:127.0.0.1:5000/
