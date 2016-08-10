#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author:Mine DOGAN <mine.dogan@agem.com.tr>

from base.plugin.abstract_plugin import AbstractPlugin


class Init(AbstractPlugin):
    def __init__(self, context):
        super(Init, self).__init__()
        self.context = context
        self.logger = self.get_logger()

        self.logger.debug('[LOGIN-MANAGER - init] Parameters were initialized.')

    def handle_init_mode(self):
        self.logger.debug('[LOGIN-MANAGER - init] Removing login-manager cron job if exist...')
        self.execute('crontab -l | sed \'/{0}/d\' | crontab -'.format('login-manager/scripts/check.py'))


def handle_mode(context):
    init = Init(context)
    init.handle_init_mode()