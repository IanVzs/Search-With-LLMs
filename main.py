import json
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Generator
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse

app = FastAPI()

app.mount("/ui", StaticFiles(directory="ui", html=True))


def _raw_stream_response(
    contexts, llm_response, related_questions_future
) -> Generator[str, None, None]:
    """
    A generator that yields the raw stream response. You do not need to call
    this directly. Instead, use the stream_and_upload_to_kv which will also
    upload the response to KV.
    """
    # First, yield the contexts.
    yield json.dumps(contexts)
    yield "\n\n__LLM_RESPONSE__\n\n"
    # Second, yield the llm response.
    if not contexts:
        # Prepend a warning to the user
        yield (
            "(The search engine returned nothing for this query. Please take the"
            " answer with a grain of salt.)\n\n"
        )
    for chunk in llm_response:
        if chunk.choices:
            yield chunk.choices[0].delta.content or ""
    # Third, yield the related questions. If any error happens, we will just
    # return an empty list.
    if related_questions_future is not None:
        related_questions = related_questions_future.result()
        try:
            result = json.dumps(related_questions)
        except Exception as e:
            logger.error(f"encountered error: {e}\n{traceback.format_exc()}")
            result = "[]"
        yield "\n\n__RELATED_QUESTIONS__\n\n"
        yield result

def stream_and_upload_to_kv(contexts, llm_response, related_questions_future, search_uuid) -> Generator[str, None, None]:
    """
    Streams the result and uploads to KV.
    """
    # First, stream and yield the results.
    all_yielded_results = []
    for result in _raw_stream_response(
        contexts, llm_response, related_questions_future
    ):
        all_yielded_results.append(result)
        yield result
    # Second, upload to KV. Note that if uploading to KV fails, we will silently
    # ignore it, because we don't want to affect the user experience.
    #_ = self.executor.submit(self.kv.put, search_uuid, "".join(all_yielded_results))

class ParamsQuery(BaseModel):
    query: str
    search_uuid: str
    generate_related_questions: Optional[bool] = True,

@app.post("/query")
def query_function(
    params: ParamsQuery,
) -> StreamingResponse:
    from demo_data import contexts, llm_response, related_questions_future
    contexts = contexts
    llm_response = llm_response
    related_questions_future = related_questions_future
    return StreamingResponse(
        stream_and_upload_to_kv(
            contexts, llm_response, related_questions_future, params.search_uuid
        ),
        media_type="text/html",
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
