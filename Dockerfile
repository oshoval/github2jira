FROM fedora

# Install packages
RUN dnf install -y python3 \
    git \
    pip

RUN pip install requests
RUN pip install jira

CMD [“echo”, “Hello World!”]

