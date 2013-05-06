# -*- coding: utf-8 -*-
# Copyright(C), projekt-und-partner.com, 2011
# Author: Michael Jenny

import re

from p2.datashackle.core.models.identity import generate_random_identifier


class ScopedMarkup(object):
    #onclick = re.compile("""(<[^>]*((?i)onclick="([^"]*)")[^>]*>)""")

    def __init__(self):
        self.script_id = generate_random_identifier()
        self._snippets = list()

    def script(self, javascript):
        script = '<script type="text/javascript">'
        script += 'try{'
        script += 'eval(%s, ec_%s);' % (self.literal(javascript), self.script_id)
        script += '}catch(ex){debugger; alert(ex.message);}</script>'
        self._snippets.append(script)

    def literal(self, string):
        string = string.replace("\\", "\\\\")
        string = string.replace("'", r"\'")
        string = "'" + string + "'"
        string = string.replace("\n", '')
        return string

    def html(self, markup):
        #for match in self.onclick.finditer(markup):
        #    before = markup[:match.start()]
        #    if len(before) > 0:
        #        before = self._escape(before)
        #        self._snippets.append(before)
        #    self._inject_api2(match)
        #    markup = markup[match.end():]
        if len(markup) == 0:
            return
        self._snippets.append(markup)
        
    #def _inject_api2(self, match):
    #    ## Transform DOM Level 0 events into DOM Level 2 events.
    #    ## This is necessary, because it appears that DOM Level 0 events always execute in
    #    ## global execution context. Having all encapsuled in a javascript module pattern
    #    ## is the primary goal of this injector.
    #    pos = match.group(1).index(match.group(2))
    #    m = '<script type="text/javascript">'
    #    m += 'eval(\'$("' + self._escape(match.group(1)[:pos])
    #    m += self._escape(match.group(1)[pos + len(match.group(2)):])
    #    m += '")'
    #    m += '.click(function(){' + match.group(3) + '})\', ec_%s);' % self.script_id
    #    m += '&lt;\/script&gt;'
    #    self._snippets.append(m)

    def render(self):
        code = ''
        for snippet in self._snippets:
            code += snippet
        code = self.literal(code)
        code = code.replace('</script>', r'<\/script>') # For nested script tags
 
        markup = '<div id="%s">injection point</div>' % self.script_id
        markup += '<script type="text/javascript">'
        markup += '(ec_%s = function(){' % self.script_id
        markup += 'try{'
        markup += '$("#%s").before(%s);' % (self.script_id, code)
        markup += '}catch(ex){debugger; alert(ex.message)}'
        markup += '})();'
        # Remove injection point
        markup += '$("#%s").remove();' % self.script_id 
        markup += '</script>'
        return markup

                
                
