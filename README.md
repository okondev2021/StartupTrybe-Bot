# StartupTrybe Idea Validation Backend

This is the backend for  StartupTrybe Idea Validation web application. It makes use of Json web token for authentication and google's gemini for validating user's ideas. The model takes two input [ideas, target market].

## Features
This project consists to 2 applications.
1. UserIdea app. This app handles makes of jwt to handle user authentication, token generation, token refresh. 
2. Validator ai. This app makes use of google gemini ai to validate user idea based on the metrics provided in the prompt, stores logged in user idea, target audience, model response in the database.  

## Installation

### You need to have python installed. Danke

1. **Clone the repository:**

    ```sh
    https://github.com/okondev2021/StartupTrybe-Bot.git
    ```

2. **Navigate to the project directory:**

    ```sh
    cd into the project folder
    ```

3. **Install the dependencies from the requirements.txt file:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Start the Server:**

    ```sh
    python manage.py runserver
    ```

## This server needs to be running before you launch the frontend application, since alot of data is needed, like token for authentication or refreshing the token. Danke