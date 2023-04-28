# FAST-API

 Run ::

     python -m pip install -r requirements/local_windows.txt
    

Then create ``.env`` file (or copy and modify ``.env.example.yaml``) in project root and set environment variables for application: ::

    Windows:
    - cmd: copy env.example.yaml .env



To run the web application in debug use::

    - uvicorn app.main:app --port {port} --reload

    Lưu ý:
    - Config worker, port, host trong file gunicorn.conf.py




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
    │   │       └── schemas
    │   ├── repositories
    │   ├── settings
    │   ├── third_party
    │   │   ├── oracle
    │   │   │   └── models
    │   │   └── services
    │   └── utils
    ├── backup
    │   └── oracle
    └── requirements

-----------------