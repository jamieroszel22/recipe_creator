import pkgutil
import importlib

try:
    # Import the search package
    import beeai_framework.tools.search
    print("Successfully imported search package")
    
    # List all modules in the search package
    print("\nModules in search package:")
    for finder, name, ispkg in pkgutil.iter_modules(beeai_framework.tools.search.__path__, beeai_framework.tools.search.__name__ + '.'):
        print(f"- {name} ({'package' if ispkg else 'module'})")
    
    # Try to import DuckDuckGoSearchTool
    try:
        # Try different possible locations
        locations = [
            "beeai_framework.tools.search.duckduckgo",
            "beeai_framework.tools.search",
            "beeai_framework.tools"
        ]
        
        for location in locations:
            try:
                module = importlib.import_module(location)
                print(f"\nChecking {location}:")
                
                # Check if DuckDuckGoSearchTool is in this module
                if hasattr(module, "DuckDuckGoSearchTool"):
                    print(f"Found DuckDuckGoSearchTool in {location}")
                    break
                else:
                    # List all attributes that might be related
                    search_related = [attr for attr in dir(module) if "search" in attr.lower() or "duck" in attr.lower()]
                    if search_related:
                        print(f"Found search-related attributes: {search_related}")
                    else:
                        print(f"No search-related attributes found in {location}")
            except ImportError:
                print(f"Could not import {location}")
    
    except Exception as e:
        print(f"Error checking for DuckDuckGoSearchTool: {e}")

except ImportError as e:
    print(f"Error importing search package: {e}")
except Exception as e:
    print(f"Unexpected error: {e}") 