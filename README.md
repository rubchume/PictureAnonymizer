Author: Rubén Chuliá Mena <rubchume@gmail.com>

# Picture Anonymizer
Picture Anonymizer is an image repository prototype developed using the Django framework.

Any user can upload pictures that will be then showed in a common dashboard, with the particularity that the human faces will be blurred in order to keep anonymity.

It uses Google Cloud Storage and Google Cloud Vision API.

Try it at https://picture-anonymizer.herokuapp.com/

# Setup
The application needs to be executed in an environment with Python 3.8 installed.

If this is the case, proceed with the installation of necessary packages. Open the CLI (Command Line Interface) and execute:
```bash
pip install -r requirements.txt
```

It also uses Google Cloud Vision API. You need a service account credentials .json file in order to use it. More information at https://cloud.google.com/vision/docs/setup.

# Execution on local machine
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

# Execution in production environment
The repository already has the files required to be deployed on Heroku.

It also uses a Google Cloud Storage bucket in order to save the image files.\
You should create your own bucket and modify the file `photography_anonymizator/settings/production.py`: 
```python
GS_BUCKET_NAME = 'your_bucket_name'
```
For simplification purposes, you can configure the same service account you used for the Vision API so it has also access to the Cloud Storage service.
That way you don't need to modify anything else.  

# Test
Test the application with Pytest using
```bash
python -m pytest
```
