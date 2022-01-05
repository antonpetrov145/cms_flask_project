# CMS Flask Project

CMS Flask Project is a python app that lets you create, edit and delete posts. It uses PostgreSQL as a persistent data storage.

## Installation
First make sure you have [PostgreSQL](https://www.postgresql.org/download/) installed in the system you are using.

I suggest you install the app in it's own virtual envronment.
```
python -m venv venv
```
 
Then use the package manager [pip](https://pip.pypa.io/en/stable/) to install the dependencies for the CMS.

```
pip install -r requirements.txt
```
The app defaults to using `127.0.0.1:5000` address.

You have to make `.env` file in the root dir of the app with the following environment variables:

```
SECRET_KEY=
DB_USER=
DB_PASSWORD=
DB_ADDRESS=
DB_PORT=
DB_NAME=
```


**CAUTION** Read the whole document before attempting to use this app. This app is **not** production ready!

## Usage

There are 4 types of `users` that have different roles and permissions in the CMS. Each of them has a different endpoint for register and login:
### Authors

```
POST http://app-ip-address/authors/register

POST http://app-ip-address/authors/login
```

### Editors

```
POST http://app-ip-address/editors/register

POST http://app-ip-address/editors/login
```

### Clients

```
POST http://app-ip-address/clients/register

POST http://app-ip-address/clients/login
```

### Admins

```
POST http://app-ip-address/admins/register

POST http://app-ip-address/admins/login
```

On hitting both anedpoints you will receive a token that expires in **two days**.

Example response after hitting login endopoint:
```
{
    "token": <token>,
    "role": <role>
}
```

## Roles and permissions
`Authors` can create, edit and delete its own posts.

`Editors` can edit and delete all posts from all `Autors`.

`Admins` can edit and delete all posts from all `Autors` and do the same with the user accounts. Only admins can register other admins.

#### TODO
`Clients` can make requests for advertising posts for which they will set a word limit, language etc.

## Posts
Every post has an author and post content that is written in the database.

#### TODO
Authors should have CRUD only on their own posts.

### Endpoints
As a regular nonregistered user you can seee all posts:
```
GET http://app-ip-address/posts
```
As a registered Author you can see all of your posts:
```
GET http://app-ip-address/authors/<pk of the author>/posts
```
As a registered Editor you can see,edit and delete all posts:
```
GET http://app-ip-address/posts

PUT http://app-ip-address/posts/<pk of the post>

DELETE http://app-ip-address/posts/<pk of the post>
```

## Security

The security is accomplished with the help of JWT for login and register.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
