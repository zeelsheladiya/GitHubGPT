from githubgpt import GitHubGPT


# Example usage
repo_url = "https://github.com/jpetzke/AutoGPT-YouTube/tree/master"
github_gpt = GitHubGPT(repo_url)
github_gpt.fetch_code_from_github()
ai_text = github_gpt.generate_ai_text()
print(ai_text)
