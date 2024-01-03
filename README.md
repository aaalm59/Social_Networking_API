**Without Docker**
Create a virtual environment:
python -m venv venv
Activate the virtual environment:
On Windows:
venv\Scripts\activate
On Unix or MacOS:
source venv/bin/activate
Install dependencies:
pip install -r requirements.txt
Navigate to project directory /app
cd Social_Networking_API
Apply migrations:
python manage.py migrate
Run the development server:
python manage.py runserver
Visit the server URL in the browser with port 8000
127.0.0.1:8000










API Functionalities:

User Authentication:

User Signup: POST /api/signup/
User Login: POST /api/login/
User Search:

Search Users: GET /api/search/?keyword=<search_keyword>
Friend Requests:

Send Friend Request: POST /api/send-friend-request/<int:receiver_id>/
Accept Friend Request: POST /api/accept-friend-request/<int:request_id>/
Reject Friend Request: POST /api/reject-friend-request/<int:request_id>/
Friends List:

List Friends: GET /api/friends-list/
Pending Friend Requests:

List Pending Friend Requests: GET /api/pending-friend-requests/
Remember to include the appropriate authentication headers (e.g., Token-based authentication) in your requests to access the authenticated endpoints. Adjust the URLs based on your project structure and preferences.

Here's a brief explanation of each endpoint:

User Authentication:

POST /api/signup/: User registration endpoint.
POST /api/login/: User login endpoint.
User Search:

GET /api/search/?keyword=<search_keyword>: Search for users by email or name.
Friend Requests:

POST /api/send-friend-request/<int:receiver_id>/: Send a friend request to the user with the specified ID.
POST /api/accept-friend-request/<int:request_id>/: Accept a friend request with the specified ID.
POST /api/reject-friend-request/<int:request_id>/: Reject a friend request with the specified ID.
Friends List:

GET /api/friends-list/: Retrieve the list of friends for the authenticated user.
Pending Friend Requests:

GET /api/pending-friend-requests/: Retrieve the list of pending friend requests for the authenticated user.
