#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author:Mine DOGAN <mine.dogan@agem.com.tr>

import datetime
import json

from base.plugin.abstract_plugin import AbstractPlugin

class LoginManager(AbstractPlugin):
    def __init__(self, data, context):
        super(AbstractPlugin, self).__init__()
        self.data = data
        self.context = context
        self.logger = self.get_logger()
        self.message_code = self.get_message_code()

        self.username = self.context.get('username')

        self.parameters = json.loads(self.data)

        self.days = self.parameters['days']
        self.start_time = self.parameters['start-time']
        self.end_time = self.parameters['end-time']
        self.last_date = datetime.datetime.strptime(str(self.parameters['last-date']), "%d/%m/%Y").date()

        self.arr_start_time = str(self.start_time).split(':')
        self.arr_end_time = str(self.end_time).split(':')

        self.today = datetime.datetime.today().weekday()
        self.current_time = datetime.datetime.today().time()
        self.current_date = datetime.datetime.today().date()

        self.start_minute = int(self.arr_start_time[0]) * 60 + int(self.arr_start_time[1])
        self.end_minute = int(self.arr_end_time[0]) * 60 + int(self.arr_end_time[1])
        self.current_minute = int(self.current_time.hour) * 60 + int(self.current_time.minute)

        self.command_logout_user = 'pkill -u {0}'
        self.command_get_users_currently_login = "who | cut -d' ' -f1 | sort | uniq"

        self.logger.debug('[LOGIN-MANAGER] Parameters were initialized.')

    def handle_policy(self):
        try:
            if self.username != None:
                self.logger.debug('[LOGIN-MANAGER] Writing to user profile...')
                self.write_to_user_profile()
            else:
                self.logger.debug('[LOGIN-MANAGER] Writing to global profile...')
                self.write_to_global_profile()

            self.context.create_response(code=self.message_code.POLICY_PROCESSED.value,
                                         message='Login-Manager profili başarıyla uygulandı.')
            self.logger.info('[LOGIN-MANAGER] Login-Manager policy is handled successfully')

        except Exception as e:
            self.logger.error(
                '[LOGIN-MANAGER] A problem occured while handling Login-Manager policy: {0}'.format(str(e)))
            self.context.create_response(code=self.message_code.POLICY_ERROR.value,
                                         message='Login-Manager profili uygulanırken bir hata oluştu.')

    def write_to_user_profile(self):

        if str(self.today) in self.days:

            if not(self.start_minute < self.current_minute < self.end_minute and self.current_date <= self.last_date):
                self.logger.debug('[LOGIN-MANAGER] User: {0} cannot log in. Session will be terminated.'.format(self.username))
                self.execute(self.command_logout_user.format(self.username))
            else:
                self.logger.debug('[LOGIN-MANAGER] User: {0} can log in.'.format(self.username))

        else:
            self.logger.debug('[LOGIN-MANAGER] User: {0} cannot log in. Session will be terminated.'.format(self.username))
            self.execute(self.command_logout_user.format(self.username))

    def write_to_global_profile(self):

        result_code, p_out, p_err = self.execute(self.command_get_users_currently_login)
        users = []

        if p_out != None:
            users = str(p_out).split('\n')
            users.pop()

        if str(self.today) in self.days:

            if not (self.start_minute < self.current_minute < self.end_minute and self.current_date <= self.last_date):
                self.logger.debug('[LOGIN-MANAGER] All users in this machine cannot log in. Sessions will be terminated.')
                for user in users:
                    self.execute(self.command_logout_user.format(user))
            else:
                self.logger.debug('[LOGIN-MANAGER] Users can log in.')

        else:
            self.logger.debug('[LOGIN-MANAGER] All users in this machine cannot log in. Sessions will be terminated.')
            for user in users:
                self.execute(self.command_logout_user.format(user))


def handle_policy(profile_data, context):
    manage = LoginManager(profile_data, context)
    manage.handle_policy()