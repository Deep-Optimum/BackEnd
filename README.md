# Synopsis [![Build Status](https://travis-ci.com/Deep-Optimum/BackEnd.svg?branch=main)](https://travis-ci.com/Deep-Optimum/BackEnd) [![Build Status](https://travis-ci.com/Deep-Optimum/Front-End-Demo.svg?branch=main)](https://travis-ci.com/Deep-Optimum/Front-End-Demo)
Course project for COMS 4156 - Advanced Software Engineering

## Instructions
To run, first clone this repository

To install requirements:
```sh
$pip install -r requirements.txt
```

To compile all tests:

```sh
$python -m pytest tests
```
The backend database schema is defined in schema.sql under the folder resources.

You can automatically build your database and tables by running

```sh
$python src/set_up.py
```

To deploy the backend,
```sh
$python3 src/app.py
```