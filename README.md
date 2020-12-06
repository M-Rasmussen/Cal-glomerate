# Cal-Glomerate

#https://calglomerate.herokuapp.com/

## 1. Upgrade Node upgrade

```$ nvm install 10.23.0```

## 2. Install initial `npm` dependencies from `package.json`

```$ npm install```
## 3. Install Socket.IO & Webpack

  ```pip install flask-socketio```
  
  ```pip install eventlet```
  
  ```npm install -g webpack```
  
   ```npm install --save-dev webpack```
  
   ```npm install socket.io-client --save```

##4. Setting up Database

   ```sudo yum update```
   
  ```sudo /usr/local/bin/pip install --upgrade pip```
  
  ```sudo /usr/local/bin/pip install psycopg2-binary```
  
  ```sudo /usr/local/bin/pip install Flask-SQLAlchemy==2.1```
  
  ```sudo yum install postgresql postgresql-server postgresql-devel postgresql-contrib postgresql-docs```
  
  ```sudo service postgresql initdb```
   
   ```sudo service postgresql start```
   
   ```sudo -u postgres createuser --superuser $USER```
   
   ```sudo -u postgres createdb $USER```
   
   ```psql```
   
   ```create user [YOUR_USERNAME] superuser password '[YOUR_PASSWORD]';```
   
   Create a .env file
   -  add -> "export DATABASE_URL=postgresql://[YOUR_USERNAME]:[YOUR_PASS]@localhost/postgres"
## 5. Link your database
     ``` sudo vim /var/lib/pgsql9/data/pg_hba.conf ```
     
     ```:%s/ident/md5/g```
      ```:wq ``` 
    ```sudo service postgresql restart```
## 6. Google Auth Creation
   1) Go to https://console.developers.google.com
   2) Select a project and then create 
   3) Click on new project and Create
   4) Go to Credentials and click OAuth 
   5) Pick Web application 
   6) Set authorized url to your react web page url 
    Install `` npm install react-google-login `` 
    
    ```pip install google-oauth2-tool```
   7) Your keys will pop up and you should use that for react Login.jsx file under "clientId= " 
## 7. Install Calandar Packages
  
```npm i react-big-calendar```

```npm install moment --save```

```npm i react-tackle-box```

```npm install date-fns --save```

```npm i react-calendar```

```npm i rc-time-picker```





##  make sure to sudo service postgresql start.

## Individual work
###Worked on as group
```push to heroku```
### Matt: 
```Worked on front end.``` 
```Displayed the calender component that we are using and created events to accept it.```
```Created merge front-end that will. ```

### Sam:
``` worked on style```
```worked on frontend```
```added microsoft ui elements to frontend```

### Harsh:
```created add event button```
```unit testing```

### David: 
```Worked on database backend```
```worked on google auth```
```worked on database```

pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
pip install oauth2client
pip install iso8601