FROM fedora

# Install packages
RUN dnf install -y python3 \
    git \
    pip

RUN git clone https://github.com/oshoval/github2jira.git
RUN pip install --user requests

CMD [“echo”, “Hello World!”]

