from zope.i18nmessageid import MessageFactory
MF = MessageFactory("p2.datashackle.core")

from zope.app.appsetup.product import getProductConfiguration

from fanstatic import Library
config = getProductConfiguration("setmanager")
style_dir = config.get('management_styles')
management_styles_library = Library('management_styles', style_dir)

