# scheduler
"Python flask application that takes JSON-formatted schedule of a person as an input and outputs hours in more human-readable format ordered by day and start time. It also shows if there is a conflict in schedule". (UCLA Assignment)

To use this application, initiate virtual environemnt of your choice, such as:
\
`pipenv shell`
\
\
Run the scheduleAssignment script
\
`python scheduleAssignment.py`
\
\
Use Postman (https://www.getpostman.com) to send JSON input and view output. These settings are required:
```
POST http://127.0.0.1:5000/schedule
Body
raw JSON
header "Content-Type: application/json"
```
<img width="1407" alt="Screen Shot 2022-12-14 at 3 55 43 PM" src="https://user-images.githubusercontent.com/32961623/207741947-ae1d3842-fdaa-4407-878c-2bab27276954.png">


For more information on using Flask, check out this tutorial I followed: https://www.digitalocean.com/community/tutorials/processing-incoming-request-data-in-flask.
