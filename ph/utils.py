import llama_index
from llama_index.core import PromptTemplate
from llama_index.llms.gemini import Gemini
from llama_index.core.base.llms.types import ChatMessage
from requests.exceptions import HTTPError, ConnectionError, Timeout
from time import time
from typing import List
import os
import logging
from mongoengine.connection import get_db
from datetime import datetime
from dateutil.relativedelta import relativedelta
from ph.config import GOOGLE_API_KEYS, GEMINI_MODEL_NAME, TIMESPAN_DICT


def get_previous_data(duration: str = "this week") -> List[dict]:
    db = get_db()
    collection = db["processed_data"]

    match_stage = {}
    start_date = TIMESPAN_DICT.get(duration)
    match_stage["$expr"] = {
            "$gte": [
                {
                    "$dateFromString":{
                        "dateString": "$date",
                        "format": "%d/%m/%Y",
                        "onError": None,
                        "onNull": None
                    }
                },
                start_date
            ]
        }

    results = list(
        collection.find(match_stage,
                            {"date", "title", "text"})
        .sort("date", -1)
    )
    return results

def switch_google_api_key(current_index: int, first_attempt:bool = False) -> int:
   """
    Switch to the next API key in the list.
    Args:
        current_index (int): The index of the current API key.
        first_attempt (bool): default is False
    Returns:
        int: The new API key index.
    Raises:
        ValueError: If all API keys have been exhausted.
    """
   # move to the next index
   # will be reset to 0 once reached the end
   new_index = (current_index + 1)%len(GOOGLE_API_KEYS)

   if new_index == 0:

      # stopping condition for recursion
      if first_attempt:
        raise ValueError("All API keys are exhausted")

      # go into recursive loop....
      # retries when the new index = 0 but this time first attempt = True
      # this means its a retry
      return switch_google_api_key(new_index, first_attempt = True)
   

def summary_prompt_message(text: List[dict]) -> List[llama_index.core.base.llms.types.ChatMessage]:
    '''
    This function converts the input text & query into chat message template
    Args:
      Input context text & query
    Returns:
      Chat Message template
    '''
    summary_prompt = (
   "You are a development impact writer. Below is a collection of news articles and reports from the past 7 days. "
    "Your task is to write a **concise and impactful weekly summary** that captures the key developments, trends, and events reflected in the context. "
    "The tone should be **engaging, human-centered, and insightful**, highlighting real-world implications and the people affected wherever possible.\n\n"

    "Focus on the 'so what'—why the events matter.\n"
    "Identify any emerging patterns, crises, or shifts.\n"
    "If possible, group related events under thematic umbrellas (e.g. health, climate, displacement).\n"
    "Avoid repetition and do not quote or copy text directly from the context.\n"
    "Keep it original, factual, and coherent.\n\n"

    "------------ CONTEXT ------------\n"
    "{context_str}\n"
    "------------ END CONTEXT ------------\n\n"

    "Begin your weekly case story summary below:"
    )
    prompt = PromptTemplate(summary_prompt)
    prompt_text = prompt.format(context_str=text)
    return [ChatMessage(role="user", content=prompt_text)]


def sitrep_message(text: List[dict]) -> List[llama_index.core.base.llms.types.ChatMessage]:
    '''
    This function converts the input text & query into chat message template
    Args:
      Input context text & query
    Returns:
      Chat Message template
    '''
    situational_report_prompt = (
    "You are a situational analyst tasked with producing a structured weekly **Situational Report** based on the information provided below. "
    "This report should summarize **major events, developments, and emerging issues** from the past 7 days, grouped by relevant sectors or themes "
    "(e.g., health, conflict, climate, migration, food security, governance, etc.).\n\n"

    "Present the facts in a clear, objective, and neutral tone.\n"
    "Use bullet points or brief paragraphs under sector-specific subheadings.\n"
    "Include dates or locations if they are available and important.\n"
    "Highlight significant changes or escalations from the previous week.\n"
    "Avoid speculation; rely only on the context provided.\n\n"

    "------------ CONTEXT ------------\n"
    "{context_str}\n"
    "------------ END CONTEXT ------------\n\n"

    "Begin your Weekly Situational Report below:"
    )
    prompt = PromptTemplate(situational_report_prompt)
    prompt_text = prompt.format(context_str=text)
    return [ChatMessage(role="user", content=prompt_text)]


def risk_assessment_message(text: List[dict]) -> List[llama_index.core.base.llms.types.ChatMessage]:
    '''
    This function converts the input text & query into chat message template
    Args:
      Input context text & query
    Returns:
      Chat Message template
    '''
    risk_assessment_prompt = (
    "You are a crisis and risk analyst. Based on the news and reports from the past 7 days, assess and summarize the **key risks and emerging threats** "
    "that may require monitoring or response in the coming weeks.\n\n"

    "Identify potential health, humanitarian, environmental, or geopolitical risks.\n"
    "Explain what makes them risky—e.g., scale, speed, uncertainty, or potential impact.\n"
    "Flag early warning signals or weak signals that may become critical.\n"
    "Group risks under categories (e.g., Health, Conflict, Climate, Food Insecurity).\n"
    "Be analytical but avoid exaggeration or unsupported claims.\n\n"

    "------------ CONTEXT ------------\n"
    "{context_str}\n"
    "------------ END CONTEXT ------------\n\n"

    "Begin your Weekly Risk Assessment below:"
    )
    prompt = PromptTemplate(risk_assessment_prompt)
    prompt_text = prompt.format(context_str=text)
    return [ChatMessage(role="user", content=prompt_text)]




def generate_reports(text: List[dict], action: str) -> str:
    '''
    This function generates case story
    Args:
      Input text
    Returns:
      case story
    '''
    if action == "summary":
      message = summary_prompt_message(text)
    elif action == "situational report":
        message = sitrep_message(text)
    elif action == "risk assessment":
        message = risk_assessment_message(text)

    current_index = 0
    while True:
        try:
            api_key = GOOGLE_API_KEYS[0]
            llm = Gemini(model = GEMINI_MODEL_NAME, api_key = api_key)
            response = llm.chat(message)
            try:
                return response.message.content.strip()
            except Exception as ex:
                logging.error(f"Error: {ex}")
                return response.text.strip()

        except HTTPError as e:
            if e.response.status_code == 429:
                try:
                    current_index = switch_google_api_key(current_index)
                    time.sleep(2)
                except ValueError:
                    raise ValueError("All API keys are exhausted or invalid.")

            elif e.response.status_code in [501, 502, 503, 504]:
                logging.error(f"Server error {e.response.status_code}: {e.response.text}")
                return  None

            elif e.response.status_code in [401, 401, 403, 404]:
                logging.error(f"Client error {e.response.status_code}: {e.response.text}")
                return  None
            else:
                raise e

        except (ConnectionError, Timeout) as e:
            logging.error(f"Network error: {str(e)}")
            return  None

        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            return  None