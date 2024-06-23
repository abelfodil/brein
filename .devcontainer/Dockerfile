FROM mcr.microsoft.com/vscode/devcontainers/base:ubuntu-24.04

RUN apt-get update && apt-get install -y apt-transport-https pipx python3-pip python3-venv

# Workaround for https://github.com/devcontainers/images/issues/1056
RUN userdel -r ubuntu || true

USER vscode
