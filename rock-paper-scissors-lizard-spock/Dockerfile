FROM python:3

WORKDIR /usr/src/app

ENV RPSLS_ROUNDS 50

# COPY requirements.txt ./
# RUN pip install --no-cache-dir -r requirements.txt

COPY rpsls.py .
CMD [ "python", "./rpsls.py" ]
