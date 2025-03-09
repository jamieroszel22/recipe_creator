import pkgutil
import importlib

# Try to import the main package
try:
    import beeai_framework
    print(f"Successfully imported beeai_framework")
    print(f"Package location: {beeai_framework.__file__}")
    
    # List all submodules
    print("\nAvailable submodules:")
    for finder, name, ispkg in pkgutil.iter_modules(beeai_framework.__path__, beeai_framework.__name__ + '.'):
        print(f"- {name} ({'package' if ispkg else 'module'})")
        
        # If it's a package, try to list its contents too
        if ispkg:
            try:
                submodule = importlib.import_module(name)
                for subfinder, subname, subispkg in pkgutil.iter_modules(submodule.__path__, submodule.__name__ + '.'):
                    print(f"  - {subname} ({'package' if subispkg else 'module'})")
            except Exception as e:
                print(f"  Error exploring {name}: {e}")
    
except ImportError as e:
    print(f"Error importing beeai_framework: {e}")
except Exception as e:
    print(f"Unexpected error: {e}") 