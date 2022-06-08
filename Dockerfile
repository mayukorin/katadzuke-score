FROM python:3
ENV PYTHONUNBUFFERED=1
RUN mkdir /katadzuke-score
WORKDIR /katadzuke-score
COPY requirements.txt /katadzuke-score/
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y libgl1-mesa-dev
RUN pip install -r requirements.txt
COPY . /katadzuke-score/ 