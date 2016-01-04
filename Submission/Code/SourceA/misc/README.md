# TrackStats Project
This folder contains all files necessary for the application execution in the Google App Engine (GAE) platform. File structure follow the Django pattern combined with the GAE requirements.

## Architecture
Django has file/folder conventions that will be explained in more detail in the next section. However, conceptually those files and folders are designed to define a Project and several Django Apps. The Project is only one and is contained in the folder with the same name as the root folder, in this case _trackstats_. This folder is mainly a wrapper and contains general definition, configuration and routing files. There are other folders containing Django Apps that actually provide some services to the end user. 

## Files and Folders
* **app.yaml**: This file is one of the most important ones for the execution in the GAE environment, as well as to deploy the project to the final URL (http://trackstatsk.cloudapp.com). This is an adapted file from the standard one for GAE.
* **manage.py**: Management and configuration file for Django. This file should not be modified and is used mostly for major configuration changes and Django application creation.
* **ClientIDSecret.json**: File that contains the details to connect to the Google API with the OAuth Trackstatsk credentials.
* **trackstats**: This is the Project folder and contains configuration and routing files like settings.py, urls.py and wsgi.py. In general terms, those files are not expected to have important changes during the development.
* **frontend**: This Django App contains the content pages like the welcome page, dashboard, session details, etc. Pages content is displayed depending on authentication status. Authentication is directly managed by the usrmgmt Django App.
* **services**: Django App that is the application layer between Google Fit and the frontend. It contains only REST services that pull content from Google Fit for the autenticated user, and after transformations and calculation renders JSON reponses for the frontend layer.
* **usrmgmt**: User Management Django App that handles user sign-in sign-out operations against the Google Authentication API.
* **static**: Folder containing all static files like images, styles and scripts. Paths are mapped in the app.yaml file to avoid the static part. e.g. /static/images --> /images.

