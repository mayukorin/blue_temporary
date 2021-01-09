# Name（リポジトリ/プロジェクト/OSSなどの名前）

青チャート管理システム（仮）  





# Features

勉強記録の登録や更新ができるところまで 

# Requirement


* Django
* PostgreSQL
* psycopg2
* Pillow

# Installation

Requirementで列挙したライブラリなどのインストール方法を説明する

1. PostgreSQLをインストールする  
1. psycopg2をインストールする  
1. Pillowをインストールする  
1. インストール時に設定したパスワードを使い、コマンドプロンプト（ターミナル）で  PostgreSQLにログイン  
```psql -U postgres```  
1. データベースを所有するためのユーザを作成する
```create role （ユーザ名） with login password (パスワード);```
1. データベースを作成する（4で作成したユーザーを所有者にする）  
```create database （データベース名) with owner (4で作成したユーザ名);```
1. app1/config/settings/の下にlocal.pyを作り、以下のように編集する
```
from .base import *
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'データベース名',
        'USER':'4で作成したユーザ名',
        'PASSWORD': '4で作成したユーザのパスワード',
        'HOST': 'localhost',
        'PORT': '',
    }
}
```
1. test7ディレクトリで、     
```python manage.py makemigrations```
```python manage.py migrate app1```
```python manage.py migrate``` 
を実行  




# Usage

```python manage.py runserver```でhttp://127.0.0.1:8000/siteUser/login にアクセス  



