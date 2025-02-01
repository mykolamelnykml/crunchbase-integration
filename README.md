# Crunchbase API integration

## Poetry

This project uses poetry. It's a modern dependency management
tool.

To install deps use this set of commands:

```bash
poetry install
```

## Configuration

This application can be configured with environment variables.

You can create `.env` file in the root directory and place all
environment variables here. 

All environment variables should start with "CRUNCHBASE_" prefix.

For example if you see in your "ml_rest_api/settings.py" a variable named like
`random_parameter`, you should provide the "CRUNCHBASE_RANDOM_PARAMETER" 
variable to configure the value. This behaviour can be changed by overriding `env_prefix` property
in `crunchbase.settings.Settings.Config`.

An example of .env file:
```bash
CRUNCHBASE_API_KEY="api_key"
```

## Pre-commit

To install pre-commit simply run inside the shell:
```bash
pre-commit install
```

pre-commit is very useful to check your code before publishing it.
It's configured using .pre-commit-config.yaml file.

By default it runs:
* black (formats your code);
* mypy (validates types);
* ruff (spots possible bugs);


## Running tests

If you want to run it in docker, simply run:

```bash
docker-compose run --build --rm main pytest -vv .
docker-compose down
```

For running tests on your local machine.


2. Run the pytest.
```bash
pytest -vv .
```


## Generate data model code from JSON data

For avoid to write data model classes manually you can use `datamodel-codegen` tool.

```bash
datamodel-codegen  --input ./tests/testresources/crunchbase/organizations/test_organization.json \
 --input-file-type json --output ./crunchbase/schemas/organization.py \
 --class-name Organization
```