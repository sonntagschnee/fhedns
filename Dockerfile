FROM rockylinux:9
WORKDIR /app
RUN dnf update -y
RUN dnf install python3-pip -y
RUN python3 -m pip install wheel setuptools concrete-python
ADD app /app
