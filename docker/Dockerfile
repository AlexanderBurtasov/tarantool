FROM ubuntu:bionic

# install these utilities if they are missing
RUN apt-get -y install sudo && \
    sudo apt-get -y install gnupg2 && \
    sudo apt-get -y install curl

RUN curl https://download.tarantool.org/tarantool/2.2/gpgkey | sudo apt-key add -

# install the lsb-release utility and use it to identify the current OS code name;
# alternatively, you can set the OS code name manually, e.g. stretch
RUN apt-get -y install lsb-release && \
    release=`lsb_release -c -s`

# install https download transport for APT
RUN apt-get -y install apt-transport-https

# append two lines to a list of source repositories
RUN sudo rm -f /etc/apt/sources.list.d/*tarantool*.list && \
    echo "deb https://download.tarantool.org/tarantool/2.2/ubuntu/ ${release} main" | sudo tee /etc/apt/sources.list.d/tarantool_2_2.list && \
    echo "deb-src https://download.tarantool.org/tarantool/2.2/ubuntu/ ${release} main" | sudo tee -a /etc/apt/sources.list.d/tarantool_2_2.list

# install tarantool
RUN sudo apt-get -y update && \
    sudo apt-get -y install tarantool

