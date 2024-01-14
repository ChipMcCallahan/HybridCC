# __init__.py in instances directory

# __init__.py in instances directory

import pkgutil
import os
import importlib

# Get the current package name
package_name = __name__

# Iterate over all modules in the current directory
for (_, module_name, _) in pkgutil.iter_modules([os.path.dirname(__file__)]):
    # Import the module
    full_module_name = f"{package_name}.{module_name}"
    imported_module = importlib.import_module(full_module_name)

    # Add each class from the module to the package namespace
    # Only add classes that are defined in this module (not imported)
    for attribute_name in dir(imported_module):
        attribute = getattr(imported_module, attribute_name)
        if (isinstance(attribute, type) and
                attribute.__module__ == full_module_name):
            globals()[attribute_name] = attribute
