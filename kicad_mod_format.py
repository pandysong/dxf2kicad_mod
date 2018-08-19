''' The format of .kicad_mod is modeled in class

So the data could be constructed by abstract interface and print out via str()
interface according to the file format documented at:

https://www.compuphase.com/electronics/LibraryFileFormats.pdf


The format of kicad_mod is in `s-expressions`
https://en.wikipedia.org/wiki/S-expression
'''

import functools


class Cmd:
    '''
    The .kicad_mod format has some comment pattern
    - it always starts with a command name, it could contains zero of more
    parameters and sub-commands
    - parameters, could be any object which support __str__()
    - sub-commands, the sub-commands has the same form of `Cmd`.
    '''
    INDENT = 4

    def __init__(self, name, *args, children=()):
        '''
        if we have only one child Cmd and there is no other arguments,
        the __init__() could be used by Cmd(AnotherCmd), this will simply the
        object init for this special case and make the code concise.
        '''
        self.name = name
        if len(args) == 1 and isinstance(args[0], Cmd):
            self.args = ()
            self.children = (args[0],)
        else:
            self.args = args
            self.children = children

    def str_with_indent(self, indent_level):
        indent_str = ' '*indent_level*self.INDENT
        if not self.args and not self.children:
            return indent_str + self.name
        else:
            return (indent_str +
                    '({}{}{})'.format(self.name,
                                      ''.join(' '+str(s)
                                              for s in self.args),
                                      ''.join('\n' +
                                              s.str_with_indent(indent_level+1)
                                              for s in self.children)))

    def __str__(self):
        return self.str_with_indent(0)


# convert command string to Cmd creator
_CmdList = ('at',
            'layer',
            'tedit',
            'fp_text',
            'effects',
            'thickness',
            'font',
            'hide',
            'fp_line',
            'fp_circle',
            'fp_arc',
            'fp_poly',
            'fp_curve',
            'pts',
            'xy',
            'start',
            'end',
            'angle',
            'width')
for c in _CmdList:
    exec('{} = functools.partial(Cmd, "{}")'.format(c, c))


class Module(Cmd):
    '''
    A Module is a Cmd with
    - cmd name `module`
    - module name `module_name`
    - fixed command plus user defined sub-commands
    '''
    head = (layer('F.Cu'),
            tedit(0),
            fp_text('reference', 'G***', children=(
                at(0, -4),
                layer('F.SilkS'),
                hide(),
                effects(font(thickness(0.2)))
            )),
            fp_text('value', 'value', children=(
                at(0, 4),
                layer('F.SilkS'),
                hide(),
                effects(font(thickness(0.2)))
            )))

    def __init__(self, module_name, children=()):
        super().__init__('module', module_name,
                         children=self.head+children)
