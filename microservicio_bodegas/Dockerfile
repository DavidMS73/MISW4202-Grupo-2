FROM python:3.10
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app

ENV FLASK_APP=app.py

EXPOSE 5000
ENTRYPOINT [ "gunicorn" ]
CMD ["-b", "0.0.0.0:5000", "app:app"]
