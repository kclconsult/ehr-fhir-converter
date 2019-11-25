# EHR-FHIR Mapper

Converting data from arbitrary EHR vendors to the FHIR standard.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Before installing, [download and install Python 3](https://www.python.org/download/releases/3.7) and [Pip](https://pip.pypa.io/en/stable/installing/), a Python package manager.

(Recommended) Then install [virtualenv](https://virtualenv.pypa.io/en/stable/installation/).

### Building (Optional)

Clone this repository:

```
git clone https://github.kcl.ac.uk/consult/fhir-ehr-adapter
```

Change into the directory:

```
cd ehr-fhir-adapter/src
```

Initialise a virtual environment, and activate:

```
virtualenv -p python3 env
. env/bin/activate
```

Install dependencies:

```
pip install -r requirements.txt
```

Rename EHR configuration file, and add appropriate variables:

```
mv src/EHR/APIVariables-Template.py src/EHR/APIVariables.py
vim src/EHR/APIVariables.py
```

##### (Optional, Option 1) Build FHIR classes

Clone the FHIR parser repository:

```
git clone git@github.com:smart-on-fhir/fhir-parser.git src/main/python/fhir-parser
```

Copy configuration scripts into the directory:

```
cp src/main/python/mappings.py src/main/python/fhir-parser/
cp src/main/python/settings.py src/main/python/fhir-parser/
```

Install parser requirements:

```
cd src/main/python/fhir-parser/
pip install -r requirements.txt
```

Generate FHIR Python classes:

```
touch Default/__init__.py
python generate.py
```

Move generated classes into project:

```
cd ../
mv models/ models_full/
touch models_full/__init__.py
```

Automated through `fhir-parser.sh`.

##### (Optional, Option 2) Download FHIR classes

Clone the FHIR client repository.

```
git clone git@github.com:smart-on-fhir/client-py.git src/main/python/client-py
```

Copy FHIR classes into project:

```
cd src/main/python/
cp -r client-py/fhirclient/models/ models_full/
```

##### Back to building

Run setup tools

```
cd ../
python setup.py sdist bdist_wheel
```

Given a certain release, either available in ``dist/`` if built, or via Github, install as follows:

```
python setup.py install
```

## Usage

Run as follows:

```
python listen.py
```

The app runs by default on port 3004.

## Running the tests

```
python setup.py test
```

## Deployment

Deployment is via [Docker](https://docs.docker.com/compose/install/), and includes containers for this application and an optional message queue.

Specify the address of the FHIR server and credentials in [docker-compose](docker-compose.yml). If a hostname, reference its corresponding certificate. Also specify the address of the hostname if unlikely to be present in the DNS.

Build these containers:

```
docker-compose build
```

Run these containers:

```
docker-compose up
```

(Optional) Run without queue:

```
docker-compose up --scale webapp-queue=0 rabbit=0
```

Different docker-compose files exist to accomodate different service configurations.

## Built With

* [NLTK](https://www.nltk.org/)

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/martinchapman/nokia-health/tags).

## Authors

Produced as part of the [CONSULT project](https://consult.kcl.ac.uk/).

![CONSULT project](https://consult.kcl.ac.uk/wp-content/uploads/sites/214/2017/12/overview-consult-768x230.png "CONSULT project")

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

*
