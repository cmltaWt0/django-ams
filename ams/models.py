# -*- coding: utf-8 -*-

from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.db.models.signals import post_save
from django.contrib.comments.signals import comment_was_posted
from django.dispatch import receiver

import os
import ConfigParser
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate

import errno
from socket import error as socket_error


def fetcher(key):
    """
    fetcher(key: str) -> function fetcher
    """
    a = {}
    config = ConfigParser.RawConfigParser()
    config.read(PATH + '/../conf.ini')
    items = config.items(key)

    a[key] = [item[1] for item in items if item[1] != '']

    return a


from django.conf import settings
PATH = settings.PROJECT_PATH

SEND_TO = fetcher('send_to')
SEND_FROM = fetcher('send_from')
SMTP_IP = fetcher('smtp_ip')
SMTP_PORT = fetcher('smtp_port')


class Phone(models.Model):
    number = models.CharField(max_length=20)

    def __unicode__(self):
        return self.number

    class Meta:
        verbose_name_plural = "Телефоны"


class State(models.Model):
    title = models.CharField(max_length=10)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Состояния"


class AbstractEmployee(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40, blank=True)
    post = models.CharField(max_length=50, blank=True)
    email = models.EmailField('E-mail', blank=True)
    phone = models.ManyToManyField(Phone, blank=True, related_name="%(app_label)s_%(class)s_related")

    def __unicode__(self):
        return '%s %s' % (self.first_name, self.last_name)

    class Meta:
        abstract = True


class Engineer(AbstractEmployee):
    class Meta:
        verbose_name_plural = "Инженеры"


class Publisher(AbstractEmployee):
    class Meta:
        verbose_name_plural = "Открывают аварии"


class AbstractEvent(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    start_datetime = models.DateTimeField(blank=True, null=True)
    end_datetime = models.DateTimeField(blank=True, null=True)
    engineer = models.ManyToManyField(Engineer)
    publisher = models.ForeignKey(Publisher)
    publication_datetime = models.DateTimeField(blank=True, null=True)
    state = models.ForeignKey(State, related_name="%(app_label)s_%(class)s_related")

    def __unicode__(self):
        return self.title

    class Meta:
        abstract = True


class Step(AbstractEvent):
    class Meta:
        verbose_name_plural = "Этапы"


class Event(AbstractEvent):
    step = models.ManyToManyField(Step, blank=True)

    class Meta:
        verbose_name_plural = "Аварии"


# @receiver(post_save, sender=Event, dispatch_uid="EventSaveDispatch")
# def send_mail(sender, **kwargs):
#         """
#         send_mail(smtp_ip: dict, smtp_port: dict, send_from: dict, send_to: dict,
#                   user: str, login_name: str, reply: str) -> None
#         """
#         try:
#             msg = MIMEMultipart()
#             msg['From'] = SEND_FROM['send_from'][0]
#             msg['Date'] = formatdate(localtime=True)
#
#             if 'instance' in kwargs:
#                 instance = kwargs['instance']
#                 text = instance.title
#                 msg['Subject'] = u'Авария изменена.'
#                 post_id = str(instance.id)
#             elif 'comment' in kwargs:
#                 comment = kwargs['comment']
#                 text = comment.content_object.title + '\n' + comment.comment
#                 msg['Subject'] = u'Добавлен комментарий.'
#                 post_id = str(comment.content_object.id)
#             else:
#                 text = 'Caramba...'
#                 msg['Subject'] = 'Something goes wrong'
#
#             msg['To'] = COMMASPACE.join(SEND_TO['send_to'])
#             msg.attach(MIMEText(text.encode('UTF-8')+'\n\n'+
#                        'http://sokolskiy.masq.lc'+reverse('ams:detail', args=(post_id,))))
#
#             smtp = smtplib.SMTP(SMTP_IP['smtp_ip'][0], int(SMTP_PORT['smtp_port'][0]))
#             smtp.sendmail(SEND_FROM['send_from'][0], SEND_TO['send_to'], msg.as_string())
#         # In python 3.3 it now has ConnectionRefusedError and socket.error is deprecated.
#         except socket_error as serr:
#             if serr.errno != errno.ECONNREFUSED:
#                 raise serr
#             else:
#                 pass
#
# comment_was_posted.connect(send_mail, dispatch_uid='CommentPostDispatch')
