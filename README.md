# FAST-API

 Run ::

     python -m pip install -r requirements.txt
    

Then create ``.env`` file (or copy and modify ``.env.example.yaml``) in project root and set environment variables for application: ::

    Windows:
    - cmd: copy env.example.yaml .env
  
    MacOs/Linux:
    - cmd: cp env.example.yaml .env





To run the web application in debug use::

    - uvicorn app.main:app --port {port} --reload
    
    Lưu ý:
    - Config worker, port, host trong file gunicorn.conf.py

Build web application with docker::


    - docker-compose up
    





Project structure
-----------------

Files related to application are in the ``app`` directories.
Application parts are::

    .
    ├── app
    │   ├── api
    │   │   └── v1
    │   │       ├── controllers
    │   │       ├── dependencies
    │   │       ├── endpoints
    |   |       ├── repository
    │   │       └── schemas
    │   ├── repositories
    │   ├── settings
    │   ├── third_party
    │   │   ├── oracle // config db and declare model
    │   │   │   └── models
    │   │   └── services
    │   └── utils // shared functions
    |
    │   
    └── requirements // library use for project

-----------------
