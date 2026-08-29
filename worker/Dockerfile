FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive ANDROID_HOME=/opt/android-sdk
RUN apt-get update && apt-get install -y openjdk-17-jdk git curl unzip zip ca-certificates python3 python3-pip && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /opt/android-sdk /workspace /artifacts
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --break-system-packages -r /tmp/requirements.txt
COPY server.py /server.py
RUN useradd -m -u 10001 builder && chown -R builder:builder /workspace /artifacts /opt/android-sdk
USER builder
EXPOSE 8787
CMD ["python3","/server.py"]