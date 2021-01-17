import platform
from datetime import datetime
from time import sleep

from lib2cubs.applevelcom.basic import HandlerBase, action


class Handler(HandlerBase):

	VERSION = '0.3.0'

	# TODO THIS IS DUMMY CODE, It doesn't work yet with systemd and dbus

	list_of_services: dict = None

	def init(self):
		self.prepare_service_list()

	def app(self, remote):
		print('Navys Server Handler started')
		while True:
			sleep(10)
			name = 'ufw.service'
			if self.list_of_services[name]['started']:
				self.on_stop_service(name)
			else:
				self.on_start_service(name)
			sleep(5)
			name = 'upower.service'
			if self.list_of_services[name]['started']:
				self.on_stop_service(name)
			else:
				self.on_start_service(name)

	def prepare_service_list(self):
		self.list_of_services = dict()
		self.list_of_services['paths.target'] = {
			'name': 'paths.target',
			'type': 'target',
			'started': True,
			'enabled': True,
			'description': 'Not a real service. It\'s a dummy simulation.'
		}
		self.list_of_services['remote-fs.target'] = {
			'name': 'remote-fs.target',
			'type': 'target',
			'started': True,
			'enabled': False,
			'description': 'Not a real service. It\'s a dummy simulation.'
		}
		self.list_of_services['sockets.target'] = {
			'name': 'sockets.target',
			'type': 'target',
			'started': False,
			'enabled': False,
			'description': 'Not a real service. It\'s a dummy simulation.'
		}
		self.list_of_services['network-online.target'] = {
			'name': 'network-online.target',
			'type': 'target',
			'started': False,
			'enabled': True,
			'description': 'Not a real service. It\'s a dummy simulation.'
		}
		self.list_of_services['cups.socket'] = {
			'name': 'cups.socket',
			'type': 'socket',
			'started': True,
			'enabled': True,
			'description': 'Not a real service. It\'s a dummy simulation.'
		}
		self.list_of_services['dbus.socket'] = {
			'name': 'dbus.socket',
			'type': 'socket',
			'started': True,
			'enabled': False,
			'description': 'Not a real service. It\'s a dummy simulation.'
		}
		self.list_of_services['syslog.socket'] = {
			'name': 'syslog.socket',
			'type': 'socket',
			'started': False,
			'enabled': True,
			'description': 'Not a real service. It\'s a dummy simulation.'
		}
		self.list_of_services['user-1000.slice'] = {
			'name': 'user-1000.slice',
			'type': 'slice',
			'started': True,
			'enabled': False,
			'description': 'Not a real service. It\'s a dummy simulation.'
		}
		self.list_of_services['wpa_supplicant.service'] = {
			'name': 'wpa_supplicant.service',
			'type': 'service',
			'started': True,
			'enabled': True,
			'description': 'Not a real service. It\'s a dummy simulation.'
		}
		self.list_of_services['upower.service'] = {
			'name': 'upower.service',
			'type': 'service',
			'started': False,
			'enabled': False,
			'description': 'Not a real service. It\'s a dummy simulation.'
		}
		self.list_of_services['ufw.service'] = {
			'name': 'ufw.service',
			'type': 'service',
			'started': False,
			'enabled': False,
			'description': 'Not a real service. It\'s a dummy simulation.'
		}

	def on_start_service(self, service: str):
		print(f'Service {service} started')
		self.list_of_services[service]['started'] = True
		self._remote.event_service_status_changed(service=service, config=self.list_of_services[service])

	def on_stop_service(self, service: str):
		print(f'Service {service} stopped')
		self.list_of_services[service]['started'] = False
		self._remote.event_service_status_changed(service=service, config=self.list_of_services[service])

	def on_enable_service(self, service: str):
		print(f'Service {service} enabled')
		self.list_of_services[service]['enabled'] = True
		self._remote.event_service_status_changed(service=service, config=self.list_of_services[service])

	def on_disable_service(self, service: str):
		print(f'Service {service} disabled')
		self.list_of_services[service]['enabled'] = False
		self._remote.event_service_status_changed(service=service, config=self.list_of_services[service])

	@action
	def server_info(self):
		return {
			'uname': platform.uname(),
			'current_time': str(datetime.now())
		}

	@action
	def server_time(self):
		return str(datetime.now())

	@action
	def services_list(self) -> list:
		return list(self.list_of_services.keys())

	@action
	def service_status(self, services: str or list) -> dict:
		if isinstance(services, str):
			services = [services]
		res = dict()
		los = self.list_of_services
		for item in services:
			res[item] = los[item] if item in los else None
		return res

	@action
	def service_start(self, services: str or list) -> dict:
		if isinstance(services, str):
			services = [services]
		res = dict()
		los = self.list_of_services
		for item in services:
			self.on_start_service(item)
			res[item] = los[item]['started'] if item in los else None
		return res

	@action
	def service_stop(self, services: str or list) -> dict:
		if isinstance(services, str):
			services = [services]
		res = dict()
		los = self.list_of_services
		for item in services:
			self.on_stop_service(item)
			res[item] = los[item]['started'] is False if item in los else None
		return res

	@action
	def service_disable(self, services: str or list) -> dict:
		if isinstance(services, str):
			services = [services]
		res = dict()
		los = self.list_of_services
		for item in services:
			self.on_disable_service(item)
			res[item] = los[item]['enabled'] is False if item in los else None
		return res

	@action
	def service_enable(self, services: str or list) -> dict:
		if isinstance(services, str):
			services = [services]
		res = dict()
		los = self.list_of_services
		for item in services:
			self.on_disable_service(item)
			res[item] = los[item]['enabled'] if item in los else None
		return res

	@action
	def service_config(self, service: str) -> dict or False:
		if service in self.list_of_services:
			return self.list_of_services[service]
		return False
