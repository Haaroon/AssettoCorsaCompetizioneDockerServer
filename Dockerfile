# Ubuntu Base
FROM ubuntu:20.04
# Change workdir
WORKDIR /root/
# Change to multi architecture system
RUN dpkg --add-architecture i386 \
    && apt-get update \
    && apt-get install -y libc6:i386 \
    && apt-get install -f
# Install WGET
RUN  apt-get update \
  && apt-get install -y wget unzip gnupg software-properties-common
# Unzip file personal Assetto Corsa Competizione Server (download from steam and save as zip file)
RUN unzip acc.zip -d /root/ \
    && rm -rf /root/__MACOSX \
    && rm -rf /root/acc.zip \
    && rm -rf /root/acc/cfg
# Add winekey
#RUN wget -nc https://dl.winehq.org/wine-builds/winehq.key \
#        && apt-key add winehq.key \
#        && add-apt-repository 'deb https://dl.winehq.org/wine-builds/ubuntu/ focal main' \
#        && apt-get update
# Now install Wine
ENV WINEARCH=win64
RUN apt-get install -y wine64 wine32
# Install VC Speicif files
RUN apt-get update && apt-get install -y xvfb
RUN Xvfb :1 -ac -pixdepths 8 16 24 32 -screen 0 1024x768x24 +extension GLX +extension RANDR +render -noreset &
RUN wget  https://raw.githubusercontent.com/Winetricks/winetricks/master/src/winetricks && chmod +x winetricks && mv winetricks /usr/local/bin
RUN set -xe						&& \
	WINEDLLOVERRIDES="mscoree,mshtml=" xvfb-run wine wineboot && \
	xvfb-run wineserver -w 		&& \
	xvfb-run winetricks -q vcrun2015
# Copy server config
COPY serverConfigs/settings.json /root/acc/server/cfg/
COPY serverConfigs/event.json /root/acc/server/cfg/
COPY serverConfigs/entrylist.json /root/acc/server/cfg/
COPY serverConfigs/configuration.json  /root/acc/server/cfg/
# Forward the ports
EXPOSE 9231/udp
EXPOSE 9232/tcp
WORKDIR /root/acc/server/
# Run the server
CMD ["/bin/bash", "wine", "/root/acc/server/accServer.exe"]

