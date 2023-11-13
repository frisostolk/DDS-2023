INFOMDDS Team Red - Argicultural Dashboard

Deployment of the dashboard:

1. Ensure the presence of a program capable of running containerized applications on your system.
2. Build the Docker file included in the repository. During the build process, the necessary libraries and dependencies will be automatically installed.
3. Once the Docker file is successfully built (this can take a couple of minutes the first time you run it), the dashboard will automatically load the data into the PostgreSQL database.
4. The dashboard is ready for exploration.


Overview of the project folders

- dashboard: A Flask application that hosts our dashboard and contains some subforders.
    - src: Holds a file for importing the data into the database, and one file for fetching the data the data from the database.
    - static: Containes files for the visualisations in the dashboard
    - app.py: This is the main Flask app that hosts your dashboard, in here we also build the dashboard with the library dash.
    - Dockerfile_dashboard: Dockerfile for the flask-app.
    - requirements.txt: Holds all python libraries.
- data: Holds all the data files for the dashboard in subfolders.
- scrape-data: Holds all the files that do the data scraping from the datasources
- docker-compose.yml > Sets up the environments and docker containers.



