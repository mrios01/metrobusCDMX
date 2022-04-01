git clone https://github.com/mrios01/metrobusCDMX.git
cd metrobusCDMX

sudo docker build -t local/metrobus_api:beta .
sudo docker run -p 8000:8000 local/metrobus_api:beta

or

sudo docker-compose up