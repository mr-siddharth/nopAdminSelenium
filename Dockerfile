FROM python:3.8

RUN pip install selenium
RUN pip install pytest
RUN pip install openpyxl
RUN pip install pytest-html
RUN pip install requests
RUN pip install pytest-xdist

RUN mkdir -p /home/app

COPY . /home/app

EXPOSE 6969
CMD ["pip", "list"]

http://172.20.0.2:4444/wd/hub