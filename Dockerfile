# Dockerfile to run entire app in a local container.
FROM python:3.9
WORKDIR /udacity_capstone_project_local
COPY Pipfile .
COPY Pipfile.lock .
RUN python -m pip install --upgrade pip
RUN pip install -U pipenv==2018.11.26
RUN pipenv install
COPY . .
ENV PYTHONPATH=$PATHONPATH:`pwd`
CMD pipenv run bash
