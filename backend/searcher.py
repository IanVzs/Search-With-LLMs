import traceback
from loguru import logger

from .prompt import _rag_query_text
from .search_bing import search_bing
from .search_confluence import search_confluence
from .llms import chat

from demo_data import llm_response

llm_response

def search_to_llms(query, should_do_related_questions=False, generate_related_questions=False):
    contexts_bing = search_bing.search(query=query) or []
    contexts_confluence = search_confluence.search(query=query) or []
    contexts = contexts_bing + contexts_confluence
    system_prompt = _rag_query_text.format(
        context="\n\n".join(
            [f"[[citation:{i+1}]] {c['snippet']}" for i, c in enumerate(contexts)]
        )
    )
    # llm_response = llm_response
    try:
        llm_response = chat(0, query, system_prompt)
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
