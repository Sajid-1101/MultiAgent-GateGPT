# pyrefly: ignore [missing-import]
from google import genai

# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

import os



load_dotenv()


client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

import time
import logging

logger = logging.getLogger("GeminiLLM")

def generate_content_with_retry(model: str, contents, config=None, max_retries=4, initial_delay=3.0):
    """
    Wraps client.models.generate_content with exponential backoff and smart parsing on 429 errors.
    """
    delay = initial_delay
    for attempt in range(max_retries + 1):
        try:
            return client.models.generate_content(
                model=model,
                contents=contents,
                config=config
            )
        except Exception as e:
            err_str = str(e)
            if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str or "quota" in err_str.lower() or "limit" in err_str.lower():
                if attempt < max_retries:
                    sleep_time = delay
                    import re
                    match = re.search(r"retry in ([\d\.]+)", err_str)
                    if match:
                        try:
                            sleep_time = float(match.group(1)) + 1.0
                            logger.info(f"Parsed retry time of {sleep_time:.2f} seconds from Gemini error.")
                        except ValueError:
                            pass
                    logger.warning(f"Gemini API 429 Rate Limit hit. Retrying in {sleep_time:.2f} seconds... (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(sleep_time)
                    delay *= 2
                    continue
            raise e





def ask_gemini(context, question):


   prompt = f"""

You are an intelligent and friendly GATE Computer Science Engineering (CSE) preparation assistant.

Your role is to help students understand Computer Science concepts clearly using the provided study material.

Instructions:
*DO not talk about the provided context, like u dont have this context, you are just a GATE CSE assistant, you have knowledge of all the topics but you will only answer based on the provided context, if the context does not have much information then you can answer based on your general knowledge but you will not mention that the provided material has limited information about that topic*
1. Use the given context as your primary source of information.
2. Explain concepts in a simple, structured, and student-friendly manner.
3. If required, break complex topics into:
   - Definition
   - Explanation
   - Important points
   - Examples
   - GATE exam perspective

4. Do not simply copy the context. Understand it and explain it clearly.

5. If the question is related to Computer Science, GATE preparation, programming, mathematics, or engineering topics:
   - Answer using the provided context.
   - If the context has limited information, explain using your general Computer Science knowledge but mention that the provided material has limited details.

6. If the user asks a question unrelated to GATE, Computer Science, academics, or career guidance:
   - Politely tell them that you are designed as a GATE CSE preparation assistant.
   - Do not provide unrelated answers.
   - Guide them back toward GATE preparation or Computer Science learning.

7. If the user greets you or has a normal conversation:
   - Respond politely and naturally.
   - Introduce yourself as a GATE CSE assistant if appropriate.

8. Avoid hallucinating:
   - Do not invent facts, formulas, or previous year questions.
   - If information is unavailable, clearly say so.

9. Keep answers:
   - Clear
   - Accurate
   - Beginner-friendly
   - Exam-focused

Context:
{context}


Student Question:
{question}


Provide the best possible response:

"""


   try:
      response = generate_content_with_retry(
        model="gemini-2.5-flash",
        contents=prompt
      )

      return response.text

   except Exception as e:
      if "429" in str(e):
        return "Daily AI usage limit reached. Please try again later."

      return "AI service temporarily unavailable."

