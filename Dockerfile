FROM python:3.7

RUN apt update && apt upgrade -y
COPY requirements.txt .
RUN pip install -r requirements.txt
copy . /

ENTRYPOINT ["python"]
CMD ["run.py"]

EXPOSE 5000
