import llama_index
from pydantic import BaseModel, Field
from llama_index.core.output_parsers import PydanticOutputParser
from llama_index.core.program import LLMTextCompletionProgram
from llama_index.llms.gemini import Gemini
from ph_drf.config import GOOGLE_API_KEYS, GEMINI_MODEL_NAME

class EntityExtraction(BaseModel):
  disease: str = Field(description = "name of disease")
  location: str = Field(description = "geographic location")

def create_prompt_template(text: str) -> str:
    '''
    This function creates the prompt template
    Args:
        text
    Returns:
        text with prompt
    '''
    prompt_template = f'''
    Extract disease and location from the following text in a structured format.
    {text}
    '''
    return prompt_template


def initialize_text_completion_program(llm: llama_index.llms,
                                       prompt_template: str,
                                       output_parser: PydanticOutputParser) -> LLMTextCompletionProgram:
    '''
    This function initializes the text completion program
    Args:
        llm, prompt template, output parser
    Returns:
        llm text completion program
    '''
    program = LLMTextCompletionProgram.from_defaults(
        llm = llm,
        prompt_template_str = prompt_template,
        output_parser = output_parser,
        verbose = True
    )
    return program


def extract_entities(query: str) -> dict:
    '''
    This function extract entities from a given query
    Args:
        query
    Returns:
        entities - disease & location
    '''
    prompt_template = create_prompt_template(query)
    llm = Gemini(model = GEMINI_MODEL_NAME, 
                 api_key = GOOGLE_API_KEYS[0])
    output_parser = PydanticOutputParser(EntityExtraction)
    program = initialize_text_completion_program(llm, prompt_template, output_parser)
    output = program(text = query)
    return output.model_dump()
