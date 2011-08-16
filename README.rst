About
-----

*django-commitlog* - git integrated online developement.
Known to work in Django 1.3

Features
--------

* manage multimple GIT repositories
* create/uplod/modify/delete files together with GIT commits
* view commit history and its diffs for any file 
* browse file tree in any point of the repo history
* editor syntax highliting (thanx to CodeMirror 2)
* editor zen-coding for .html nad .css files ( thanx to zen-texarea.js )


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
    * support múltiple repositiories

LICENSE
-------

django-commitlog is released under the MIT License. See the LICENSE_ file for more
details.

.. _LICENSE: http://github.com:k1000/django-commitlog/blob/master/LICENSE

