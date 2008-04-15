
"""A block tag that changes any links within it pointing to the current page into non-links with class=current."""

from django import template

register = template.Library()

@register.tag()
def navfixup(parser, token):
    nodelist = parser.parse(("endnavfixup",))
    parser.delete_first_token()
    return NavFixup(nodelist)

class NavFixup(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist
    def render(self, context):
        output = self.nodelist.render(context)
        position = 0
        while True:
            start = output[position:].find('href=')
            if start == -1:
                break
            start += position + 6
            end = output[start:].find('>')
            if end == -1:
                break
            end += start
            url = output[start:end].strip("'\" ")
            if url == context["request"].path or (url == "/" and context["request"].path == ""):
                output = output[:start-7] + ' class="current" ' + output[end:]
            position = start
        return output

