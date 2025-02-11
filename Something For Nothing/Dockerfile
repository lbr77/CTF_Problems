FROM ubuntu:24.04 AS base
RUN apt update && apt upgrade -y && apt install -y python3-pip curl git
RUN python3 -m pip install --break-system-packages web3==6.20.3 py-solc-x==2.0.3
ENV PATH="$PATH:/root/.foundry/bin"
RUN curl -L https://foundry.paradigm.xyz | bash && foundryup
WORKDIR /app

FROM base AS compile
COPY . .
RUN forge install --no-git && forge install OpenZeppelin/openzeppelin-contracts --no-git 
RUN forge build

FROM base AS run
COPY --from=compile /app/out /app/out
RUN mkdir /root/.solcx && wget https://ghfast.top/https://github.com/ethereum/solidity/releases/download/v0.8.27/solc-static-linux -O  /root/.solcx/solc-v0.8.27
COPY deploy_and_run.py .
RUN apt install -y socat

CMD ["socat", "TCP-LISTEN:9999,reuseaddr,fork", "EXEC:python3 deploy_and_run.py"]
