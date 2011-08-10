About
-----

*django-commitlog* - view GIT commit log.
Known to work in Django 1.3


Installation
------------

1. Requires GitPython http://packages.python.org/GitPython/0.3.2/index.html::
        
        pip  install GitPython

2. Download and install::

        git clone git@github.com:k1000/django-commitlog.git
        cd django-commitlog
        python setup.py install

   or using pip::     
    
        pip install -e git@github.com:k1000/django-commitlog.git#egg=commitlog

3. Add "commitlog" to your INSTALLED_APPS in "settings.py" 

TODO
----
    * views
    * diffs

LICENSE
-------

django-commitlog is released under the MIT License. See the LICENSE_ file for more
details.

.. _LICENSE: http://github.com:k1000/django-commitlog/blob/master/LICENSE

