FROM fedora:25
RUN dnf install -y git python3-pip npm && \
    npm install -g bower

ARG USER_ID=1000
RUN useradd -o -u ${USER_ID} cracker && \
    mkdir -p /opt/app && \
    chown cracker:cracker /opt/app
USER cracker

WORKDIR /opt/app
COPY ./requirements.txt /opt/app/
RUN pip3 install --user -r ./requirements.txt

# COPY ./install_static_data.sh /opt/app
# COPY ./bower.json /opt/app
# RUN ./install_static_data.sh

# the actual sources will be replaced by bind mount in development
COPY ./crack_this_container /opt/app/
USER root
RUN chown -R cracker:cracker .
USER cracker

CMD ["python3", "/opt/app/manage.py", "runserver", "-v3", "0.0.0.0:8000"]
