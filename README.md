[![Businge Scott](https://img.shields.io/badge/Businge%20Scott-Checkpoint2-green.svg)]()
[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Liste des seaux : A Bucketlist API
 
## Introduction
A Bucket List is a list of things that one has not done but wishes to accomplish before their demise. Liste des seauxis the french word for bucketlist. It enables CRUD
functionality (Create, Read, Update, Delete) operations on the bucket list.

>A project done in fulfillment of the second checkpoint of the Andela training program.

# Project description

Brief highlights about the following concepts is necessary:

 >API

 >REST

 >JSON

**API**

An **API**, acronym for Application Programming Interface, provides a blueprint for how software programs interacts with each other.

**REST**

REST is an acronym that stands for **RE**presentational **S**tate **T**ransfer and has become the de-facto way of building API's and thus API's using this standard are known as RESTFul API's. The five main principles the implementation of REST and RESTFulness are:

>Everything is a resource.

>Every resource has a unique identifier.

>Use simple and uniform interfaces.

>Communication is done by representation.

>Aim to be Stateless.

**JSON**

Yet another acronym, JSON which stands for **J**avascript **O**bject **N**otation, is a light-weight format that facilitates interchange of data between different systems or, case in point, software. It is intended to be universal and thus allows consumption of data by any program regardless of the programming language it is written in. Sample JSON data would be as follows:

```
{
"name":"bucketlist",
"description":"A Flask Bucketlist API",
"created_by":"scotty-b",
}

```

## Installation
 
Clone the GitHub repo:
 
http:
>`$ git clone https://github.com/scott45/checkpoint2-bucketlist.git`

cd into the folder and install a [virtual environment](https://virtualenv.pypa.io/en/stable/)

`$ virtualenv venv`

Activate the virtual environment

`$ venv/bin/activate`

Install all app requirements

`$ pip install -r requirements.txt`
Create the database and run migrations

`$ createdb bucketlist_db`

`$ createdb testing_dbt`

`$ python manage.py db init`

`$ python manage.py db migrate`

`$ python manage.py db upgrade`

All done! Now, start your server by running `python manage.py runserver`. You could use a GUI platform like [postman](https://www.getpostman.com/) to make requests to and fro the api.
### Endpoints

Here is a list of all the endpoints in bucketlist app.

Endpoint | Functionality| Access
------------ | ------------- | ------------- 
POST bucketlist/app/v1/auth/login |Logs a user in | PUBLIC
POST bucketlist/app/v1/auth/register | Registers a user | PUBLIC
POST bucketlist/app/v1/bucketlists/ | Creates a new bucket list | PRIVATE
GET bucketlist/app/v1/bucketlists/ | Lists all created bucket lists | PRIVATE
GET bucketlist/app/v1/bucketlists/id | Gets a single bucket list with the suppled id | PRIVATE
PUT bucketlist/app/v1/bucketlists/id | Updates bucket list with the suppled id | PRIVATE
DELETE bucketlist/app/v1/bucketlists/id | Deletes bucket list with the suppled id | PRIVATE
POST bucketlist/app/v1/bucketlists/id/items/ | Creates a new item in bucket list | PRIVATE
PUT bucketlist/app/v1/bucketlists/id/items/item_id | Updates a bucket list item | PRIVATE
DELETE bucketlist/app/v1/bucketlists/id/items/item_id | Deletes an item in a bucket list | PRIVATE

### Searching

It is possible to search bucketlists using the parameter `q` in the GET request. 
Example:

`GET http://localhost:/bucketlists?q=<whatever>`

This request will return all bucketlists with `whatever` in their name

### Sample GET response
After a successful resgistration and login, you will receive an athentication token. Pass this token in your request header.
Below is a sample of a GET request for bucketlist

### Testing
The application tests are based on python’s unit testing framework unittest.
To run tests with nose, run `nosetests`

### License
The API has an MIT license
