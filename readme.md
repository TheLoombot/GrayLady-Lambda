# Dependencies
-- python 2.7
-- all other dependencies are inside of the project

# Deployment

**Note** Please open file contentful.py in root directory for point 1-2-3
1. access_token = 'ce03285b239a8bebc753266729ec5f8bbaf28dedba2d63721728ce850af99f09'
-- scroll down and search button with **Login to get a token button** text on [this page][1]
-- sign in and again scroll down on same location - new token will be there instead of button

[1]: https://www.contentful.com/developers/docs/references/authentication/#the-management-api/

2. space_id = 'clmzlcmno5rw'
-- this is the space in which you want to add briefings and pieces
-- open your space in browser and you can find this in url. for example
https://app.contentful.com/spaces/**clmzlcmno5rw**/
-- please note that the access token must be from same account as the space id

3. locale = 'en-US'
-- no need to change this
-- might be useful for translation in future

4. Just zip everything and upload to lambda
5. Please change **Handler** in *AWS Lambda* configuration to 'handler.lambda_handler'
6. In *AWS Lambda* advance settings please change **Timeout** to 5 minutes
7. *AWS Lambda* is too fast and sometimes second request fires so quicckly that the first request isn't comepletly handled by Contenful -- 3 second delay is add to resolve this issue

# Code
1. *lambda.py*
-- main file - handle lambda event
2. *nytimes.py*
-- parse briefings and pieces from nytimes based on news link
-- returns briefings and pieces
3. *contentful.py*
-- send all pieces and briefings to contentful via API
-- Contentful creation, process and publishing - everything is done in this file

# Tesing
-- there is a test.py file contains a dummy raw email to test
-- to test just run
~~~~
python test.py
~~~~