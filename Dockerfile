FROM python:3
RUN mkdir app/
ADD app app/
COPY requirements.txt /tmp
COPY main.py /
RUN pip install -r /tmp/requirements.txt
CMD ["python", "/main.py"]