FROM python:3.8-slim-buster
# WORKDIR /app
COPY requirements.txt requirements.txt
RUN python -m pip install --upgrade py4web --no-cache-dir
Run py4web setup apps -Y
COPY ./src /apps/Charitably
# CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=8085"]
CMD ["py4web", "run","-H", "172.17.0.2", "apps"]

# TODO !!!
# 1. Install py4web
# 2. Perform first run procedure
# 3. Set password for dash board (use encrypted password file?
# 4. Copy app in to correct dir
# 5. Restart ???
# 6. Find way to setup without extra crap
# 7. Find way to programatically set host address
