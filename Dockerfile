FROM public.ecr.aws/lambda/python:3.9

COPY app/requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt  --target "${LAMBDA_TASK_ROOT}"

COPY app ${LAMBDA_TASK_ROOT}/app

ENV DATA_PATH=/data
ENV CONFIG_PATH=/config

VOLUME /data
VOLUME /config

CMD ["app.main.lambda_handler"]
