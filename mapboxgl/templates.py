from jinja2.ext import Extension
from jinja2 import Environment, PackageLoader, StrictUndefined

class SkipBlockExtension(Extension):
    def __init__(self, environment):
        super(SkipBlockExtension, self).__init__(environment)
        environment.extend(skip_blocks=[])

    def filter_stream(self, stream):
        block_level = 0
        skip_level = 0
        in_endblock = False

        for token in stream:
            if (token.type == 'block_begin'):
                if (stream.current.value == 'block'):
                    block_level += 1
                    if (stream.look().value in self.environment.skip_blocks):
                        skip_level = block_level

            if (token.value == 'endblock' ):
                in_endblock = True

            if skip_level == 0:
                yield token

            if (token.type == 'block_end'):
                if in_endblock:
                    in_endblock = False
                    block_level -= 1

                    if skip_level == block_level+1:
                        skip_level = 0

env = Environment(
    loader=PackageLoader('mapboxgl', 'templates'),
    autoescape=False,
    undefined=StrictUndefined,
    extensions=[SkipBlockExtension],
    cache_size=0
)


def format(viz, parent_template, **kwargs):
    print "Currently ", viz
    if kwargs['is_child']:
        print viz, " is a child so remove main blocks"
        env.skip_blocks.append('upper_main_block')
        env.skip_blocks.append('middle_main_block')
        env.skip_blocks.append('lower_main_block')

    print "Now get render template"
    template = env.get_template('{}.html'.format(viz))
    return template.render(viz=viz, parent_template=parent_template, **kwargs)
