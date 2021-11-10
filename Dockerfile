FROM fedora:32

RUN dnf install -y python3 git pip \
    && dnf clean all \
    && rm -rf /var/cache/yum

RUN pip install requests jira

CMD [“echo”, “Hello World”]

