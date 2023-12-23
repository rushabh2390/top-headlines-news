# Top-healines-news
## Get newsapi key 
---
  Get key from [Newsapi](https://newsapi.org/docs/endpoints/top-headlines)   
  Add you api key in docker-compose-file or in backend .env file like below.
   In docker-compose.yaml
```
SECRET_API_KEY ='xxxxxxx'
```

## Run Locally   
---
   ## .Env file   
   In backend create .env file and add following Details
```
DATABASE_URL=postgresql://postgres:postgres@localhost/postgres
SECRET_API_KEY=xxxxxx
DEBUG=True
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
DATABASE_HOST=localhost
DATABASE_NAME=newsDB
DATABASE_PORT=5432
REDIS_URL=redis://localhost:6379/0
```
  ---
  In frontend create .env file and add follwoing details
```
NODE_ENV=development
VUE_APP_BASE_URL=http://localhost:8000/
VUE_APP_WEBSOCKET=ws://localhost:8000/ws/news/
```
---

1. clone this repo.
2. Go to Project Directory backend/ in terminal. 
3. Make virtual environment and active it as given below command
```
pipenv shell
```
4. Install dependency list.
```
pip install -r requiremenets.txt
```
Here we are using celery, redis celery-beat for eunning reply nalysis task asynchronously.
5. create a superuser
```
python manage.py createsuperuser
```
6. How to install and run redis please refere: [celery-redis-django](https://www.codingforentrepreneurs.com/blog/celery-redis-django)

7. After install  and run redis please type following 2 command in 2 seperate terminal.
```
celery -A newsapi worker -l info -P gevent

celery -A newsapi beat -l info
```
> if you gevent is   not installed please installed it with ``` pip install gevent ```

8. Now run this project with.
```
python manage.py runservere
```
9. Open another terminal and go to project directory
10. Go to frontend
```
cd frontend
```
11. Install package from package.json
```
npm install
```
12. Run front end vue
```
npm run dev
```
9. open [Frontend](http://localhost:8080/)

## Run in Docker
---
1. clone this repo.
2. Go to Project Directory in terminal.
3. Run following command.
```
docker-compose up -d
```
