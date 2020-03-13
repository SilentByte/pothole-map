
![Pothole Map](pothole-map.png)

[![Pothole Map](https://img.shields.io/badge/app-pothole--map-3f51b5.svg?style=for-the-badge)](https://pothole-map.silentbyte.com)&nbsp;
[![Pothole Map Version](https://img.shields.io/badge/version-1.0-05a5cc.svg?style=for-the-badge)](https://pothole-map.silentbyte.com)&nbsp;
[![Pothole Map Status](https://img.shields.io/badge/status-live-00b20e.svg?style=for-the-badge)](https://pothole-map.silentbyte.com)


# Pothole Map

This repository contains the source code of Pothole Map, an interactive visualization of pothole locations that have been discovered by using artificial intelligence.


# How Does it Work?

TODO


# Development

*   Install app dependencies:
    ```bash
    $ cd app
    $ npm install
    ```

*   Set app environment variables by creating the file `.env.local` with the following variables. You'll need a [Google Maps API key](https://developers.google.com/maps/documentation/javascript/get-api-key).
    ```bash
    VUE_APP_GOOGLE_MAPS_API_KEY=YOUR_GOOGLE_MAPS_KEYS
    VUE_APP_API_URL=http://localhost:8888
    ```

*   Start app in development mode:
    ```bash
    $ npm run dev
    ```

*   Create a Python virtual environment and install lambda dependencies:
    ```bash
    $ cd lambdas
    $ virtualenv --python python3 venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt
    $ npm install
    ```

*   Set lambda environment variables by creating the file `.env.development` with the following variables:
    ```bash
    DEBUG=True
    PRODUCTION=False

    QUERY_MAX_RESULT_COUNT=100
    QUERY_DEFAULT_RESULT_COUNT=10

    PHOTO_BUCKET_NAME=S3_BUCKET_NAME
    PHOTO_KEY_PREFIX=potholes/

    DB_HOST=YOUR_DATABASE_HOST
    DB_PORT=YOUR_DATABASE_PORT
    DB_NAME=YOUR_DATABASE_NAME
    DB_USER=YOUR_DATABASE_USER
    DB_PASSWORD=YOUR_DATABASE_PASSWORD
    ```

*   Start lambdas in development mode:
    ```bash
    $ npm run dev
    ```


# Building & Deployment

*   Run the following commands to create a production build of the front-end app. The content of the resulting `dist/` folder can be uploaded onto any static site hosting provider. We're using [Firebase](https://firebase.google.com/).
    ```bash
    $ cd app
    $ npm run build
    ```

*   Deploy lambdas using serverless:
    ```bash
    $ cd lambdas
    $ npm run deploy
    ```


# License

MIT, see [LICENSE.txt](LICENSE.txt).
