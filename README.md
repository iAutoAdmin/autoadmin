# autoadmin

## 开发环境
1. 同步数据库
```shell script
python manage.py makemigrations users
python manage.py makemigrations servicetree
python manage.py makemigrations pms
python manage.py migrate
```

2. 起动服务
```shell script
python manage.py runserver 0.0.0.0:8000
```