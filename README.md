# Coffee Shop

A new digitally enabled cafe for students to order drinks, socialize, and study hard.

## Features of the application

1. Display graphics representing the ratios of ingredients in each drink.
2. Allow public users to view drink names and graphics.
3. Allow the shop baristas to see the recipe information.
4. Allow the shop managers to create new drinks and edit existing drinks.

### Backend

The `./backend` directory contains a Flask server with a SQLAlchemy module. It serves as an API that interacts with the frontend and integrates with Auth0 for user authentication.

[View the README.md within ./backend for more details.](./backend/README.md)

### Frontend

The `./frontend` directory contains an Ionic frontend to consume the data from the Flask server. You will only need to update the environment variables found within (./frontend/src/environment/environment.ts) to reflect the Auth0 configuration details set up for the backend app.

[View the README.md within ./frontend for more details.](./frontend/README.md)
