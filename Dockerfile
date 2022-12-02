FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

# install requirements
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#RUN  apt-get update \
#  && apt-get install -y netcat g++ \
#  && rm -rf /var/lib/apt/lists/*

#RUN  pipenv lock \
#  && pipenv install --system --deploy --dev

#COPY app/core/bin/wait-for/ ./app/core/bin/wait-for/
#RUN chmod u+x ./app/core/bin/wait-for/wait-for.sh

# copy source files
ADD . /code/



