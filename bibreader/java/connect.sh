# voir https://stackoverflow.com/questions/9717477/java-rxtxcomm-lib-to-connect-to-dev-ttyacm0
# RXTXcomm ne reconnait pas /dev/ttyACM0 comme un port série
# il est nécessaire créer un lien avec un nom commun (/dev/ttyS..)
# le numéro 80 est quasiment certainement indéfini donc utilisable
sudo ln -s /dev/ttyACM0 /dev/ttyS80
