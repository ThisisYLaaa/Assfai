import os
import re

if __name__ == '__main__':
    md_files: list[str] = []
    for root, dirs, files in os.walk("english"):
        for file in files:
            if file.endswith('.md'):
                md_files.append(os.path.join(root, file))
    
    pattern = r"# Agent Instructions: Querying This Documentation\n\nIf you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.\n\nPerform an HTTP GET request on the current page URL with the `ask` query parameter:\n\n```\nGET https://adofaieditor\.gitbook\.io/.*?\?ask=<question>\n```\n\nThe question should be specific, self-contained, and written in natural language.\nThe response will contain a direct answer to the question and relevant excerpts and sources from the documentation.\n\nUse this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.\n"
    
    for i in md_files:
        with open(i, 'r', encoding='utf-8') as f:
            content = f.read()
            content = re.sub(pattern, "", content)

        with open(i, 'w', encoding='utf-8') as f:
            f.write(content)


