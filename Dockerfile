FROM python:3.11-alpine


WORKDIR /app


COPY . /app


RUN pip install -r requirements.txt


ENV GUNICORN_WORKERS=1
ENV GUNICORN_BIND=0.0.0.0:8000
ENV GUNICORN_WORKER_CLASS=geventwebsocket.gunicorn.workers.GeventWebSocketWorker
ENV GUNICORN_APP_MODULE='social_app:create_app()'


EXPOSE 8000


CMD gunicorn -w $GUNICORN_WORKERS -b $GUNICORN_BIND -k $GUNICORN_WORKER_CLASS -n social_app $GUNICORN_APP_MODULE
