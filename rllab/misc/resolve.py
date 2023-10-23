from pydoc import locate
import types
from rllab.misc.ext import iscanr


def classesinmodule(module):
    md = module.__dict__
    return [
        md[c] for c in md if (
            isinstance(md[c], type) and md[c].__module__ == module.__name__
        )
    ]


def locate_with_hint(class_path, prefix_hints=[]):
    module_or_class = locate(class_path)
    if module_or_class is None:
        # for hint in iscanr(lambda x, y: x + "." + y, prefix_hints):
        #     module_or_class = locate(hint + "." + class_path)
        #     if module_or_class:
        #         break
        hint = ".".join(prefix_hints)
        module_or_class = locate(f"{hint}.{class_path}")
    return module_or_class
   

def load_class(class_path, superclass=None, prefix_hints=[]):
    module_or_class = locate_with_hint(class_path, prefix_hints)
    if module_or_class is None:
        raise ValueError(f"Cannot find module or class under path {class_path}")
    if type(module_or_class) == types.ModuleType:
        if superclass:
            classes = [x for x in classesinmodule(module_or_class) if issubclass(x, superclass)]
        if len(classes) == 0:
            if superclass:
                raise ValueError(
                    f'Could not find any subclasses of {str(superclass)} defined in module {class_path}'
                )
            else:
                raise ValueError(f'Could not find any classes defined in module {class_path}')
        elif len(classes) > 1:
            if superclass:
                raise ValueError(
                    f'Multiple subclasses of {str(superclass)} are defined in the module {class_path}'
                )
            else:
                raise ValueError(f'Multiple classes are defined in the module {class_path}')
        else:
            return classes[0]
    elif isinstance(module_or_class, type):
        if superclass is None or issubclass(module_or_class, superclass):
            return module_or_class
        else:
            raise ValueError(
                f'The class {str(module_or_class)} is not a subclass of {str(superclass)}'
            )
    else:
        raise ValueError(f'Unsupported object: {str(module_or_class)}')
