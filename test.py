from githubgpt import GitHubGPT


# Example usage
github_token = 'YOUR_GITHUB_TOKEN'
repo_url = 'https://github.com/username/repository'
prompt = "function add(a, b) {"

github_gpt = GitHubGPT(github_token)
suggestions = github_gpt.generate_suggestions_for_repository(repo_url, prompt)

print("Generated code suggestions:")
for i, suggestion in enumerate(suggestions):
    print(f"Code suggestion {i+1}:")
    print(suggestion)
    print()
