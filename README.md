# Senior-Project
#### Repository for Spring 2024 Senior Project at Rowan University with Dr. Baliga 

  **How to run application:**
  <ol>
  <li><b>git clone git@github.com:Ahmad1786/Senior-Project.git</b> </li>
  <li><b>cd Senior-Project/</b></li>
  <li>Create a Virtual Environment (make sure to name it something in the <b>.gitignore</b> such as <b>venv</b>)</li>
  <li>Activate the Virtual Environment</li>
  <li>Install all of the dependencies: <b>pip install -r requirements.txt</b></li>
  <li><b>cd project/</b></li>
  <li><b>python manage.py makemigrations</b> (Note: not needed unless made changes to the model)</li>
  <li><b>python manage.py migrate</b> (Apply changes from migrations to the actual database)</li>
  <li>Run project: e.g. <b>python manage.py migrate</b></li>
  </ol>

  **NOTE: Need to insert google credentials into the database if you want to use google login functionality in application**
