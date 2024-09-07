Scenario Outline: Successful retrieval of a user by ID
  Given a user exists with ID "1"
  When I send a GET request to "<url>"
  Then I should receive a response with status code "<status_code>"
  And the response should contain the field "username"
  And the response should contain the field "first_name"
  And the response should contain the field "last_name"
  And the response should contain the field "email"
  And the response should contain the field "phone"
  And the response should contain the field "position"
  And the response should contain the field "project"
  Examples:
    | url              | status_code |
    | /api/v1/users/1/ | 200         |
