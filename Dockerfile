FROM python:3
RUN mkdir app
ADD app app/
COPY requirements.txt /tmp
COPY main.py /
RUN chmod 0744 /main.py
RUN pip3.9 install -r /tmp/requirements.txt
CMD ["python", "main.py"]