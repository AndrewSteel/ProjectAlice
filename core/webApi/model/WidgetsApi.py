#  Copyright (c) 2021
#
#  This file, WidgetsApi.py, is part of Project Alice.
#
#  Project Alice is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>
#
#  Last modified: 2021.04.13 at 12:56:49 CEST

from flask import jsonify, request, send_from_directory
from flask_classful import route

from core.util.Decorators import ApiAuthenticated
from core.webApi.model.Api import Api


class WidgetsApi(Api):
	route_base = f'/api/{Api.version()}/widgets/'


	def __init__(self):
		super().__init__()


	@route('/', methods=['GET'])
	def getWidgets(self):
		try:
			widgets = {widget.id: widget.toDict(self.UserManager.apiTokenValid(request.headers.get('auth', ''))) for widget in self.WidgetManager.widgets.values()}
			return jsonify(success=True, widgets=widgets)

		except Exception as e:
			self.logError(f'Failed retrieving widget instances: {e}')
			return jsonify(success=False, message=str(e))


	@route('/', methods=['PUT'])
	@ApiAuthenticated
	def addWidget(self):
		try:
			skillName = request.json['skillName']
			widgetName = request.json['widgetName']
			pageId = request.json['pageId']
			widget = self.WidgetManager.addWidget(skillName, widgetName, pageId)
			if not widget:
				raise Exception

			return jsonify(success=True, widget=widget.toDict(isAuth=True))
		except Exception as e:
			self.logError(f'Failed adding widget instance: {e}')
			return jsonify(success=False, message=str(e))


	@route('/resources/<skillName>/<widgetName>.js/', methods=['GET'])
	def getJS(self, skillName: str, widgetName: str):
		try:
			return send_from_directory(f'{self.Commons.rootDir()}/skills/{skillName}/widgets/js', f'{widgetName}.js')
		except Exception as e:
			self.logError(f'Error fetching widget JS resource {e}')
			return jsonify(success=False, message=str(e))


	@route('/resources/<skillName>/<widgetName>.css', methods=['GET'])
	def getCSS(self, skillName: str, widgetName: str):
		try:
			return send_from_directory(f'{self.Commons.rootDir()}/skills/{skillName}/widgets/css', f'{widgetName}.css')
		except Exception as e:
			self.logError(f'Error fetching widget CSS resource {e}')
			return jsonify(success=False, message=str(e))


	@route('/resources/img/<skillName>/<image>', methods=['GET'])
	def getImage(self, skillName: str, image: str):
		try:
			return send_from_directory(f'{self.Commons.rootDir()}/skills/{skillName}/widgets/img', f'{image}')
		except Exception as e:
			self.logError(f'Error fetching widget image resource {e}')
			return jsonify(success=False, message=str(e))


	@route('/<widgetId>/', methods=['DELETE'])
	@ApiAuthenticated
	def removeWidget(self, widgetId: str):
		try:
			self.WidgetManager.removeWidget(int(widgetId))
			return jsonify(success=True)
		except Exception as e:
			self.logError(f'Failed removing widget: {e}')
			return jsonify(success=False, message=str(e))


	@route('/pages/', methods=['GET'])
	def getPages(self):
		try:
			return jsonify(success=True, pages={page.id: page.toDict() for page in self.WidgetManager.pages.values()})
		except Exception as e:
			self.logError(f'Failed retrieving widget pages: {e}')
			return jsonify(success=False, message=str(e))


	@route('/pages/<pageId>/', methods=['DELETE'])
	@ApiAuthenticated
	def removePage(self, pageId: str):
		try:
			if int(pageId) == 0:
				raise Exception

			self.WidgetManager.removePage(int(pageId))
			pages = {page.id: page.toDict() for page in self.WidgetManager.pages.values()}
			return jsonify(success=True, pages=pages)
		except Exception as e:
			self.logError(f'Failed removing widget page: {e}')
			return jsonify(success=False, message=str(e))


	@route('/pages/<pageId>/', methods=['PATCH'])
	@ApiAuthenticated
	def updatePageIcon(self, pageId: str):
		try:
			self.WidgetManager.updatePageIcon(int(pageId), request.json['newIcon'])
			return jsonify(success=True)
		except Exception as e:
			self.logError(f'Failed saving widget page icon: {e}')
			return jsonify(success=False, message=str(e))


	@route('/templates/')
	def getTemplates(self):
		try:
			return jsonify(success=True, widgets=self.WidgetManager.widgetTemplates)
		except Exception as e:
			self.logError(f'Failed retrieving widget templates: {e}')
			return jsonify(success=False, message=str(e))


	@route('/addPage/', methods=['PUT'])
	@ApiAuthenticated
	def put(self):
		try:
			page = self.WidgetManager.addPage()
			if not page:
				raise Exception

			return jsonify(success=True, newpage=page.toDict())
		except Exception as e:
			self.logError(f'Failed adding new widget page: {e}')
			return jsonify(success=False, message=str(e))


	@route('/<widgetId>/savePosition/', methods=['PATCH'])
	@ApiAuthenticated
	def savePosition(self, widgetId: str):
		try:
			return jsonify(success=self.WidgetManager.saveWidgetPosition(int(widgetId), request.json['x'], request.json['y']))
		except Exception as e:
			self.logError(f'Failed saving widget position: {e}')
			return jsonify(success=False, message=str(e))


	@route('/<widgetId>/saveSize/', methods=['PATCH'])
	@ApiAuthenticated
	def saveSize(self, widgetId: str):
		try:
			return jsonify(success=self.WidgetManager.saveWidgetSize(int(widgetId), request.json['x'], request.json['y'], request.json['w'], request.json['h']))
		except Exception as e:
			self.logError(f'Failed saving widget size: {e}')
			return jsonify(success=False, message=str(e))


	@route('/<widgetId>/', methods=['PATCH'])
	@ApiAuthenticated
	def saveSettings(self, widgetId: str):
		try:
			self.WidgetManager.saveWidgetSettings(int(widgetId), request.json['settings'])
			self.WidgetManager.saveWidgetConfigs(int(widgetId), request.json['configs'])
			return jsonify(success=True)
		except Exception as e:
			self.logError(f'Failed saving widget settings: {e}')
			return jsonify(success=False, message=str(e))


	@route('/<widgetId>/function/<function>/', methods=['POST'])
	@ApiAuthenticated
	def widgetApiCall(self, widgetId: str, function: str):
		try:
			widget = self.WidgetManager.getWidgetInstance(int(widgetId))
			if not widget:
				raise Exception(f'Widget instance with id **{widgetId}** not found')

			func = getattr(widget, function)
			data = func(**request.json)

			return jsonify(success=True, data=data)
		except Exception as e:
			self.logError(f'Failed widget API call: {e}')
			return jsonify(success=False, message=str(e))
