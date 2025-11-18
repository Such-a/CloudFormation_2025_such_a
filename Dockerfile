# Use Ubuntu 22.04 base image
ARG RELEASE
ARG LAUNCHPAD_BUILD_ARCH
FROM ubuntu:22.04

# Labels
LABEL org.opencontainers.image.ref.name="ubuntu"
LABEL org.opencontainers.image.version="22.04"
LABEL maintainer="Grafana Labs <hello@grafana.com>"
LABEL org.opencontainers.image.source="https://github.com/grafana/grafana"

# Args for Grafana user/group
ARG GF_UID=472
ARG GF_GID=0

# Environment variables
ENV PATH=/usr/share/grafana/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
    GF_PATHS_CONFIG=/etc/grafana/grafana.ini \
    GF_PATHS_DATA=/var/lib/grafana \
    GF_PATHS_HOME=/usr/share/grafana

# Set working directory
WORKDIR /usr/share/grafana

# Copy Grafana files
COPY /tmp/grafana/conf ./conf
COPY /tmp/grafana/bin/grafana* /tmp/grafana/bin/*/grafana* ./bin/
COPY /tmp/grafana/public ./public
COPY /tmp/grafana/LICENSE ./

# Expose Grafana port
EXPOSE 3000

# Copy entrypoint script
ARG RUN_SH=./packaging/docker/run.sh
COPY ./packaging/docker/run.sh /run.sh

# Set user
USER 472

# Default command
ENTRYPOINT ["/run.sh"]
CMD ["/bin/bash"]
