![Build Status](https://github.com/Alfareiza/ScrappingColombianNewspapers/actions/workflows/main/badge.svg)

# Scrapping Colombian Newspapers 

:shipit: Scrapping information of Colombian newspapers.

## Getting Started

Repository that captures information from Colombian newspapers (list of newspapers), then generates a csv with all the information.

### Prerequisites

Pip and Python installed and configured as environment variables. Then, install pipenv.

```
pip install pipenv
```

### Installing

Install pipenv in order to isolate your enviroment.

```
pipenv install -d
```

And then

```
python scrapproject/main.py
```

Will be generated a csv (all_news.csv) with all the information captured at the moment of the execution of the line above.

At the moment, the list of scrapped sites is [20]:
- elheraldo
- zonacero
- elpilon
- eluniversal
- diariodelcesar
- hoydiariodelmagdalena
- diariodelnorte
- laopinion
- eltiempo
- elcolombiano
- elespectador
- lapatria
- elpais
- elmundo
- elnuevodia
- elmanduco
- semana
- publimetro
- pulzo
- larepublica

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## How to contribute

All code follows PEP8, except for the lenght of line, which contains 120 characters. Every function /class/method/module must have docstrings.

1. Fork the project and clone or project: git clone git@github.com:<your_user>/ScrappingColombianNewspapers.git
2. Install pipenv: pip install pipenv
3. Install the dependencies of dev: pipenv install -d
4. Develop the feature with tests
5. un the tests locally: pipenv run pytest
6. Submit the pull request with testing in a single commit
7. Submit the PR for review
8. After revised and corrected, the PR will be accepted and the lib will be posted to PyPi
9. Put your name and username in the contributors portion

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 


## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
