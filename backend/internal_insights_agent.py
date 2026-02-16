import logging
import os
import json
from typing import Optional

logger = logging.getLogger(__name__)

try:
    from config import API_CONFIG
except Exception:
    API_CONFIG = {}

class InternalInsightsAgent:
    """Internal Knowledge and Document Analysis Agent

    This agent can optionally call an LLM (OpenAI) to generate a summary.
    If `emitter` is provided to `summarize_docs` the agent will stream tokens
    produced by the LLM through the emitter as incremental events.
    """

    def summarize_docs(self, molecule: str, emitter: Optional[callable] = None):
        """Summarize internal company documents and knowledge base.

        If an `OPENAI_API_KEY` is available in `API_CONFIG` or the environment,
        the agent will call OpenAI Chat Completions API with `stream=true` and
        forward token deltas to `emitter` as they arrive.

        Args:
            molecule: Molecule name
            emitter: Optional callable to receive streaming JSON events
        Returns:
            Summary dict (non-streaming) or a minimal dict when streaming is used.
        """
        try:
            logger.info(f"Internal: Analyzing documents for {molecule}")

            api_key = API_CONFIG.get('OPENAI_API_KEY') if isinstance(API_CONFIG, dict) else None
            api_key = api_key or os.getenv('OPENAI_API_KEY')

            if api_key and emitter:
                # Perform streaming request to OpenAI Chat Completions
                import requests

                url = 'https://api.openai.com/v1/chat/completions'
                headers = {
                    'Authorization': f'Bearer {api_key}',
                    'Content-Type': 'application/json'
                }

                system_prompt = (
                    "You are an internal R&D assistant. Summarize internal documents and "
                    "produce concise key takeaways, strategic implications, and suggested next steps."
                )

                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Summarize internal documents for {molecule}."}
                ]

                payload = {
                    "model": API_CONFIG.get('LLM_MODEL', 'gpt-4o-mini') if isinstance(API_CONFIG, dict) else 'gpt-4o-mini',
                    "messages": messages,
                    "temperature": 0.2,
                    "stream": True
                }

                # Stream response and forward token deltas
                with requests.post(url, headers=headers, json=payload, stream=True, timeout=120) as resp:
                    resp.raise_for_status()
                    for line in resp.iter_lines(decode_unicode=True):
                        if not line:
                            continue
                        # OpenAI streaming lines are like: "data: {json}"
                        try:
                            text = line.lstrip('data:').strip()
                            if text == '[DONE]':
                                break
                            data = json.loads(text)
                            # Extract token delta
                            choices = data.get('choices', [])
                            for ch in choices:
                                delta = ch.get('delta', {})
                                content = delta.get('content')
                                if content:
                                    emitter({"type": "llm_token", "data": content})
                        except json.JSONDecodeError:
                            # ignore malformed lines
                            continue

                # When streaming finishes, emit a done event so master can proceed
                emitter({"type": "llm_done", "message": "LLM streaming complete"})
                # Return a placeholder; final MIT will be built by the master agent
                return {"summary_source": "streamed_llm"}

            # Fallback: no API key or no emitter — return a static summary
            return {
                "key_takeaways": [
                    f"Internal research suggests {molecule} has strong potential in oncology repurposing.",
                    f"Previous internal trials showed promising results in Phase II studies.",
                    f"Patent landscape review indicates freedom to operate in major markets."
                ],
                "strategic_implications": f"High priority molecule for investment and development portfolio expansion",
                "internal_notes": f"Recommended to proceed with Phase III clinical trials planning",
                "documents_analyzed": 45,
                "last_updated": "2024-12-15"
            }

        except Exception as e:
            logger.error(f"Internal: Error summarizing documents: {str(e)}")
            if emitter:
                emitter({"type": "error", "message": str(e)})
            return {}
