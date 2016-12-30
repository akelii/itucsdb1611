Developer Guide
===============

Database Design
---------------

**Modern way of working!**

Academic Freelance offers you to work on ITU projects which vary and we guarantee that you will find YOUR project to work on!

Every members of ITU can register and create projects. You will develop your skills by working on professional projects and  connect new people from the university!


    Following diagram shows Academic Freelance database design. In Academic Freelance, fifteen dynamic and seven look-up tables ara implemented, which means totally twenty two tables are used.

.. image:: DB_ER.png
      :scale: 100 %
      :align: center
      :alt: Academic Freelance Entity Relation Diagram


Code
----

**Note:** File folders indexing is following:

    - *./classes* includes class description which depends the entities coming from database.
    - *./classes/operations* includes class methods.
    - *./static* file includes css and javascript files.
    - *./templates* includes HMTL files which means front-end side.
    - *./templates_operations* includes python code related to HTML files which means server side development.

Installation
------------

**Academic Freelance** uses PostgreSQL and Python 3.5 so you need to install postgresql locally or use vagrant.

Jinja2 is used for templating language for Pyhton Flask Framework.


.. code-block:: python

    @app.route('/', methods=['GET', 'POST'])
    def profile():
    ## some Python Code




Folllowing code partition shows global User Information **GET** function description using *context_processor*

.. code-block:: python

    @app.context_processor
    def CurrentUserInfo():
    if hasattr(current_user, 'email'):
        person = person_operations().GetPerson(current_user.email)

        return dict(full_name=person[1], title=person[6], photopath=person[7])
    else:
        return dict(full_name='')



For each python code is binding to user interface using template which means there is layout (or master) html page and sending information from
server side is printed Jinja 2 to html document.

.. code-block:: python

    ## HTML templates ##
    <div class="content-wrapper">
        {% block container %}{% endblock %}
    </div>
    ## HTML templates ##

.. toctree::
   member1
   member2
   member3
   member4
   member5
