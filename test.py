from githubgpt import GitHubGPT


# Example usage
repo_url = "https://github.com/jpetzke/AutoGPT-YouTube/tree/master"
api_key = "YOUR_OPENAI_API_KEY"
github_gpt = GitHubGPT(repo_url, api_key)
github_gpt.fetch_code_from_github()
ai_text = github_gpt.generate_ai_text()
print(ai_text)
