import os
import requests
from typing import List
from pydantic import BaseModel

openaiurl = os.environ.get('OPENAI_URL')
openaiapitoken = os.environ.get('OPENAI_API_TOKEN')


class MsgOpenAI(BaseModel):
    role: str
    content: str

class PayloadOpenAI(BaseModel):
    messages: List[MsgOpenAI]
    max_tokens: int
    temperature: float
    top_p: int
    frequency_penalty: int
    presence_penalty: int
    model: str

stop_words = [
    "<|im_end|>",
    "[End]",
    "[end]",
    "\nReferences:\n",
    "\nSources:\n",
    "End.",
]

def chat(chat_id, content, system_prompt):
    payload = PayloadOpenAI(
        messages=[
            MsgOpenAI(role="system", content=system_prompt),
            MsgOpenAI(role="user", content=context)
        ],
        max_tokens = 1024,
        temperature = 0.9,
        top_p = 0.8,
        frequency_penalty = 0,
        presence_penalty = 0,
        model = "gpt-3.5-turbo",
    )
    resp = requests.post(openaiurl, json=payload.json(), headers={"Authorization": f"Bearer {openaiapitoken}", "Content-Type": "application/json"})
    resp_content = resp.json()
    return resp_content

def get_related_questions(self, query, contexts):
    """
    Gets related questions based on the query and context.
    """

    def ask_related_questions(
        questions: Annotated[
            List[str],
            [(
                "question",
                Annotated[
                    str, "related question to the original question and context."
                ],
            )],
        ]
    ):
        """
        ask further questions that are related to the input and output.
        """
        pass

    try:
        response = self.local_client().chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": _more_questions_prompt.format(
                        context="\n\n".join([c["snippet"] for c in contexts])
                    ),
                },
                {
                    "role": "user",
                    "content": query,
                },
            ],
            tools=[{
                "type": "function",
                "function": tool.get_tools_spec(ask_related_questions),
            }],
            max_tokens=512,
        )
        related = response.choices[0].message.tool_calls[0].function.arguments
        if isinstance(related, str):
            related = json.loads(related)
        logger.trace(f"Related questions: {related}")
        return related["questions"][:5]
    except Exception as e:
        # For any exceptions, we will just return an empty list.
        logger.error(
            "encountered error while generating related questions:"
            f" {e}\n{traceback.format_exc()}"
        )
        return []

