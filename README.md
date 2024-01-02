# Introduction

## About the app
Picture Anonymizer is a web application that allows any user to upload images, store them and visualize them in a common dashboard.
Before an image is saved, the human faces are automatically blurred to keep the anonymity.

The app is already prepared to be deployed as-is on the PaaS [Heroku](https://www.heroku.com/).

## Approach
It has been developed by using the [Django](https://www.djangoproject.com/) framework as the web backend.

For the detection of faces, it uses [Google Cloud Vision API](https://cloud.google.com/vision) (and [Google Cloud Storage](https://cloud.google.com/storage?hl=es-419) for support tasks).

The deployment has been done in [Heroku](https://www.heroku.com/).

# Setup

## Installation
The application needs to be executed in an environment with Python 3.8 installed.

If this is the case, proceed with the installation of necessary packages. Open the CLI (Command Line Interface) and execute:
```bash
pip install -r requirements.txt
```

It also uses Google Cloud Vision API. You need a service account credentials `.json` file in order to use it. More information at https://cloud.google.com/vision/docs/setup.

## Execution on local machine
Run
```bash
python manage.py runserver
```

Open a web browser and navigate to the url http://127.0.0.1:8000.

Use the command
```bash
python manage.py remove_old_pictures [max_picture_storage_minutes]
```
to remove pictures that are older than the supplied value. If you don't supply any value, the default is configured in `photography_anonymizator/settings/base.py` in the variable `MAX_PICTURE_STORAGE_MINUTES`. It is set to 24 hours.

## Execution in production environment
The repository already has the files required to be deployed on Heroku.

It also uses a Google Cloud Storage bucket in order to save the image files.\
You should create your own bucket and modify the file `photography_anonymizator/settings/production.py`: 
```python
GS_BUCKET_NAME = 'your_bucket_name'
```
For simplification purposes, you can configure the same service account you used for the Vision API so it has also access to the Cloud Storage service.
That way you don't need to modify anything else.  

## Test
Test the application with Pytest using
```bash
python -m pytest
```
