Basic notes for Flask, file struction, opperation:
Flask is a web application framework for python. If you don't know what a framework is you can think of it like this. Your software calls a library, a framework calls your software.

## Template function
![alt text](/common_tools/Flask_Template/docs/SystemOverview.jpg "System Overview")

The heart of flask uses the route decorator to convert functions into route functions. These functions run when a browser sends a get request to the url. You can use them different ways to do different things. The two most basic methods are 1. to display a page to the user or 2. as a data route to update a data field.

Web pages can be either static, or templates using jinja2 https://jinja.palletsprojects.com/en/3.1.x/
The default location of file is the templates folder. -> 'index.html' is physically located in templates/index.html. Usually static files, css, js and static pages are stored in the static folder which can be access via route functions as follows, style.css is physically located in static/style.css
Jinja is powerful for templating, you can modularize pages, reuse subtemplates, run loops and logic on variables and create dynamic pages that scale with data. 

Flask applications run on a wsgi server (Web server gateway interface) which acts as a middle man between the webserver and the application software. You can access apps directly using only a wsgi server by specifying the port they are running on, or you can configure a webserver to handle the routing.


To use template
1. create virtual environment. Navigate to the folder above Flask_Template and run <code>python -m venv Flask_Template</code>
2. Activation virtual environment. Windows -> <code>./'folder_name'/Scripts/activate</code> Linux -> <code>. venv/bin/activate</code> VSCode -> select the python interpreter in the appropriate folder and restart terminal. cmd/terminal should have ('folder_name') as a prefix on the entry line while the virtual environment is active.
3. Install required libraries. <code>pip install -r requirements.txt</code>
4. Run using <code>python app.py</code> and navigate to 127.0.0.1:5000