from zope.i18nmessageid import MessageFactory
MF = MessageFactory("p2.datashackle.core")

from fanstatic import Library, Resource, Group


# Publish ./resources under localhost/fanstatic/management
management_library = Library('management', 'resources') 


# Define resource instances for inclusion via resource.need()

elastic = Resource(management_library, 'jquery_plugins/elastic/jquery.elastic.js')
jquerytools = Resource(management_library, "jquery_plugins/jquery_tools/jquery.tools.min.js")
xmlDOM = Resource(management_library, "jquery_plugins/xmlDOM.js")
html5_upload = Resource(management_library, "jquery_plugins/html5_upload.js")

jstree_core_js = Resource(management_library, "jquery_plugins/jsTree/jstree.core.js")
jstree_html_js = Resource(management_library, "jquery_plugins/jsTree/jstree.html.js")
jstree_themes_js = Resource(management_library, "jquery_plugins/jsTree/jstree.themes.js")
jstree_vakata_js = Resource(management_library, "jquery_plugins/jsTree/vakata.js")

jsTree = Group([jstree_core_js, jstree_html_js, jstree_themes_js,
    jstree_vakata_js
    ])


p2_js = Resource(management_library, "base/p2.js")
cookies_js = Resource(management_library, "base/cookies.js", depends=[p2_js])
jsonstring_js = Resource(management_library, "base/jsonstring.js")
dom_js = Resource(management_library, "base/dom.js")
multiple_inheritance_js = Resource(management_library, "base/multiple_inheritance.js")


windowmanager_js = Resource(management_library, "windowmanager.js")
window_js = Resource(management_library, "window.js")


# Atm, we can't include it via js.jqueryui, because of the following bug:
# http://dev.jqueryui.com/ticket/4261                                 
# This bug prevents the blur event being triggered when an input is draggable, which leads to outdated data
# in the data graph, because the value's not always updated when the user changes the field value.
# A patch in jquery.ui.mouse.js fixed it.

# We also had once a problem with jquery.ui.dialog.js. Not any more, because we removed the z-index from the widget.
# See also: http://bugs.jqueryui.com/ticket/6267
#
#jqueryui = resource.GroupInclusion([resource.ResourceInclusion(JavascriptLibrary, "jquery-ui-1.8.7.custom/development-bundle/ui/jquery-ui-1.8.7.custom.js"),
#                                   
jquery_ui_core_js = Resource(
    management_library,
    "jquery-ui-1.8.7.custom/development-bundle/ui/jquery.ui.core.js"
    )
jquery_ui_widget_js = Resource(
    management_library,
    "jquery-ui-1.8.7.custom/development-bundle/ui/jquery.ui.widget.js",
    depends=[]
    )
jquery_ui_mouse_js = Resource(
    management_library, 
    "jquery-ui-1.8.7.custom/development-bundle/ui/jquery.ui.mouse.js",
    depends=[jquery_ui_widget_js]
    )
jquery_ui_draggable_js = Resource(
    management_library,
    "jquery-ui-1.8.7.custom/development-bundle/ui/jquery.ui.draggable.js",
    depends=[jquery_ui_widget_js, jquery_ui_core_js, jquery_ui_mouse_js]
    )
jquery_ui_button_js = Resource(management_library, 
    "jquery-ui-1.8.7.custom/development-bundle/ui/jquery.ui.button.js",
    depends=[jquery_ui_core_js, jquery_ui_widget_js]
    )
jquery_ui_droppable_js = Resource(management_library, 
    "jquery-ui-1.8.7.custom/development-bundle/ui/jquery.ui.droppable.js",
    depends=[jquery_ui_widget_js]
    )
jquery_ui_position_js = Resource(management_library, "jquery-ui-1.8.7.custom/development-bundle/ui/jquery.ui.position.js")
#

# jsquey.ui.dialog depends:
# *	jquery.ui.core.js
# *	jquery.ui.widget.js
# *  jquery.ui.button.js
# *	jquery.ui.draggable.js
# *	jquery.ui.mouse.js
# *	jquery.ui.position.js
# *	jquery.ui.resizable.js
#
jquery_ui_dialog_js = Resource(management_library,
    "jquery-ui-1.8.7.custom/development-bundle/ui/jquery.ui.dialog.js",
    depends=[jquery_ui_core_js, jquery_ui_widget_js, jquery_ui_button_js,
        jquery_ui_draggable_js, jquery_ui_droppable_js, jquery_ui_position_js,
        
        ]
    )

# resource.ResourceInclusion(JavascriptLibrary, "jquery-ui-1.8.7.custom/development-bundle/ui/jquery.ui.selectable.js"),
#                                    resource.ResourceInclusion(JavascriptLibrary, "jquery-ui-1.8.7.custom/development-bundle/ui/jquery.effects.highlight.js"),
#                                    ])

jqueryui = Group([jquery_ui_core_js, jquery_ui_dialog_js, jquery_ui_mouse_js,
    jquery_ui_draggable_js, jquery_ui_widget_js, jquery_ui_droppable_js
    ])
 
