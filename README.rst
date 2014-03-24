=======
AMS
=======
Ams is a simple Django app to accident's management.

Quick start
-----------

1. Add "ams" to your INSTALLED_APPS setting like this::

       INSTALLED_APPS = (
          ...
          'ams',
       )

2. Include the polls URLconf in your project urls.py like this::

    url(r'^ams/', include('ams.urls')),

 3. Create or change conf.ini file in root of your django project to add next::

   [smtp_ip]
   smtp_ip =

   [smtp_port]
   smtp_port =

   [send_from]
   from = no-reply@mail.com

   [send_to]
   to1 = user@mail.com
   to2 =  

