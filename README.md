Because I liteally always forget how to activate a virtual machine on windows `./venv/Scripts/activate`

# BFEX [![CircleCI](https://circleci.com/gh/CMPUT401-Find-an-Expert/BFEX/tree/master.svg?style=shield)](https://circleci.com/gh/CMPUT401-Find-an-Expert/BFEX/tree/master)

## Dev Environment
To work on BFEX on your local machine, you will need the following dependencies. If you simply wish to run it, you can use docker to deploy the entire system with `docker-compose up --build` from the root directory.

The environmental variable `BFEX_CONFIG` by default points to `${project_dir}/config.json` and can be changed. Link to UI http://localhost:8901/static/index.html

### Conda
We use conda to manage our virtual python environment and install some more complicated dependencies ie. scipy and numpy. 

The file `web/environment.yml` will allow you to recreate the exact environment we are using.

#### Ubuntu / Mac
Download the miniconda installer from [Conda](https://conda.io/miniconda.html), and run the installer from wherever you download it. It provides sensible defaults, but you can change any you like.

Once you've installed conda, you will be able to recreate the environment with `conda-env create -f web/environment.yml`. This creates the `BFEX` environment, which you can activate with `source activate BFEX`. If you want to delete the environment, run `conda-env remove --name BFEX`. Whenever you want to run any of the BFEX code, you should have the environment activated.

### Elasticsearch
We use Elasticsearch as our datastore.

#### Ubuntu
Elasticsearch can be installed by linking into the Elastic APT repository. Digital Ocean provides a good [setup guide](https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-elasticsearch-on-ubuntu-16-04) which you can follow. Or you can follow the official Elasticsearch [setup guide](https://www.elastic.co/guide/en/elasticsearch/reference/current/deb.html).

Once you've followed those steps, you should be able to start Elasticsearch with `sudo systemctl start elasticsearch`, and stop it with `sudo systemctl stop elasticsearch`. To verify it is running, you can use the curl request `curl -XGET localhost:9200`.

#### Mac
Installation is simplified when using a Mac, using the Brew package manager. Update Brew, then install with `brew install elasticsearch`.

Brew should automatically link it, so it should be accessible with the command `elasticsearch`.

### Kibana (optional)
Kibana is a UI layer for Elasticsearch. It's helpful for looking at the data inside, as well as running arbitrary queries for testing.

#### Ubuntu
Follow the Elastic [setup guide](https://www.elastic.co/guide/en/kibana/current/deb.html). After completion, you should be able to run Kibana with `sudo systemct start kibana`. It will be hosted on `localhost:5601`.

#### Mac
Installation on Mac is again simplified by brew. Install with `brew install kibana` and run with the command `kibana`.

### Celery
Celery is used for distributed asynchronous task processing. It allows us to submit tasks into task queue, where it will processed sometime in the future. This way, we can offload the heavy work like scraping pages from our UI processes. Celery is installed as part of our environment file, but the Celery process must be started seperately. If you have your PYTHONPATH environment variable set up to include `BFEX/web` you can run the following command from anywhere. Otherwise, run it from the `web` folder.
`celery worker -A bfex.tasks -l debug` creates the celery process, registers the tasks in bfex.tasks, and sets the logging mode to debug.

### Redis
Redis is an in memory datastore, used as the message broker and result store used by Celery. It serves as an waiting place for tasks that need to be executed.

#### Ubuntu
The redis-server is available in the default APT repositories. The version is slightly older. Use `sudo apt-get install redis-server' to install.

The development version of redis can be run simply with the `redis-server` command, which will create an instance in your current session.

#### Mac
`brew install redis` will provide both `redis-server` and `redis-client`. Run using `redis-server`.

## Tests
There are 2 forms of tests for BFEX. Those that do not require access to a database, and those that do. By default, the tests that require a connection to elasticsearch are not run. This is to prevent cluttering elasticsearch with test data.

To enable the database tests, you need to set the environment variable `PYTEST_ENV` to `build`. A new connection will be created to the elasticsearch specified by `ELASTIC_HOST`, or default to localhost.
