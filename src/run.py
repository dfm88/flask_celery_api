from project import create_app, ext_celery

app = create_app()
celery = ext_celery.celery

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)