### Run
`pip install -r requirements.txt`

`export SENDGRID_API_KEY="Send grid API Key"`

`export FLASK_APP=app/application.py`

`flask run`

Swagger page loads and the entire application can be tested

### Workflow
 - create user
```bash
curl -X POST "http://127.0.0.1:5000/help_your_neighbor/v1/user/SomeID" -H "accept: application/json" -H "Content-Type: application/json" -d "{ \"first_name\": \"string\", \"last_name\": \"string\", \"address\": \"string\", \"email\": \"string\", \"mobile\": \"string\", \"lat_long\": \"string\", \"role\": \"string\"}"
```

 - Registration email would be sent with instructions to complete registration process
```bash
curl -X POST "http://127.0.0.1:5000/help_your_neighbor/v1/register/e55c3079-baea-4a8d-86c4-a6b41f1a0b67" -H "accept: application/json" -H "Content-Type: application/json" -d "{ \"username\": \"SomeID\", \"password\": \"asdadasasdasd\"}"
``` 

 -  Login with user and password
```bash
curl -X POST "http://127.0.0.1:5000/help_your_neighbor/v1/auth" -H "accept: application/json" -H "Content-Type: application/json" -d "{ \"username\": \"string\", \"password\": \"string\"}"

Response:
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL2hlbHB5b3VybmVpZ2hib3IuY29tLyIsInN1YiI6ImFiaGlyajg3IiwicmVnIjpudWxsLCJpYXQiOjE1ODc4OTY0NTMsImV4cCI6MTU4NzkwMDA1M30.IoX8WVncPQ1FojsaDx3xnnF9wUsU_fce2k8_rtRrHME"
}
```

 - This signed jwt token needs to be sent to all other APIs to authenticate [to request help/ to respond to it. Admin dash login/ dashboard etc] .
 - Eg: send HTTP header like `Authorization: bearer <token mentioned above>`  


### To Do List
    - [ ]   Replace temp database with real one
    - [ ]   Test Deployment
      
