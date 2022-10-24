FROM python:3-slim

# For healthcheck
RUN apt-get update && apt-get install curl -y

# Install python requirements
COPY requirements.txt /tmp/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements.txt

# Copy server files
COPY rfSsdpServer.py redfishMockupServer.py /usr/src/app/
COPY server.crt server.key /usr/src/app/

# Env settings
EXPOSE 8000
#HEALTHCHECK CMD curl --fail https://127.0.0.1:8000/redfish/v1 || exit 1
WORKDIR /usr/src/app
ENTRYPOINT ["python", "/usr/src/app/redfishMockupServer.py", "-H", "0.0.0.0", "-D", "/usr/src/app/instance", "-s", "--cert", "/usr/src/app/server.crt", "--key", "/usr/src/app/server.key"]