import asyncio
import traceback
from typing import List, Optional

from pydantic import BaseModel, ValidationError

from beeai_framework.agents.types import BeeAgentExecutionConfig
from beeai_framework.backend.chat import ChatModel
from beeai_framework.backend.message import UserMessage
from beeai_framework.memory import UnconstrainedMemory
from beeai_framework.tools.search.duckduckgo import DuckDuckGoSearchTool
from beeai_framework.workflows.agent import AgentFactoryInput, AgentWorkflow
from beeai_framework.workflows.workflow import WorkflowError


class NutritionInfo(BaseModel):
    calories: Optional[int] = None
    protein: Optional[float] = None
    carbs: Optional[float] = None
    fat: Optional[float] = None


async def create_recipe_workflow(llm: ChatModel) -> AgentWorkflow:
    """Create a multi-agent workflow for recipe generation"""
    # Create the workflow
    workflow = AgentWorkflow(name="Recipe Creator")
    
    # 1. Recipe Finder Agent - Searches for recipes and formats them
    workflow.add_agent(
        agent=AgentFactoryInput(
            name="RecipeFinder",
            instructions="""You are a Recipe Finder assistant specialized in discovering recipes based on available ingredients.

            Your tasks:
            1. Search for recipes that can be made with the provided ingredients
            2. For each recipe found, verify that it primarily uses the provided ingredients
            3. Format each recipe with:
               - Recipe name as a heading
               - Complete list of ingredients with measurements
               - Step-by-step cooking instructions
               - Estimated cooking time
               - Source or inspiration for the recipe
            
            Use the DuckDuckGo search tool to find real recipes and adapt them to the available ingredients.
            Focus on practical, achievable recipes rather than theoretical combinations.
            
            If a recipe requires additional common ingredients (salt, pepper, oil, etc.), that's acceptable.
            Always explain any substitutions or adaptations you make to the original recipes.""",
            tools=[DuckDuckGoSearchTool()],
            llm=llm,
            execution=BeeAgentExecutionConfig(
                max_iterations=3,
                timeout_seconds=300  # 5 minutes per agent
            ),
        )
    )
    
    # 2. Recipe Compiler Agent - Formats and enhances the recipes
    workflow.add_agent(
        agent=AgentFactoryInput(
            name="Compiler",
            instructions="""You are a Recipe Compiler specialized in presenting recipes in a clear, user-friendly format.

            Your tasks:
            1. Review and enhance the recipes provided by the RecipeFinder
            2. Ensure consistent formatting across all recipes
            3. Add helpful tips and notes where appropriate
            4. Include:
               - A brief introduction for each recipe
               - Any relevant cooking tips or techniques
               - Possible variations or substitutions
               - Serving suggestions
               - Storage recommendations if applicable
            
            Format the final output in a clean, readable structure using markdown-style formatting.
            Maintain all the original recipe details while making them more accessible and user-friendly.""",
            llm=llm,
            execution=BeeAgentExecutionConfig(
                max_iterations=1,
                timeout_seconds=180  # 3 minutes for compilation
            ),
        )
    )
    
    return workflow


async def generate_recipes(ingredients: str) -> str:
    """Generate recipes using the multi-agent workflow"""
    try:
        # Initialize the LLM with Granite 3.2
        llm = await ChatModel.from_name("ollama:granite3.2-dense:8b")
        
        # Create the workflow
        workflow = await create_recipe_workflow(llm)
        
        # Format the prompt
        prompt = f"""Create detailed recipes using these ingredients: {ingredients}

        Please ensure the recipes:
        1. Primarily use the provided ingredients
        2. Include complete measurements and instructions
        3. Provide cooking times and tips
        4. Include source information or inspiration
        
        Focus on practical, achievable recipes."""
        
        # Initialize memory and add the user message
        memory = UnconstrainedMemory()
        await memory.add(UserMessage(content=prompt))
        
        # Run the workflow with a timeout
        response = await asyncio.wait_for(
            workflow.run(messages=memory.messages),
            timeout=600  # 10 minute total timeout
        )
        
        return response.state.final_answer
        
    except asyncio.TimeoutError:
        return "The recipe generation took too long. Please try again with fewer ingredients."
    except WorkflowError as e:
        error_msg = f"An error occurred in the workflow: {str(e)}"
        traceback.print_exc()
        return error_msg
    except ValidationError as e:
        error_msg = f"A validation error occurred: {str(e)}"
        traceback.print_exc()
        return error_msg
    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        traceback.print_exc()
        return error_msg


async def main():
    """Test the recipe generation workflow"""
    print("Recipe Creator with Multi-Agent System")
    print("=====================================")
    
    try:
        ingredients = input("Enter ingredients (separated by commas): ")
        print("\nGenerating recipes... This may take several minutes.")
        print("Step 1: RecipeFinder is searching for and adapting recipes...")
        
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
            result = await generate_recipes(ingredients)
            
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