# -*- coding: utf-8 -*-

import sys

from ckanext.lacounts.model import create_tables, tables_exist
from ckan.plugins import toolkit
import ckanapi


class GetInvolved(toolkit.CkanCommand):
    u'''Utilities for administrating the Get Involved pages (events and volunteering).

    Usage:
        paster get_involved init-db
            Initialize database tables
    '''
    summary = __doc__.split('\n')[0]
    usage = __doc__

    def command(self):
        self._load_config()

        if len(self.args) != 1:
            self.parser.print_usage()
            sys.exit(1)

        cmd = self.args[0]
        if cmd == 'init-db':
            self.init_db()
        else:
            self.parser.print_usage()
            sys.exit(1)

    def init_db(self):

        if tables_exist():
            print(u'Get Involved tables already exist')
            sys.exit(1)

        create_tables()

        print(u'Get Involved tables created')
