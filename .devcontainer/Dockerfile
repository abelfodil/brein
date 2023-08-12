FROM mcr.microsoft.com/vscode/devcontainers/base:ubuntu-22.04

RUN apt-get update && apt-get install -y build-essential pkg-config

USER vscode

RUN curl https://sh.rustup.rs -sSf | sh -s -- --default-toolchain stable -y

ENV PATH "/home/vscode/.cargo/bin:${PATH}"

RUN rustup component add cargo clippy rls rustfmt rust-std rust-docs rls rust-src rust-analysis
