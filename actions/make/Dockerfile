FROM docker:18.09.7
LABEL "com.github.actions.name"="Makefile runner"
LABEL "com.github.actions.description"="A docker base image that can run make"
LABEL "com.github.actions.icon"="code"
LABEL "com.github.actions.color"="gray-dark"
LABEL "maintainer"="abatilo"

RUN apk add make=4.2.1-r2 bash=5.0.0-r0
COPY ./entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]
