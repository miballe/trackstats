TrackStats
Folders are all relative to the root folder for Google App Engine Launcher App.
By keeping the same structure and copying each file/folder from the respective SourceX to the same folder, it will
rebuild the whole project structure and be ready for deployment.

There's just a special consideration in the /frontend/templates/frontend/*.html
- JavaScript: All these files were kept as HTML but the JavaScript code was isolated for easy counting.
- HTML: HTML code was isolated and copied to the misc folder. Opening and closing script tags were left in the HTML source so 
  after copying the code it should be possible to have a functional page.
The reason why these pages were split that way is because all javascript was inline in the HTML code.