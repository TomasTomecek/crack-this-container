FROM registry.fedoraproject.org/fedora:28
RUN dnf install -y git python3-pip npm python3-psycopg2

ARG USER_ID=1000
RUN useradd -o -u ${USER_ID} cracker && \
    mkdir -p /opt/app && \
    chown cracker:cracker /opt/app
USER cracker

WORKDIR /opt/app
COPY ./requirements.txt /opt/app/
RUN pip3 install --user -r ./requirements.txt

COPY ./package.json /opt/app
RUN npm install

# the actual sources will be replaced by bind mount in development
COPY ./crack_this_container /opt/app/crack_this_container/
WORKDIR /opt/app/crack_this_container
USER root
RUN chown -R cracker:cracker /opt/app/
USER cracker

CMD ["python3", "./manage.py", "runserver", "-v3", "0.0.0.0:8000"]
