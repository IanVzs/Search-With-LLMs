import traceback
from loguru import logger

from .prompt import _rag_query_text
from .search_bing import search_bing
from .search_confluence import search_confluence

from demo_data import llm_response

llm_response


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


def search_to_llms(query, should_do_related_questions=False, generate_related_questions=False):
    contexts = search_bing.search(query=query) or []
    contexts_confluence = search_confluence.search(query=query) or []
    system_prompt = _rag_query_text.format(
        context="\n\n".join(
            [f"[[citation:{i+1}]] {c['snippet']}" for i, c in enumerate(contexts_confluence + contexts)]
        )
    )
    # llm_response = llm_response
    try:
        # client = self.local_client()
        # llm_response = client.chat.completions.create(
        #     model=self.model,
        #     messages=[
        #         {"role": "system", "content": system_prompt},
        #         {"role": "user", "content": query},
        #     ],
        #     max_tokens=1024,
        #     stop=stop_words,
        #     stream=True,
        #     temperature=0.9,
        # )
        if should_do_related_questions and generate_related_questions:
            # While the answer is being generated, we can start generating
            # related questions as a future.
            related_questions_future = executor.submit(
                get_related_questions, query, contexts
            )
        else:
            related_questions_future = None
    except Exception as e:
        logger.error(f"encountered error: {e}\n{traceback.format_exc()}")
    return contexts, llm_response
