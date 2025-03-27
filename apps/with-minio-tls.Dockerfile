FROM apache/spark:3.5.5

USER root

COPY minio-public.crt /usr/local/share/ca-certificates/minio-public.crt

RUN update-ca-certificates

RUN keytool -importcert \
  -noprompt \
  -trustcacerts \
  -alias minio \
  -file /usr/local/share/ca-certificates/minio-public.crt \
  -keystore $JAVA_HOME/lib/security/cacerts \
  -storepass changeit

USER spark