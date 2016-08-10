#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author:Mine DOGAN <mine.dogan@agem.com.tr>

import configparser
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
        self.current_date = datetime.datetime.today().date()

        self.command_logout_user = 'pkill -u {0}'
        self.command_get_users_currently_login = "who | cut -d' ' -f1 | sort | uniq"

        self.logger.debug('[LOGIN-MANAGER] Parameters were initialized.')

    def handle_policy(self):
        try:
            config = configparser.RawConfigParser()
            config.add_section('PERMISSION')

            config.set('PERMISSION', 'days', str(self.days))
            config.set('PERMISSION', 'start_time', str(self.start_time))
            config.set('PERMISSION', 'end_time', str(self.end_time))
            config.set('PERMISSION', 'last_date', str(self.last_date))

            self.create_directory('{0}login-manager/login_files'.format(self.Ahenk.plugins_path()))
            with open('{0}login-manager/login_files/{1}.permissions'.format(self.Ahenk.plugins_path(), self.username), 'w') as configfile:
                config.write(configfile)

            self.logger.debug('[LOGIN-MANAGER] Creating a cron job to check session every minute...')
            self.make_executable('{0}login-manager/scripts/cron.sh'.format(self.Ahenk.plugins_path()))
            self.make_executable('{0}login-manager/scripts/check.py'.format(self.Ahenk.plugins_path()))
            self.execute_script('{0}login-manager/scripts/cron.sh'.format(self.Ahenk.plugins_path()), ['* * * * * /usr/bin/python3 {0}login-manager/scripts/check.py {0}'.format(self.Ahenk.plugins_path())])

            if self.current_date > self.last_date:
                if self.username != None:
                    self.logger.debug(
                        '[LOGIN-MANAGER] Because of the last availability date, session will be terminated for user \'{0}\''.format(
                            self.username))
                    self.execute(self.command_logout_user.format(self.username))
                else:
                    result_code, p_out, p_err = self.execute(self.command_get_users_currently_login)
                    users = []

                    if p_out != None:
                        users = str(p_out).split('\n')
                        users.pop()

                    for user in users:
                        self.logger.debug(
                            '[LOGIN-MANAGER] Because of the last availability date, session will be terminated for user \'{0}\''.format(
                                user))
                        self.execute(self.command_logout_user.format(user))


            self.context.create_response(code=self.message_code.POLICY_PROCESSED.value,
                                             message='Oturum kontrolü başlatıldı.')
            self.logger.info('[LOGIN-MANAGER] Session check has been started.')


        except Exception as e:
            self.logger.error(
                '[LOGIN-MANAGER] A problem occured while handling Login-Manager policy: {0}'.format(str(e)))
            self.context.create_response(code=self.message_code.POLICY_ERROR.value,
                                         message='Login-Manager profili uygulanırken bir hata oluştu.')


def handle_policy(profile_data, context):
    manage = LoginManager(profile_data, context)
    manage.handle_policy()