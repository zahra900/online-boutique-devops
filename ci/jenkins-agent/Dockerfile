FROM jenkins/inbound-agent:3396.ve02b_5cde31b_2-4-jdk21

USER root

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-venv \
    python3-pip \
    nodejs \
    npm \
    docker.io \
    git \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*


RUN existing_gid=$(getent group docker | cut -d: -f3) \
    && if [ "$existing_gid" != "112" ]; then \
         groupmod -g 112 docker; \
       fi \
    && usermod -aG docker jenkins

USER jenkins