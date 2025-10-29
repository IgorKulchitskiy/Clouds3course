FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY t08_flask_mysql/app/requirements.txt ./requirements.txt

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        build-essential \
        default-libmysqlclient-dev \
        pkg-config \
        wget \
        ca-certificates \
    && wget -q -O /etc/ssl/certs/BaltimoreCyberTrustRoot.crt.pem https://www.digicert.com/CACerts/BaltimoreCyberTrustRoot.crt.pem \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf /var/lib/apt/lists/*

COPY t08_flask_mysql ./t08_flask_mysql
COPY config ./config

ENV FLASK_ENV=production
ENV MYSQL_SSL_CA=/etc/ssl/certs/BaltimoreCyberTrustRoot.crt.pem
ENV MYSQL_SSL_MODE=REQUIRED

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "t08_flask_mysql.app.app:app"]
