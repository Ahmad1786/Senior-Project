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
  <li><b>python manage.py shell < data_creation/insert_data.py</b> (Create all the dummy data - Also creates a SuperUser) </li> 
  May need to do: <b>echo "import data_creation.insert_data.py" | python manage.py shell </b> instead
  <li>May also need to run <b>python manage.py activategoogle &lt;json_file_path&gt;</b> (See Below) </li>
  <li>Run project: e.g. <b>python manage.py runserver</b></li>
  </ol>

  **NOTE on #10: <br> Need to insert google credentials into the database if running for the first time to use the google signin functionality. <br> Theres a script to avoid manually inserting them, simply put the client_secret json file somewhere into the project (it will be gitignored), or even anywhere on your computer, and run the custom command specifying the path to the file as an argument**
