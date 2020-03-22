export LC_ALL=C.UTF-8
export LANG=C.UTF-8

export SECRET_KEY=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)
export FLASK_APP=app

if [ "$1" != '' ]; then
    export FLASK_ENV=$1
else
    export FLASK_ENV='development'
fi

export APP_SETTINGS=../app/config.py

if [ ! -e './instance' ];then
    mkdir instance
fi

if [ $FLASK_ENV == 'development' ]; then
    # Debug Mode: Using flask test server (single worker) -- Only for debug and test
    pipenv run flask run -h 0.0.0.0
elif [ $FLASK_ENV == 'production' ]; then
    # Production Mode: Using GUnicorn as WSGI to allow multi workers
    pipenv run gunicorn --workers 3 --bind 0.0.0.0:5000 wsgi 
fi

