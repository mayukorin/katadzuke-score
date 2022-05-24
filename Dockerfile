FROM python:3
ENV PYTHONUNBUFFERED=1
RUN mkdir /katadzuke-score
WORKDIR /katadzuke-score
COPY requirements.txt /katadzuke-score/
RUN pip install -r requirements.txt
COPY . /katadzuke-score/ 