from githubgpt import GitHubGPT


repo_url = "https://github.com/owner/repo"
model_name = "gpt2"  # Specify the desired Hugging Face GPT model
github_gpt = GitHubGPT(repo_url, model_name)
github_gpt.fetch_code_from_github()
ai_text = github_gpt.generate_ai_text()
print(ai_text)
