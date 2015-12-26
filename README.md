# trackstats
Repository for the Cloud Application Development coursework. This application is a fitness activity visualiser reading data from Google Fit.

http://trackstatsk.appspot.com/

## Folders
* trackstats: Contains the general definition files for the whole Django Project. This is the starting point and any request is redirected to the appropriate App
* frontend: Django App containing the site pages displaying fitness data. Data is pulled using client-side JavaScript and using the services App.
* services: App containing the REST services used by the client-side JavaScript. Returns data coming from Google Fit, after applying the necessary transformations or calculations.
