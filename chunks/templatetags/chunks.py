from django import template
from django.db import models

register = template.Library()

Chunk = models.get_model('chunks', 'chunk')

def do_get_chunk(parser, token):
    # split_contents() knows not to split quoted strings.
    tokens = token.split_contents()
    if len(tokens) == 2:
        tag_name, key = tokens
        cache_time = 0
    else:
        raise template.TemplateSyntaxError, "%r tag should have 2 arguments" % (tokens[0],)
    # Check to see if the key is properly double/single quoted
    if not (key[0] == key[-1] and key[0] in ('"', "'")):
        raise template.TemplateSyntaxError, "%r tag's argument should be in quotes" % tag_name
    # Send key without quotes
    return ChunkNode(key[1:-1])
    
class ChunkNode(template.Node):
    def __init__(self, key):
       self.key = key
    
    def render(self, context):
        try:
            c = Chunk.objects.get(key=self.key)
            content = c.content
        except Chunk.DoesNotExist:
            content = ''
        return content
        
register.tag('chunk', do_get_chunk)
