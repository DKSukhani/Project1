FROM dipeshsukhani/ubuntu:latest
WORKDIR /home
ADD . /home
RUN alias pip=pip3
RUN alias python=python3
RUN pip3 install -r requirements.txt
RUN pip3 install psycopg2
CMD tail -f /dev/null