### Flow
# 1. Import neccessary libraries
# 2. Define the model using OpenAIModel
# 3. Define the agent using the model
# 4. Define the system prompt for the agent
# 5. Update result_sync to use the chainlit agent
###

#1. Import neccessary libraries
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
import chainlit as cl #newly added from main.py 
import httpx

#2. Define the model using OpenAIModel
model = OpenAIModel(
    'google/gemini-2.0-flash-lite-001',
    provider=OpenAIProvider(
        base_url='https://openrouter.ai/api/v1',
        #api_key=os.getenv('OPENROUTER_API_KEY'),
        api_key='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',
        http_client=httpx.AsyncClient(verify=False)
    ),
)

#3 & 4. Define agent with system prompt
smalltalk_agent = Agent(
    model=model,
    # 'Be concise, reply with one sentence.' is enough for some models (like openai) to use
    # the below tools appropriately, but others like anthropic and gemini require a bit more direction.
    system_prompt=(
        'You are a helpful assistant. '
        'Please answer in traditional Chinese.'
    ),
)

simpleweather_agent = Agent(
    model=model,
    # 'Be concise, reply with one sentence.' is enough for some models (like openai) to use
    # the below tools appropriately, but others like anthropic and gemini require a bit more direction.
    system_prompt=(
        'You are a helpful weather agent. Please answer in traditional Chinese.'
    ),    
)

#5. Update result_sync to use the chainlit agent
@cl.on_message
async def on_message(message: cl.Message):
    user_input = message.content
    
    # Simple keyword detection for weather-related queries
    if any(keyword in user_input.lower() for keyword in ["weather", "temperature", "forecast", "天氣", "溫度", "預報"]):
        result = simpleweather_agent.run_sync(user_input)
    else:
        result = smalltalk_agent.run_sync(user_input)
    
    # Send the response back through Chainlit
    await cl.Message(content=result.output).send()


###result_sync = simpleweather_agent.run_sync('whats your name?') #What is the capital of Italy
### print(result_sync.output) 