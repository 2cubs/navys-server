#!/bin/env python
from lib2cubs.applevelcom.basic import ServerBase

from navys.server.Handler import Handler


if __name__ == '__main__':
	ServerBase.get_instance(handler_class=Handler).start_app()
