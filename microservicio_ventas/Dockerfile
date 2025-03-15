FROM python:3.12
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app

ENV FLASK_APP=app.py

EXPOSE 5000
ENTRYPOINT [ "gunicorn" ]
CMD ["-b", "0.0.0.0:5000", "app:app"]
