FROM python:3.12
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app

ENV FLASK_APP=app.py
ENV BODEGAS_HOST=http://bodegas:5000
ENV VENTAS_HOST=http://ventas:5000

EXPOSE 5000
ENTRYPOINT [ "gunicorn" ]
CMD ["-b", "0.0.0.0:5000", "app:app"]
