# Inception


Setting up development Environment on Linux
----------------------------------

### Install Project (edit mode)

#### Working copy
    
    $ cd /path/to/workspace
    $ cd inception
    $ pip install -e .
 
### Setup Database

#### Configuration

```yaml

db:
  url: postgresql://postgres:postgres@localhost/inception_dev
  test_url: postgresql://postgres:postgres@localhost/inception_test
  administrative_url: postgresql://postgres:postgres@localhost/postgres
```

#### Remove old abd create a new database **TAKE CARE ABOUT USING THAT**

    $ inception db create --drop --mockup

And or

    $ inception db create --drop --basedata 

#### Drop old database: **TAKE CARE ABOUT USING THAT**

    $ inception [-c path/to/config.yml] db --drop

#### Create database

    $ inception [-c path/to/config.yml] db --create

Or, you can add `--drop` to drop the previously created database: **TAKE CARE ABOUT USING THAT**

    $ inception [-c path/to/config.yml] db create --drop


### Running tests

```bash
pip install -r requirements-dev.txt
pytest
```

### Running server

#### Single threaded 

```bash
inception [-c path/to/config.yml] serve
```

#### WSGI

wsgi.py

```python
from inception import inception
inception.configure(files=...)
app = inception
```

```bash
gunicorn wsgi:app
```

### How to start

Checkout `inception/controllers/foo.py`, 
`inception/models/foo.py` and `inception/tests/test_foo.py` to
learn how to create an entity.

