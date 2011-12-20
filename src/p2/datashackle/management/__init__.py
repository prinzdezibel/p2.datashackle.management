from zope.i18nmessageid import MessageFactory
MF = MessageFactory("p2.datashackle.core")

from zope.app.appsetup.product import getProductConfiguration

from fanstatic import Library
config = getProductConfiguration("setmanager")
user_styles_path = config.get('user_styles_path')
user_styles_library = Library('user_styles', user_styles_path)
sys_staticresource_path = config.get('sys_staticresource_path')
sys_staticresource_library = Library('sys_staticresource', sys_staticresource_path)

