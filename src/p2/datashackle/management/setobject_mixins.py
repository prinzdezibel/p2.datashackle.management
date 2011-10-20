# -*- coding: utf-8 -*-

from cssutils import css



class CssStylesheetAwareness(object):
    def update_css_rules(self, stylesheet, value):
        from p2.datashackle.management.form.form import FormType
        from p2.datashackle.management.widget.widget import WidgetType
        from p2.datashackle.management.span.span import SpanType
        if isinstance(self, WidgetType):
            selector_text = 'div[data-widget-identifier="' + self.id + '"]' 
        elif isinstance(self, SpanType):
            selector_text = 'div[data-span-identifier="' + self.id + '"]'
        elif isinstance(self, FormType):
            selector_text = 'div[data-form-identifier="' + self.id + '"]'
        else:
            raise Error()
        declarations = value.split(';')
        for declaration in declarations:
            colon = declaration.find(':')
            if colon == -1:
                # nothing found
                continue
            css_name = declaration[:colon]
            css_value = declaration[colon + 1:]
            css_property = css.Property(name=css_name, value=css_value)
            found = False
            # Check if selector already exists
            for css_rule in stylesheet.cssRules:
                if not isinstance(css_rule, css.CSSStyleRule):
                    continue
                for selector in css_rule.selectorList:
                    if selector_text == selector.selectorText:
                        found = True
                        #css_rule.style[css_property] = css_value
                        css_rule.style.setProperty(css_property)
            if not found:
                declaration = css.CSSStyleDeclaration()
                declaration.setProperty(css_property)
                #declaration[css_property] = css_value
                css_rule = css.CSSStyleRule(
                    selectorText=selector_text,
                    style=declaration
                )
                stylesheet.add(css_rule)

