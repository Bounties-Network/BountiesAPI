 FROM python:3
 ENV PYTHONUNBUFFERED 1
 ARG auto_build="true"
 ENV auto_build=$auto_build
 RUN mkdir /code
 WORKDIR /code
 ADD requirements.txt /code/
 RUN pip install -r requirements.txt
 ADD . /code/
 EXPOSE 83 