FROM python:3.6

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

RUN apt-get -y update

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

#Copy contents
WORKDIR /app
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# Enter container shell
ENTRYPOINT ["/bin/sh"]

# The following would allow for the Docker container to automatically create a new model when it is powered on
# CMD ["python", "model.py", "1", "./diffs", "./tests"]
