FROM apache/spark:3.5.5

USER root
RUN pip3 install boto3

USER spark