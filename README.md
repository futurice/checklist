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
`git push deis master`

## Docker

### Build

```bash
docker build --tag USER/REPO --rm .
```

### Run

Assuming the image was built as `futurice/checklist`:

```bash
docker run -p 8000:8000 -d -e SECRET_KEY=real_secret_here \
	-e DB_HOST=my-db.example.com \
	futurice/checklist
```

Add other environment variables as needed.

### Configuration

Runtime configuration is done via environment variables set e.g. during `docker run`. The following environment variables are recognized. Defaults in parentheses.

- REMOTE_USER_HEADER (REMOTE_USER) - default is working in WSGI setup. Overwrite to use an HTTP header. Django prefixes HTTP headers with HTTP_. See https://docs.djangoproject.com/en/1.8/howto/auth-remote-user/.
- SECRET_KEY ()                    - the Django SECRET_KEY. Must be good random value. See https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-SECRET_KEY.
- DB_TYPE (default)                - default is sqlite and the rest of the DB_ variables are ignored. Set to any other value (e.g. pg) to use PostgreSQL.
- DB_HOST (localhost)
- DB_PORT (5432)
- DB_NAME (checklist)
- DB_USER (checklist)
- DB_PASSWORD ()
- DEBUG (false)          - Django DEBUG setting
- TEMPLATE_DEBUG (false) - Django TEMPLATE_DEBUG setting
- ALLOWED_HOSTS (*)      - Django ALLOWED_HOSTS setting
