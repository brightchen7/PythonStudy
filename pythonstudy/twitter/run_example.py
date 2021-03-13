#!/usr/bin/env python

import sys
sys.path.insert(0, '../..')

from twitter.app import app, create_tables
create_tables()
app.run()
