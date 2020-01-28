def run_api_server(host, port, database_url):
    pass

'''
The API:

GET /users
Returns the list of all the supported users, including their IDs and names only.


GET /users/user-id
Returns the specified user's details: ID, name, birthday and gender.

GET /users/user-id/snapshots
Returns the list of the specified user's snapshot IDs and datetimes only.|


GET /users/user-id/snapshots/snapshot-id
Returns the specified snapshot's details: ID, datetime, and the available results' names only (e.g. pose).


GET /users/user-id/snapshots/snapshot-id/result-name
Returns the specified snapshot's result in a reasonable format. You should support pose, color-image, depth-image and feelings, where anything that has large binary data should contain metadata only, with its data being available via some dedicated URL (that should be mentioned in its metadata), like so:
GET /users/user-id/snapshots/snapshot-id/color-image/data
'''