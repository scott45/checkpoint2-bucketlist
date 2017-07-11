---
title: bucketlist-Cp2-scotty

language_tabs:
  - bucketlist_shell
  - python
  - javascript (Angularjs)

toc_footers:
  - <a href='https://andela.com/'>Businge Scott </a>
  - <a href='https://andela.com/'>Andela </a>
  - <a href='https://docs.google.com/document/d/1nLXPHpACxRy8FSVMZCwZDhhML9M1tW9ELPAvzyN45HM/edit'>Checkpoint-2 </a>
  - <a href='#'>Sign Up to use bucketlist API </a>
  - <a href='https://github.com/scott45/checkpoint2-bucketlist'>Github project link (scott45)</a>

includes:
  - errors

search: true
---

# Introduction to bucketlist API

## Liste des seaux : (French word for bucketlist)


A Bucketlist API
A Bucket List is a list of things that one has not done but wishes to accomplish before their demise. Liste des seauxis the french word for bucketlist. It enables CRUD
functionality (Create, Read, Update, Delete) operations on the bucket list.

We have language bindings in Shell, Python and javascript (Angularjs)! You can view code examples in the dark area to the right, and you can switch the programming language of the examples with the tabs in the top right.

This API documentation page was created with [Slate](https://github.com/tripit/slate).

## About project

Requirements

Problem Description
According to Merriam-Webster Dictionary, a Bucket List is a list of things that one has not done before but wants to do before dying.
In this exercise you will be required to create an API for an online Bucket List service using Flask.

NB: The backend API for the application should be documented using API Documentation Tools such as Swagger, Apiary or Slate.

## About Author

Scott is an Entry level developer currently working for Andela Kenya Limited as a Software developer. He's passionate about learning to learn, Problem solving and he believes that greater things are yet to come.

# Registering a User

> To register, provide a username and password:

To register a user, the following are required.

A username which should have the following;

More than 6 characters

Should not have special characters in it

Should have no history of being used in the database

A password which should have the following;

More than 6 characters

```json
@app.route('/bucketlist/api/v1/auth/register', methods=['POST'])

{
	"username": "slatedemo", "password": "mybucketlist"
}
```

> The above returns JSON structured response like this:

```json
[
 {
    "Registration status": "slatedemo successfully registered!!"
 }
]
```

# Logging in a User

After a user is logged in, there is a generated token which is to be passed in the headers under authorisation.

Any other post, get, update or delete requests made require a user to have a token.

> To login, provide a username and password which were used during registration:


```json
@app.route('/bucketlist/api/v1/auth/login', methods=['POST'])

{
	"username": "slatedemo", "password": "mybucketlist"
}
```

> The above returns JSON structured response like this:

```json
 {
    "Login status": "Login successful",
    "Token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjpbMSwyLDMsNCw1XSwiZXhwIjoxNDk4NDE0NTY1fQ.tad9j8GQ9yGODE_fcQB6tABgNZoiJZ-5Ld78O2yeBMA"
 }
```

> Make sure you have a token generated after login which is to be placed in the headers.

```json
[
  {
    `Authorization:  eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjpbMSwyLDMsNCw1XSwiZXhwIjoxN
     Dk4NDE0NTY1fQ.tad9j8GQ9yGODE_fcQB6tABgNZoiJZ-5Ld78O2yeBMA`
  }
]
```

# Bucketlist endpoints functionality demo

## Get All Buckets

This is a GET request which returns all buckets and the items therein.

If items have been created within the buckets, they are parsed along.

> Make sure you have a token generated after login which is to be placed in the headers.

```json
@app.route('/bucketlist/api/v1/bucketlist', methods=['GET'])

[
  {
    `Authorization:  eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjpbMSwyLDMsNCw1XSwiZXhwIjoxN
     Dk4NDE0NTY1fQ.tad9j8GQ9yGODE_fcQB6tABgNZoiJZ-5Ld78O2yeBMA`
  }
]
```

> The above command returns JSON structured like this:

```json
[
    {
        "created_by": 3,
        "date-created": "Wed, 21 Jun 2017 08:37:36 GMT",
        "date_modified": "Wed, 21 Jun 2017 08:37:36 GMT",
        "id": 2,
        "name": "i am blessed"
    },
    {
        "created_by": 3,
        "date-created": "Wed, 21 Jun 2017 11:01:09 GMT",
        "date_modified": "Wed, 21 Jun 2017 11:01:09 GMT",
        "id": 3,
        "name": "this is #tia"
    },
    {
        "created_by": 4,
        "date-created": "Thu, 22 Jun 2017 17:44:36 GMT",
        "date_modified": "Thu, 22 Jun 2017 17:44:36 GMT",
        "id": 4,
        "name": "I'm the best that there is"
    }
]
```

This endpoint retrieves all buckets.

## Get a Specific bucket

This is a GET request which returns a specific bucket and the items therein.

This is done by specifying the bucket id

An error is returned in case the requested bucket id doesn't exist

> Make sure you have a token generated after login which is to be placed in the headers.

```json
@app.route('/bucketlist/api/v1/bucketlist/1', methods=['GET'])

[
  {
    `Authorization:  eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjpbMSwyLDMsNCw1XSwiZXhwIjoxN
     Dk4NDE0NTY1fQ.tad9j8GQ9yGODE_fcQB6tABgNZoiJZ-5Ld78O2yeBMA`
  }
]
```

> The above command returns JSON structured like this:

```json
{
    "date-created": "Tue, 27 Jun 2017 08:02:06 GMT",
    "date_modified": "Tue, 27 Jun 2017 08:02:06 GMT",
    "id": 1,
    "items": [
        {
            "date-created": "Tue, 27 Jun 2017 08:02:06 GMT",
            "date_modified": "Tue, 27 Jun 2017 08:02:06 GMT",
            "id": 1,
            "name": "cp sync"
        },
        {
            "date-created": "Tue, 27 Jun 2017 08:02:06 GMT",
            "date_modified": "Tue, 27 Jun 2017 08:02:06 GMT",
            "id": 2,
            "name": "sims sync"
        },
        {
            "date-created": "Tue, 27 Jun 2017 08:08:45 GMT",
            "date_modified": "Tue, 27 Jun 2017 08:08:45 GMT",
            "id": 4,
            "name": "retro for sims sync"
        }
    ],
    "name": "scott sync"
}
```

## Add a bucket to the list

This is a POST which adds a new bucket to the list.

You parse in the bucket name and the next field are auto generated.

An error is returned in case the request is done not as expected.

> Make sure you have a token generated after login which is to be placed in the headers.

```json
@app.route('/bucketlist/api/v1/bucketlist', methods=['POST'])

[
  {
    `Authorization:  eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjpbMSwyLDMsNCw1XSwiZXhwIjoxN
     Dk4NDE0NTY1fQ.tad9j8GQ9yGODE_fcQB6tABgNZoiJZ-5Ld78O2yeBMA`
  }

  {
	"name": "slatedemo bucketlist"
  }
]
```

> The above command returns JSON structured like this:

```json
 {
     "status": "Bucket added successfully"
 }
```

## Update a bucket

This is a PUT request which seeks to update an already existing entry.

This is done by specifying that the operation is a PUT

An error is returned in case the requested bucket id doesn't exist

> Make sure you have a token generated after login which is to be placed in the headers.

```json
@app.route('/bucketlist/api/v1/bucketlist/5', methods=['PUT'])

[
  {
    `Authorization:  eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjpbMSwyLDMsNCw1XSwiZXhwIjoxN
     Dk4NDE0NTY1fQ.tad9j8GQ9yGODE_fcQB6tABgNZoiJZ-5Ld78O2yeBMA`
  }

  {
	"name": "slatedemo bucketlist updated"
  }
]
```

> The above command returns JSON structured like this:

```json
{
    "date-created": "Sun, 25 Jun 2017 07:56:09 GMT",
    "date_modified": "Sun, 25 Jun 2017 07:56:09 GMT",
    "id": 5,
    "name": "slatedemo bucketlist updated"
}
```

## Delete a bucket

This is a DELETE request which removes a bucket from the database.

This is done by specifying the bucket id along the route.

An error is returned in case the requested bucket id doesn't exist

> Make sure you have a token generated after login which is to be placed in the headers.

```json
@app.route('/bucketlist/api/v1/bucketlist/5', methods=['DELETE'])

[
  {
    `Authorization:  eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjpbMSwyLDMsNCw1XSwiZXhwIjoxN
     Dk4NDE0NTY1fQ.tad9j8GQ9yGODE_fcQB6tABgNZoiJZ-5Ld78O2yeBMA`
  }
]
```

> The above command returns JSON structured like this:

```json
{
    "Status": "Bucketlist deleted successfully."
}
```

## Create a new item in a bucket

This is a POST which adds a new item to the specified bucket.

You parse in the bucket id to have the item belong.

An error is returned in case the bucket id doesn't exist.

> Make sure you have a token generated after login which is to be placed in the headers.


> Make sure you have a token generated after login which is to be placed in the headers.

```json
@app.route('/bucketlist/api/v1/bucketlist/2', methods=['POST'])

[
  {
    `Authorization:  eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjpbMSwyLDMsNCw1XSwiZXhwIjoxN
     Dk4NDE0NTY1fQ.tad9j8GQ9yGODE_fcQB6tABgNZoiJZ-5Ld78O2yeBMA`
  }

  {
	"name": "scott is done"
  }
]
```

> The above command returns JSON structured like this:

```json
{
    "Status": "Success, item has been created"
}
```

## Update an item in a bucket

This is a PUT request which seeks to update an already existing item entry.

This is done by specifying that the operation is a PUT

An error is returned in case the specified bucket id doesn't exist

> Make sure you have a token generated after login which is to be placed in the headers.

```json
@app.route('/bucketlist/api/v1/bucketlist/<int:bucket_id>/items/<int:item_id>', methods=['PUT'])
@app.route('/bucketlist/api/v1/bucketlist/1/items/1', methods=['PUT'])

[
  {
    `Authorization:  eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjpbMSwyLDMsNCw1XSwiZXhwIjoxN
     Dk4NDE0NTY1fQ.tad9j8GQ9yGODE_fcQB6tABgNZoiJZ-5Ld78O2yeBMA`
  }
]
```

> The above command returns JSON structured like this:

```json
{
    "Status": "Bucketlist Item successfully edited."
}
```

## Delete an item in a bucket

This is a DELETE request which removes an item from the buckets that are in database.

This is done by specifying the bucket id along the route where the item belongs.

An error is returned in case the requested bucket id doesn't exist

> Make sure you have a token generated after login which is to be placed in the headers.

```json
@app.route('/bucketlist/api/v1/bucketlist/<int:bucket_id>/items/<int:item_id>', methods=['DELETE'])
@app.route('/bucketlist/api/v1/bucketlist/1/items/4', methods=['DELETE'])

[
  {
    `Authorization:  eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjpbMSwyLDMsNCw1XSwiZXhwIjoxN
     Dk4NDE0NTY1fQ.tad9j8GQ9yGODE_fcQB6tABgNZoiJZ-5Ld78O2yeBMA`
  }
]
```
```json
> The above command returns JSON structured like this:

{
    "Status": "Item deleted successfully."
}
```
