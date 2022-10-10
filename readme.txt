
Hi Team, 

I have created the "address-book" api to fullfill the requirements as specified in the assignment but there are few things i would like to highlight before you test out the application.

1 -> Application which I have built is using Postgres database as I have good command over Postgres and have used it in my previous applications as well so had better understanding of integrating it with FastAPI and working with it.

2 -> I have implement the feature of "geocoding" into the api to fetch out the contacts nearby the current user (user just have to provide their current location and the radius they wanna scan for, their is a schema defined for providing input details). I am using GeoPy library to fetch the location of a given address which can subsequently get me the latitude and longitude of that particular address which i can then store in my postgres database. The related logic for this feature as well as how i am calculating the distance and executing other utilities can be found in app/routers/addresses.py , The path operations using this logic are create_contact, update_Contact, retrieve_contacts.

3 -> As the application is not deployed anywhere, I request you to install "PGADMIN4" on your machine to test out the application functionality with database. When you create the server and database on pgadmin4, use below credentials, so when you run the application, it would create tables on the database.
            Username : postgres
            Password : password123
            hostname : localhost
            port : 5432
            database name: postgres

4 -> Also attached is the snapshot of "PGadmin4 server settings" on the root page of github url for this code. Kindly refer to it for database setup.

///
Steps tp run the application:

Once you have downloaded the code and created a database on PGAdmin4 with the above credentials, kindly follow below steps:

The first step is to install the dependencies which you can find in "requirements.txt" file that I have uploaded alongside the project files.
Create a virtual environment first and then install dependencies in it.
To create a virtual environment, open a terminal (make sure you are in the root directory) and run following commands:
 1) pip install virtualenv
 2) virtualenv "any name"
 3) Activate the virtual environment by : name_you_have_Chosen\Scripts\activate.bat

Once the virtual environment is activated, run the followiing command on your terminal --> "pip install -r requirements.txt (Python 2), or pip3 install -r requirements.txt (Python 3)", This will install the dependencies from 'requirements.txt' inside this virtual environement.

Go to the project directory on terminal and run below command to run the server and test out the swagger docs for it:
*** uvicorn app.main:app --reload ***

Once the server is up and running search the url http://127.0.0.1:8000 in your browser and test out the api.
As a first step, create a user as per the schema mentioned, then login as that user (Use authorization tab at top right corner of the docs to login) and then create few contacts.
Make sure before testing out each endpoint you are logged in as that user and only then you can test it.

***
Example scenario of API working:

Multiple users can use the application, they just have to create a user with email id and password.
And using these credentials users can access the endpoints to use the functionality of creating new contacts,updating exisiting contacts , retrieving contacts within a given radius and other CRUD functionalities of Address-book application.

IF there are 2 users (Sid and Aman) , then suppose Sid creates his contacts with ids 1,2,3 and Aman creates his contacts with ids 4,5.
Then if Sid tries to view,update or delete contacts with ids 4 and 5, he wont be able to do so and vice versa.
Users can only view,update and delete those contacts where they are the owners on the contacts(i have created Owner_id field in Contact models which links up with User model for such validations)

Every account created by an user will be an unique account as one acount depends on one email and we have provided an unique constraint to our email field. No user can create different accounts on our API using same email.
***

NOTE: I have tested all the endpoints and they are working fine as per my testing of different edge cases. If you face any difficulty while initial setup of the application or testing the functionality, kindly connect with me at "sidraw122@gmail.com"
///

APPLICATION details:

-> Models using : 2 
    - Contact and User
    - Contact to store the full contact info in the database
    - User to store the users info on database

-> EndPoint Instances : 3
    - routers/addresses.py consisting of endpoints for fetching all,fetching single,deleting and updating the contacts for the users with owner id same as the user id to make sure only authenticated people could use the endpoints on their own contacts. This file also has an endpoint named "retrieve_contacts" which the user can use to find out the nearby contacts as per the radius they have chosen.

    -routers/auth.py consisting the login endpoint to login the user to authenticate themselves and only then they could use the API features.

    -routers/users.py consisting the create and get user endpoint to create and fetch the user from the database.

Extra Features:

** I have integrated JWT authentication for User login and created dependencies on the routers/addresses.py endpoints so that only logged in users when their JWT token is verified can only access the endpoints and no other people can. Token creation, verfication and dependencies have been created in app/Oauth2.py file.

** I have tried to cover all the edge cases while creating,fetching,deleting and updating the contacts from the database.

** Have specified Pydantic Schema models to make sure the POST requests and JSON responses from our API are prevalidated and strictly follow the   schema structure to not make any conflict between the API and client regarding the data.

** I have also created the utils.py file to hash the passwords and store it in the database for users using passlib[bcrypt] package.

Thanks for reading :D