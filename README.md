# README

## Download

Download anaconda from website (YES from website!):
https://www.anaconda.com/products/individual

## Conda Environment

Conda Environment is to have a virtual environment to not clutter your developer machine with test package installs

Cheatsheet: https://docs.conda.io/projects/conda/en/4.6.0/_downloads/52a95608c49671267e40c689e0bc00ca/conda-cheatsheet.pdf

### Create Environment

`conda create --name visualization-app`

### Activate Environment

`conda activate visualization-app`


### Install Prerequisites into Environment

`pip install -r requirements.txt`



# Update requirements.txt

## Write out temporary requirements-tmp.txt

Freeze into file with ALL dependencies:

`pip freeze > requirements.txt`



## Run flask app

```
Uncomment below lines in app.py to expose the Apis
# run_flask = Process(target=run_flask_app)
```