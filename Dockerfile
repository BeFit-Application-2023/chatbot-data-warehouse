FROM tiangolo/uwsgi-nginx-flask:python3.7

WORKDIR /data-warehouse
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

EXPOSE 7777

ENV FLASK_APP=main.py

CMD ["python", "-u", "main.py"]