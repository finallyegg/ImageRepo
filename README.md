# ImageRepo

# Running the database
 - `in IMAGEREPO` 
 - `docker-compose up` (must have docker installed)

# Running the backend
 - Install required dependencies 
    `pip3 install -r requirements.txt`

 - Install database schema 
    Use the --reinstall-schema option to configure database.
    `python3 run_dev_server.py --reinstall-schema`

 - Start 
   `python3 run_dev_server.py `

# How to Use
 - Run Both Database and Backend localhost:5666
 - Use Postman or similiar app to communicate with the server

# Register User
 - Send POST to 'http://127.0.0.1:5666/register'
 - In Request Body, Include Following format
 - `
 {
  "name": "YOUR USERNAME",
  "password": PASSWORD,
  "email": EMAIL ADDR"
 }`

# Test
 - Run 
   `python3 tests/apiTests/run_test.py `

# Features and Challenges
 - Prevent UnAuthorized Access and Operation by adding `jwt-token` to each API route
 - Ensure secured uploading and storing by split each image into fixed size chunk, store there reference using sha256 hash
 - secure deletion are managed by blobs manager (in case, users are uploading same images)
 - LRU cache with 