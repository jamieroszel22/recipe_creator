import inspect

try:
    # Import the agents.types module
    import beeai_framework.agents.types
    print("Successfully imported agents.types module")
    
    # List all attributes in the module
    print("\nAttributes in agents.types module:")
    for attr_name in dir(beeai_framework.agents.types):
        # Skip private attributes
        if attr_name.startswith('_'):
            continue
        
        # Get the attribute
        attr = getattr(beeai_framework.agents.types, attr_name)
        
        # Check if it's a class
        if inspect.isclass(attr):
            print(f"- {attr_name} (class)")
            # List the class attributes
            try:
                class_attrs = [a for a in dir(attr) if not a.startswith('_')]
                if class_attrs:
                    print(f"  Attributes: {', '.join(class_attrs[:5])}{'...' if len(class_attrs) > 5 else ''}")
            except Exception as e:
                print(f"  Error getting attributes: {e}")
        elif inspect.isfunction(attr):
            print(f"- {attr_name} (function)")
        else:
            print(f"- {attr_name} ({type(attr).__name__})")
    
    # Also check agents.base module
    print("\nChecking agents.base module:")
    import beeai_framework.agents.base
    for attr_name in dir(beeai_framework.agents.base):
        # Skip private attributes
        if attr_name.startswith('_'):
            continue
        
        # Get the attribute
        attr = getattr(beeai_framework.agents.base, attr_name)
        
        # Check if it's a class
        if inspect.isclass(attr):
            print(f"- {attr_name} (class)")
            # List the class attributes
            try:
                class_attrs = [a for a in dir(attr) if not a.startswith('_')]
                if class_attrs:
                    print(f"  Attributes: {', '.join(class_attrs[:5])}{'...' if len(class_attrs) > 5 else ''}")
            except Exception as e:
                print(f"  Error getting attributes: {e}")
        elif inspect.isfunction(attr):
            print(f"- {attr_name} (function)")
        else:
            print(f"- {attr_name} ({type(attr).__name__})")
    
except ImportError as e:
    print(f"Error importing module: {e}")
except Exception as e:
    print(f"Unexpected error: {e}") 