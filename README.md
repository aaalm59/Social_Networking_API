# Social_Networking_API


API Functionalities:

Search Users API:

Endpoint: /api/search-users/
Method: GET
Description: Search for other users by email and name with pagination (10 records per page).
Request Parameters:
search_keyword (string): The keyword to search for (either name or email).
Response:
If the search keyword matches an exact email, return the user associated with that email.
If the search keyword contains any part of the name, return a list of all matching users.
Paginate the results (10 records per page).
Friend Request API:

Endpoint: /api/friend-request/

Method: POST

Description: Send a friend request to another user.

Request Parameters:

receiver_email (string): Email of the user to whom the friend request is sent.
Response:

Success message on successful request submission.
Endpoint: /api/accept-friend-request/<int:request_id>/

Method: POST

Description: Accept a friend request.

Request Parameters:

request_id (integer): ID of the friend request to accept.
Response:

Success message on successful acceptance.
Endpoint: /api/reject-friend-request/<int:request_id>/

Method: POST

Description: Reject a friend request.

Request Parameters:

request_id (integer): ID of the friend request to reject.
Response:

Success message on successful rejection.
List Friends API:

Endpoint: /api/list-friends/
Method: GET
Description: List all friends (users who have accepted friend requests).
Response:
List of friend users.
List Pending Friend Requests API:

Endpoint: /api/list-pending-requests/
Method: GET
Description: List all pending friend requests (received friend requests).
Response:
List of pending friend requests.
Friend Request Rate Limit API:

Endpoint: /api/friend-request-rate-limit/
Method: GET
Description: Check if the user can send a friend request (limit: 3 requests per minute).
Response:
Success message if the user is allowed to send a friend request, otherwise an error message.
