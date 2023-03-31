

## Routes

1. /login[POST] {email, password}
2. /signup[POST] {email, password, name}
3. /reset-password [POST] {email, new_password, otp}
4. /send-otp [GET] {email}
5. /update-account [POST] {user_id, name, email, password}

6. /request-aid [POST] {user_id, description, location, image}
7. /get-requests [GET] {user_id[optional], status[optional]}



## Models

### User
- name
- email
- password

### Request
- user_id
- description
- location
- image_url[optional]
- status [ongoing, past, cancelled]
