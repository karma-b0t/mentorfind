import json
from openai import OpenAI
from decouple import config    


OPENAI_API_KEY = config('OPENAI_API_KEY')
assistant_id = config('RESUME_ASSISTANT_ID')
client = OpenAI(api_key=OPENAI_API_KEY)
async def get_mentor_by_cv(path):
    with open(path, 'r', encoding='utf-8') as file:
        text = file.read()
        # print(text)
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": text,
                # Attach the new file to the message.
                # "attachments": [
                #     {"file_id": message_file.id, "tools": [{"type": "file_search"}]}
                # ],
            }
        ]
    )

    # The thread now has a vector store with that file in its tool resources.
    print("thread.tool_resources.file_search", thread.tool_resources.file_search)

    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id, assistant_id=assistant_id
    )

    messages = list(
        client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id)
    )

    message_content = messages[0].content[0].text
    annotations = message_content.annotations
    citations = []
    for index, annotation in enumerate(annotations):
        message_content.value = message_content.value.replace(
            annotation.text, f"[{index}]"
        )
        if file_citation := getattr(annotation, "file_citation", None):
            cited_file = client.files.retrieve(file_citation.file_id)
            citations.append(f"[{index}] {cited_file.filename}")
    
    print("message_content.value", message_content.value)
    print("\n".join(citations))
    return message_content.value

# async def main():
#     await get_ai_text(text=text)

# asyncio.run(main())
if __name__ == '__main__':
    text = "downloads/"
    get_mentor_by_cv(text)