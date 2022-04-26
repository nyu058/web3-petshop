FROM python:3.9
RUN curl -sL https://deb.nodesource.com/setup_16.x | bash - ; \
    apt-get install nodejs -y ;\
    npm install -g truffle ganache solc;\
    pip install flask web3
COPY . /app
WORKDIR /app
EXPOSE 5001
ENTRYPOINT ["/bin/bash", "run.sh"]