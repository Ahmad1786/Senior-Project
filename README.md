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

  **How to get started with GIT:**
  <ol>
  <li>git clone git@github.com:Ahmad1786/Senior-Project.git</li>
  <li>cd Senior-Project</li>
  <li>git branch(To show the branches in your local repository) </li>
  <li>git branch &lt;YourName&gt;(YourName = what you want to name the branch)</li>
  <li>git checkout &lt;YourName&gt;(Switches branches and go to the new branch you created)</li>
  </ol>
  
  **How to push to GIT:**
  <ol>
  <li>git fetch origin (Download any new changes that occured since last fetch of origin)</li>
  <li>git rebase origin/main (This updates the current branch you are on and updates it to what is in main)</li>
  <ul><li>If it returns a message saying your up to date with main you can move onto push </li>
  <li>Otherwise it will go through and update your current branch to master, it will stop when it encounters a merge conflict. This means that something in you current branch is different than what is on main</li>
  </ul>
  <li>git push origin &lt;theBranchNameYouWantToPush&gt;(This pushes the branch of your choice to to the remote repo of your choice)</li>
  </ol>

  **How to create pull request:**
  <ol>
  <li>After pushing the code, if you go to https://github.com/Ahmad1786/Senior-Project. It should pop that new code was pushed and to create a pull request. Make sure the pull request is to main</li>
  <li>Then dont merge it into main until you tested it, and it been peer reviewed by someone else</li>
  </ol>

   **How to use reset_db shell script:**
   <br> This script should be used any time you need to change a model and run migrations. <br> This helps resolve the issue where a table does not exist after making a change.**
  <ol>
  <li>From the project's root directory, the directory where the reset_db.sh exists, run the following command: <b>chmod +x reset_db.sh</b>. This makes it an executable script.</li>
  <li>Then run the following command to run the script: <b>./reset_db.sh</b> </li>
  </ol>
