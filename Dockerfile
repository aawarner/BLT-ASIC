FROM python:3.7.2
LABEL maintainer="aawarner@cisco.com"
COPY BLT /home/blt
WORKDIR /home/blt
RUN pip install -r /home/blt/requirements.txt && chmod +x start.sh && groupadd -r blt \
&& useradd -r -g blt blt && mkdir /home/creds && chown -R blt /home/creds \
&& chown -R blt /home/blt
USER blt
EXPOSE 5000
ENTRYPOINT ["/bin/bash", "./start.sh"]
