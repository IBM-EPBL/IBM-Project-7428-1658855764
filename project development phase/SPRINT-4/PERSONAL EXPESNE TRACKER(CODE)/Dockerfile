
FROM python:3.10.6


ENV PYTHONUNBUFFERED 1
WORKDIR /app

ADD . /personal_expense_tracker

COPY ./requirements.txt /app/requirements.txt

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 3000
COPY . /app

CMD [ "python" ]


# ENV PYTHONUNBUFFERED 1
# WORKDIR /app              
# COPY env/requirements.txt ./  
# RUN pip install -r requirements.txt
# COPY ./ ./

# # add the following
# WORKDIR /app/project      
# EXPOSE 8000               
# CMD python3 ./app.py runserver 0.0.0.0:5000  
# WORKDIR /code

# COPY env/requirements.txt ./

# RUN pip install --upgrade pip

# RUN set -e \
#         apk add --no-cache --virtual .build-deps \
#                 gcc \
#                 libc-dev \
#                 linux-headers \
#                 mariadb-dev \
#                 python3-dev \
#                 postgresql-dev 
        

# RUN pip install -r requirements.txt

# COPY  . .

# # RUN py -m venv env 

# EXPOSE 5000

# ENTRYPOINT [ "python3" ]

# CMD ["app.py" ]