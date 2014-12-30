[![Build Status](https://travis-ci.org/futurice/checklist.svg?branch=master)](https://travis-ci.org/futurice/checklist)

# Create lists of check-items from list templates

Uses a CDN (see CDN_URL in futurice_checklist/settings.py) for front-end
libraries such as http://ivaynberg.github.io/select2/


## Usage
```bash
pip install -r requirements.txt
echo 'SECRET_KEY = "some random string"' >local_settings.py
./manage.py test
REMOTE_USER=username ./manage.py runserver
```

## Deployment
`fab -H <server> deploy`
