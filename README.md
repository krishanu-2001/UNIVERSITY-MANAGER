Clone this project  
  
## Installing Requirements  
      1. Mysql (preferably use Mysql Workbench 8.0)  
      
      2. Python 3.7 / 3.6 ( Not compatible with python 3.9 )  
 <br ><br ><br > 
        
## STEP 1  ( IMPORTING MYSQL DATABASE)
      1. Imporing export.sql in /sqldump folder to test database  
      
      2. Changing host / port / password / database name in db.yaml  
      
       Note the above step is necessary to ensure database works on your system 
<br ><br ><br >

## STEP 2  ( STARTING FLASK SERVER )  
### WINDOWS -- EVERYTHING IS AUTOMATED  

      Double click on makefile.bat -> will do all steps below  
        
      Ensure you are using python 3.7 and db.yaml is edited


### MANUAL  

      if possible use venv

      pip install -r requirements.txt

      Ensure you have edited db.yaml and imported mysql  

      Run the application by executing the command python app.py

      Use python 3.7 

      The application runs on localhost:5000
