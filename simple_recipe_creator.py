import asyncio
import traceback
from typing import List, Optional

from pydantic import BaseModel

# Import only the base modules
from beeai_framework.backend.chat import ChatModel
from beeai_framework.backend.message import UserMessage
from beeai_framework.memory import UnconstrainedMemory
from beeai_framework.tools.search.duckduckgo import DuckDuckGoSearchTool

class NutritionInfo(BaseModel):
    calories: Optional[int] = None
    protein: Optional[float] = None
    carbs: Optional[float] = None
    fat: Optional[float] = None

async def search_recipes(ingredients: str, llm: ChatModel) -> str:
    """First agent: Search for recipes using the ingredients"""
    try:
        # Create a search tool
        search_tool = DuckDuckGoSearchTool()
        
        # Create a prompt for the recipe finder
        prompt = f"""You are a Recipe Finder assistant specialized in discovering recipes based on available ingredients.

        Your task is to search for recipes that can be made with these ingredients: {ingredients}

        For each recipe you find, verify that it primarily uses the provided ingredients and format it with:
        - Recipe name as a heading
        - Complete list of ingredients with measurements
        - Step-by-step cooking instructions
        - Estimated cooking time
        - Source or inspiration for the recipe
        
        Focus on practical, achievable recipes rather than theoretical combinations.
        
        If a recipe requires additional common ingredients (salt, pepper, oil, etc.), that's acceptable.
        Always explain any substitutions or adaptations you make to the original recipes."""
        
        # Initialize memory and add the user message
        memory = UnconstrainedMemory()
        await memory.add(UserMessage(content=prompt))
        
        # First, search for recipes - using proper dictionary format
        search_query = f"recipes with {ingredients}"
        
        # Properly format the input as a dictionary
        search_input = {"query": search_query}
        
        try:
            # Try to search
            search_results = await search_tool.run(search_input)
            
            # Add search results to memory
            await memory.add(UserMessage(content=f"Here are some search results for recipes with these ingredients:\n\n{search_results}"))
        except Exception as search_error:
            # If search fails, continue without search results
            print(f"Search failed: {search_error}")
            await memory.add(UserMessage(content=f"Unable to search for recipes. Please create recipes using these ingredients: {ingredients}"))
        
        # Now ask the LLM to create recipes
        finder_prompt = f"""Based on your knowledge, create 1-2 detailed recipes using these ingredients: {ingredients}
        
        Make sure each recipe includes:
        1. A clear title
        2. Complete list of ingredients with measurements
        3. Step-by-step instructions
        4. Cooking time
        5. Source information or inspiration
        
        Focus on recipes that primarily use the provided ingredients."""
        
        await memory.add(UserMessage(content=finder_prompt))
        
        # Get response from LLM
        input_dict = {"messages": memory.messages}
        response = await llm.create(input_dict)
        
        # Extract content
        if hasattr(response, 'get_text_content'):
            content = response.get_text_content()
        elif hasattr(response, 'messages') and response.messages:
            content = response.messages[-1].content
        else:
            content = str(response)
        
        return content
        
    except Exception as e:
        error_msg = f"Error in recipe search: {e}"
        traceback.print_exc()
        return error_msg

async def compile_recipes(recipes: str, llm: ChatModel) -> str:
    """Second agent: Format and enhance the recipes"""
    try:
        # Create a prompt for the recipe compiler
        prompt = f"""You are a Recipe Compiler specialized in presenting recipes in a clear, user-friendly format.

        Review and enhance these recipes:

        {recipes}

        Your tasks:
        1. Ensure consistent formatting across all recipes
        2. Add helpful tips and notes where appropriate
        3. Include:
           - A brief introduction for each recipe
           - Any relevant cooking tips or techniques
           - Possible variations or substitutions
           - Serving suggestions
           - Storage recommendations if applicable
        
        Format the final output in a clean, readable structure.
        Maintain all the original recipe details while making them more accessible and user-friendly."""
        
        # Initialize memory and add the user message
        memory = UnconstrainedMemory()
        await memory.add(UserMessage(content=prompt))
        
        # Get response from LLM
        input_dict = {"messages": memory.messages}
        response = await llm.create(input_dict)
        
        # Extract content
        if hasattr(response, 'get_text_content'):
            content = response.get_text_content()
        elif hasattr(response, 'messages') and response.messages:
            content = response.messages[-1].content
        else:
            content = str(response)
        
        return content
        
    except Exception as e:
        error_msg = f"Error in recipe compilation: {e}"
        traceback.print_exc()
        return error_msg

async def generate_simple_recipe(ingredients: str) -> str:
    """Generate recipes using a sequential multi-agent approach"""
    try:
        # Initialize the LLM - using granite3.1 which is already available
        llm = await ChatModel.from_name("ollama:granite3.1-dense:8b")
        
        # Step 1: Search for recipes (first agent)
        print("Step 1: Searching for recipes...")
        recipes = await search_recipes(ingredients, llm)
        
        # Step 2: Compile and enhance recipes (second agent)
        print("Step 2: Compiling and enhancing recipes...")
        final_recipes = await compile_recipes(recipes, llm)
        
        return final_recipes
        
    except Exception as e:
        error_msg = f"An error occurred: {e}"
        traceback.print_exc()
        return error_msg

async def main():
    """Test the recipe generation"""
    print("Recipe Creator with Sequential Multi-Agent System")
    print("===============================================")
    
    try:
        ingredients = input("Enter ingredients (separated by commas): ")
        print("\nGenerating recipes... This may take several minutes.")
        
        # Create progress tracking
        start_time = asyncio.get_event_loop().time()
        
        async def print_progress():
            minute = 1
            while True:
                await asyncio.sleep(60)
                print(f"Still working... ({minute} minute{'s' if minute > 1 else ''} elapsed)")
                minute += 1
        
        # Start progress updates
        progress_task = asyncio.create_task(print_progress())
        
        try:
            # Generate recipes
            result = await generate_simple_recipe(ingredients)
            
            print("\n===== Your Recipe Ideas =====\n")
            print(result)
            
        finally:
            # Clean up progress task
            progress_task.cancel()
            try:
                await progress_task
            except asyncio.CancelledError:
                pass
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main()) 