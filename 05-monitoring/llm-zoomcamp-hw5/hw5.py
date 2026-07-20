from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor
from save_db import SQLiteSpanExporter

provider = TracerProvider()
# provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))

provider.add_span_processor(
    SimpleSpanProcessor(SQLiteSpanExporter("traces.db"))
)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer("llm-zoomcamp")


from rag_helper import RAGBase
from starter import rag


class RAGTraced(RAGBase):
    def search(self, query, num_results=5):
        with tracer.start_as_current_span("search") as span:
            span.set_attribute("query", query)
            results = super().search(query, num_results=num_results)
            span.set_attribute("num_results", len(results))
            return results

    def llm(self, prompt):
        with tracer.start_as_current_span("llm") as span:
            span.set_attribute("model", self.model)
            response = super().llm(prompt)
            usage = response.usage
            span.set_attribute("input_tokens", usage.input_tokens)
            span.set_attribute("output_tokens", usage.output_tokens)
            span.set_attribute("total_tokens", usage.total_tokens)
            return response

    def rag(self, query):
        with tracer.start_as_current_span("rag") as span:
            span.set_attribute("query", query)
            return super().rag(query)


traced_rag = RAGTraced(
    index=rag.index,
    llm_client=rag.llm_client,
    instructions=rag.instructions,
    prompt_template=rag.prompt_template,
    model=rag.model,
)

query = "How does the agentic loop keep calling the model until it stops?"
answer = traced_rag.rag(query)
print(answer)
