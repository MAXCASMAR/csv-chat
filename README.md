# Conversa con tu CSV

Este repositorio está dedicado a facilitar la interacción y manipulación de datos CSV de una manera amigable, permitiendo cargar datos a una base de datos Postgres e interactuar con ellos mediante lenguaje natural.

## Componentes Principales

- `CSVLoader.py`: Esta clase es responsable de cargar datos de archivos CSV y transformarlos para su inserción en una tabla de una base de datos Postgres.

- `CSVChat.py`: Utiliza lenguaje natural para consultar y manipular los datos contenidos en tu CSV a través de las transformaciones aplicadas por `CSVLoader.py`.

- `handler.py`: Es la función principal de una AWS Lambda Function y actúa como el punto de entrada para el API endpoint.

- `PostgresDatabase.py`: Proporciona métodos de interacción con una base de datos Postgres, facilitando la ejecución de consultas SQL.

## Configuración de API Keys

Para el funcionamiento completo de las herramientas proporcionadas en este repositorio, necesitarás configurar las siguientes claves:

1. Claves para el motor de IA que desees utilizar (por defecto `mixtral-8x7b-instruct-v0.1`):
   - `REPLICATE_API_TOKEN`: Obtenible desde https://replicate.com/
   - `OPENAI_API_KEY`: Obtenible desde https://openai.com/

2. Claves de la base de datos para acceder e interactuar con tus tablas Postgres. Estas claves pueden ser provistas por servicios como RDS en AWS, u otro servicio de base de datos Postgres que prefieras.

## Ejecución en Entorno Local

Para probar y ejecutar las herramientas localmente, sigue estos pasos:

1. Navega hacia la carpeta `src`:
   ```sh
   cd src
   ```

2. Instala las dependencias necesarias:
   ```sh
   pip install -r requirements.txt
   ```

3. Ejecuta `CSVLoader.py` para cargar los datos de tu archivo CSV a la base de datos:
   ```sh
   python3 CSVLoader.py
   ```

4. Con los datos ya cargados en la base de datos, ejecuta `CSVChat.py` para interactuar con la tabla resultante. Puedes modificar la consulta dentro del script según tus necesidades:
   ```sh
   python3 CSVChat.py
   ```

## Despliegue de la API

Para desplegar la API utilizando AWS y Serverless Framework, sigue estos pasos:

1. Instala Serverless y sus dependencias, y autentícate en AWS con tus claves ejecutando:
   ```sh
   make install-lambda
   ```

2. Actualiza los valores de `SERVICE_NAME`, `ACCOUNT_ID` y `BUCKET_NAME` en el archivo `serverless.yml`. Crea el rol o bucket de S3 si es necesario.

3. Revisa y ajusta el código si se requiere, y asegúrate de que las configuraciones en `serverless.yml` son correctas para tu caso de uso.

4. Despliega tu función Lambda utilizando el comando proporcionado en el archivo `Makefile`:
   ```sh
   make deploy-lambda
   ```

Lee detalladamente la documentación en los comentarios del código y asegúrate de realizar las configuraciones correspondientes para tus claves y recursos de AWS. Con estos pasos, tu API debería estar funcionando y lista para ser consumida.

## Prueba del API Endpoint
Se puede probar el API deployeada en el jupyter_notebook test_api_endpoint con diferentes preguntas, es la manera más rápida de probar el funcionamiento de este proyecto. 