import platform
from datetime import datetime
from time import sleep

from lib2cubs.applevelcom.basic import HandlerBase, action


class Handler(HandlerBase):

	def app(self, remote):
		print('Navys Server Handler started')
		for i in range(1, 4):
			sleep(3)
			remote.event_service_status_changed(service='fake-fake.service', status=f'fake-status-{i}')

	@action
	def server_info(self):
		return {
			'uname': platform.uname(),
			'current_time': str(datetime.now())
		}

	@action
	def server_time(self):
		return str(datetime.now())
