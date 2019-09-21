from flask import Flask

from core.base.model.Manager import Manager
from core.commons import commons
from core.interface.views.IndexView import IndexView
from core.interface.views.ModulesView import ModulesView


class WebInterfaceManager(Manager):

	NAME = 'WebInterfaceManager'
	app = Flask(__name__)

	def __init__(self):
		super().__init__(self.NAME)


	def onStart(self):
		super().onStart()
		if not self.ConfigManager.getAliceConfigByName('webInterfaceActive'):
			self._logger.info('[{}] Web interface is disabled by settings'.format(self.name))
		else:
			IndexView.register(self.app)
			ModulesView.register(self.app)

			self.ThreadManager.newThread(
				name='WebInterface',
				target=self.app.run,
				kwargs={
					'debug': True,
					'port': self.ConfigManager.getAliceConfigByName('webInterfacePort'),
					'host': commons.getLocalIp(),
					'use_reloader': False
				}
			)
