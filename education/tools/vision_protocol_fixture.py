"""Decode the model request contract for local protocol fixtures only."""
import json

SCHEMA_MARKER='\nRequired output schema:\n'

def request_envelope(body):
    content=body['messages'][1]['content']
    value=json.loads(content[0]['text'] if isinstance(content,list) else content)
    system=body['messages'][0]['content']
    if SCHEMA_MARKER in system:value={**value,'required_output_schema':json.loads(system.split(SCHEMA_MARKER)[-1])}
    return value
