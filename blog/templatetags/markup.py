from django import template
from django.template.defaultfilters import stringfilter
from django.conf import settings

register = template.Library()


@register.filter(name='markdown')
@stringfilter
def markdown(value, arg=''):
    try:
        import markdown
    except ImportError:
        if settings.DEBUG:
            raise (template.TemplateSyntaxError,
                "Error in {% markdown %} filter: "
                "The markdown library is not installed.")
        else:
            from django.utils.html import escape, linebreaks
            return linebreaks(escape(value))
    else:
        extensions = [] if arg == '' else arg.split(',')
        if len(extensions) > 0 and extensions[0] == 'safe':
            extensions = extensions[1:]
            safe_mode = 'escape'
        else:
            safe_mode = False
        return markdown.markdown(value, extensions=extensions, safe_mode=safe_mode)
