git clone https://github.com/mrios01/metrobusCDMX.git \
cd metrobusCDMX \

sudo docker build -t local/metrobus_api:beta .\
sudo docker run -p 8000:8000 local/metrobus_api:beta\
\
or\
\
sudo docker-compose up\
\
In your browser run:

![alt text](https://github.com/mrios01/metrobusCDMX/blob/main/img/img0.jpg)

![alt text](https://github.com/mrios01/metrobusCDMX/blob/main/img/img1.jpg)

![alt text](https://github.com/mrios01/metrobusCDMX/blob/main/img/img02.jpg)

![alt text](https://github.com/mrios01/metrobusCDMX/blob/main/img/img03.jpg)

Flow Diagram for DataPipeline:


