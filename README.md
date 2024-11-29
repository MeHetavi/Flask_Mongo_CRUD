# Flask_Mongo_CRUD

1.Clone the repository

2.Build and Run the Application
- Install requirements.txt
- Build and run docker.

3.Postman Testing
- Import the Postman collection
- Send requests to http://localhost:5000/users

4.API Endpoints
- GET /users: List all users
- GET /users/<id>: Get a specific user
- POST /users: Create a new user
- PUT /users/<id>: Update an existing user
- DELETE /users/<id>: Delete a user

5.Validation
- Passwords must be at least 8 characters.
- Includes letter, number, and special character.
- Email must be in valid format.
- Same email cannot be registered again.