FROM bwits/pdf2htmlex-alpine

RUN echo "**** install Python ****" && \
    apk add --no-cache python3 && \
    if [ ! -e /usr/bin/python ]; then ln -sf python3 /usr/bin/python ; fi && \
    \
    echo "**** install pip ****" && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --no-cache --upgrade pip setuptools wheel && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi


###########################################################################
# WEBSERVICE START:
# It's a python script wich will start a web service where
# we will send the filename and the conversion options.
###########################################################################


CMD ["sh", "/init.sh"]

EXPOSE 8085
