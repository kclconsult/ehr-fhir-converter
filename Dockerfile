FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src/ .

# Later ensures rabbitmq start can be waited for.
RUN git clone https://github.com/vishnubob/wait-for-it.git

EXPOSE 3004
CMD [ "python", "receive.py" ]
