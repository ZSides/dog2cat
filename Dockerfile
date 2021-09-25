FROM nvidia/cuda:10.0-cudnn7-devel-ubuntu18.04

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
ENV PATH=/usr/local/cuda-10.0/bin:$PATH \
   LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH \
   LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH \
   LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda-10.0/lib64/ \
   LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib

RUN apt-get update && apt-get install -y git python3-dev python3-pip python3-opencv

RUN pip3 install tensorflow torch

RUN cd /usr/share; git clone https://github.com/taki0112/UGATIT; cd UGATIT; mkdir checkpoint; mkdir static; mkdir dataset; cd dataset; mkdir cat2dog; mkdir cat2dog/testA; mkdir cat2dog/testB; rm -rf ../ass*

COPY UGATIT_light_cat2dog_lsgan_4resblock_6dis_1_1_10_10_1000_sn /usr/share/UGATIT/checkpoint/UGATIT_light_cat2dog_lsgan_4resblock_6dis_1_1_10_10_1000_sn/.

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV FLASK_APP=f
RUN pip3 install flask
COPY f.py /usr/share/UGATIT/f.py
EXPOSE 5000
WORKDIR /usr/share/UGATIT
CMD [ "flask", "run", "--host=0.0.0.0" ]
