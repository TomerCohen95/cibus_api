FROM mcr.microsoft.com/playwright:focal


WORKDIR /app

COPY . .

RUN pip install -r requirements.txt
RUN playwright install

CMD [ "python3", "cibus_api.py"]
