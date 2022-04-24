FROM python:3.10

COPY ./techtrends/requirements.txt /home/app/techtrends/requirements.txt
COPY ./techtrends /home/app/techtrends/
WORKDIR /home/app/techtrends/
RUN pip install -r requirements.txt
RUN python init_db.py
EXPOSE 3111

#CMD ["flask", "run", "-h '0.0.0.0'", "-p 3111"]
CMD ["python", "-m", "app"]
