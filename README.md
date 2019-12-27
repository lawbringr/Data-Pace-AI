# DataPaceAI
Data Pace Internship Assignment 

Used Postman as mock server for testing API response

# How to run the project
## Install dependencies
```python
pip install -r requirements.txt
```
## Start MongoDB Server
To start MongoDB Server in Windows, start Mongo Daemon (mongod.exe)
```cmd
C:\> "C:\Program Files\MongoDB\Server\4.2\bin\mongod.exe"
```
## Config the application
Change the `Database Name` in the config file according to the database name you are using.
Change the `userData.py` line no.14 and 16 and give respective `Database name` and `collection name`

## Start the application
```cmd
python run-app.py
```

Once the application is started, go to [localhost](http://localhost:5000/)
on Postman and explore the APIs.

# Following Endpoints are supported
1. http://127.0.0.1:5000/api/users - POST - To create a new user
2. http://127.0.0.1:5000//api/users/{id} - GET - To get the details of a user
3. http://127.0.0.1:5000//api/users/api/users?{Query} - GET - To list the users according to the query
4. http://127.0.0.1:5000//api/users/{id} - PUT - To update the details of a user (use $set parameter Example:
```{
	"$set": {
		"first_name": "Vishwas Saini"
	}
}
``` 
5. http://127.0.0.1:5000//api/users/{id} - DELETE - To delete the user