FROM node:19.6.0

COPY . /zeroboost-frontend
WORKDIR /zeroboost-frontend

ENV YARN_VERSION 3.4.1

RUN yarn policies set-version $YARN_VERSION

RUN yarn install

CMD [ "yarn" , "run" , "dev" ]


