import os
from openai import OpenAI
from typing import Optional

class LLMClient:
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is not set.")
        self.client = OpenAI(api_key=self.api_key)
        self.model = model

    def generate_commit_message(self, diff: str) -> str:
        """Generate a conventional commit message from a diff."""
        system_prompt = (
            "You are an expert developer. Summarize the following code changes using Conventional Commits (feat, fix, chore, etc.). "
            "Focus on the 'Why', not just the 'What'. "
            "Return only the commit message, no markdown formatting or backticks around the whole message, "
            "but you can use markdown for the body if needed (lists)."
        )
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Diff:\n{diff}"}
            ]
        )
        return response.choices[0].message.content.strip()

    def generate_pr_description(self, diff: str, commit_history: str) -> str:
        """Generate a PR description from diff and commit history."""
        system_prompt = (
            "You are an expert developer. Generate a Pull Request description based on the code changes and commit history. "
            "Include: Summary of Changes, Type of Change (Breaking, Feature, Fix), and a Checklist. "
            "Format as Markdown."
        )
        
        content = f"Commit History:\n{commit_history}\n\nDiff:\n{diff}"
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": content}
            ]
        )
        return response.choices[0].message.content.strip()
