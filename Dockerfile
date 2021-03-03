FROM node:14.3.0 AS frontend
COPY frontend/ /frontend
WORKDIR /frontend
RUN npm i --no-optional
RUN npm run build

FROM python:3.8
RUN sed 's/SECLEVEL=[0-9]/SECLEVEL=1/g' /etc/ssl/openssl.cnf > /etc/ssl/openssl.cnf

COPY requirements.txt /
RUN pip install -r requirements.txt

COPY backend/ /
COPY --from=frontend /frontend/build /static

ENV PRODUCTION=1

CMD ["gunicorn","-b","0.0.0.0:80","-k","uvicorn.workers.UvicornWorker","--forwarded-allow-ips","*","--proxy-allow-from","*","app:app"]
