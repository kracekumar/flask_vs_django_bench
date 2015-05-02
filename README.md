Django and Flask are two well known Python web frameworks. There are lot of benchmarks which claim Flask is 2x
faster for simple JSON Response, one such is [Techempower](https://www.techempower.com/benchmarks/). After looking
into the [source](https://github.com/TechEmpower/FrameworkBenchmarks/tree/master/frameworks/Python/django), it struck
me Django can do better!

I will compare Flask and Django for simple json response. The machine used is Macbook pro, `Intel Core i5-4258U CPU @ 2.40GHz`,
with `8 GB` Memory on `OS X 10.10.3`. `gunicorn==19.3.0` will be used for serving WSGI application.

    #flask simple app
    from flask import Flask, jsonify

    app = Flask(__name__)

    @app.route('/index')
    def index():
        return jsonify({'hello': 'world'})

    if __name__ == "__main__":
        app.run()

Start the flask app, `gunicorn -w 2 -b 127.0.0.1:5000 flask_app:app`.

`apachebench` will be used for benchmarking, you can use any tool for this.

    ab -n 1000 -c 2 http://localhost:5000/index
    ...
    Server Software:        gunicorn/19.3.0
    Server Hostname:        localhost
    Server Port:            5000

    Document Path:          /index
    Document Length:        22 bytes

    Concurrency Level:      2
    Time taken for tests:   0.622 seconds
    Complete requests:      1000
    Failed requests:        0
    Total transferred:      174000 bytes
    HTML transferred:       22000 bytes
    Requests per second:    1429.55 [#/sec] (mean)
    Time per request:       1.399 [ms] (mean)
    Time per request:       0.700 [ms] (mean, across all concurrent requests)
    Transfer rate:          242.91 [Kbytes/sec] received

Now let's do same thing with Django 1.8 with default settings.

    #hello/views.py
    from django.http import JsonResponse

    # Create your views here.
    def index(request):
        return JsonResponse({'hello': 'world'})

Add `url('^index/$', index),` in `urls.py` and `hello` app in `settings.py`.
Start the Django app, `gunicorn -w 2 -b 127.0.0.1:8000 django_app.wsgi`.

    ab -n 1000 -c 2 http://localhost:8000/index/
    Server Software:        gunicorn/19.3.0
    Server Hostname:        localhost
    Server Port:            8000

    Document Path:          /index/
    Document Length:        18 bytes

    Concurrency Level:      2
    Time taken for tests:   0.814 seconds
    Complete requests:      1000
    Failed requests:        0
    Total transferred:      179000 bytes
    HTML transferred:       18000 bytes
    Requests per second:    1228.25 [#/sec] (mean)
    Time per request:       1.628 [ms] (mean)
    Time per request:       0.814 [ms] (mean, across all concurrent requests)
    Transfer rate:          214.70 [Kbytes/sec] received

Time taken for 1000 requests by Django is `0.814s` and Flask is `0.622s`. Clearly flask is faster.

Django is full fledged framework but Flask is micro framework. Django comes with lot of middlewares, contrib
models etc ... Remove all those unused settings in `settings.py`.

Comment all `middleware classes`. The `settings` snippet looks like

    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',

        'hello',
    )

    MIDDLEWARE_CLASSES = (
        # 'django.contrib.sessions.middleware.SessionMiddleware',
        # 'django.middleware.common.CommonMiddleware',
        # 'django.middleware.csrf.CsrfViewMiddleware',
        # 'django.contrib.auth.middleware.AuthenticationMiddleware',
        # 'django.contrib.messages.middleware.MessageMiddleware',
        # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )

Restart the django app and run `ab -n 1000 -c 2 http://localhost:8000/index/`.

    Server Software:        gunicorn/19.3.0
    Server Hostname:        localhost
    Server Port:            8000

    Document Path:          /index/
    Document Length:        18 bytes

    Concurrency Level:      2
    Time taken for tests:   0.560 seconds
    Complete requests:      1000
    Failed requests:        0
    Total transferred:      150000 bytes
    HTML transferred:       18000 bytes
    Requests per second:    1784.37 [#/sec] (mean)
    Time per request:       1.121 [ms] (mean)
    Time per request:       0.560 [ms] (mean, across all concurrent requests)
    Transfer rate:          261.38 [Kbytes/sec] received

Now Django took only `0.560s` for 1000 requests compared to flask `0.622s`.

Now remove Django admin from `urls.py`, and remove all `contrib` apps in `INSTALLED_APPS`.

    INSTALLED_APPS = (
    #'django.contrib.admin',
    #'django.contrib.auth',
    #'django.contrib.contenttypes',
    #'django.contrib.sessions',
    #'django.contrib.messages',
    #'django.contrib.staticfiles',

    'hello',
    )

Restart the Django app and run the benchmark `ab -n 1000 -c 2 http://localhost:5000/index`.

    Server Software:        gunicorn/19.3.0
    Server Hostname:        localhost
    Server Port:            8000

    Document Path:          /index/
    Document Length:        18 bytes

    Concurrency Level:      2
    Time taken for tests:   0.553 seconds
    Complete requests:      1000
    Failed requests:        0
    Total transferred:      150000 bytes
    HTML transferred:       18000 bytes
    Requests per second:    1806.90 [#/sec] (mean)
    Time per request:       1.107 [ms] (mean)
    Time per request:       0.553 [ms] (mean, across all concurrent requests)
    Transfer rate:          264.68 [Kbytes/sec] received


That is much better. While developing API based application in Django tweak your setting to get
better performance out of Django.
