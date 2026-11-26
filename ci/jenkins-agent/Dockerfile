FROM jenkins/inbound-agent:3396.ve02b_5cde31b_2-4-jdk21

USER root

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-venv \
    python3-pip \
    nodejs \
    npm \
    docker-cli \
    git \
    ca-certificates \
    && command -v docker \
    && docker --version \
    && rm -rf /var/lib/apt/lists/*


RUN if getent group docker >/dev/null; then \
        groupmod -g 112 docker; \
    else \
        groupadd -g 112 docker; \
    fi \
    && usermod -aG docker jenkins

USER jenkins