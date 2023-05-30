from githubgpt import GitHubGPT


# Usage example
access_token = 'your_github_personal_access_token'
repo_url = 'https://github.com/username/repository_name'

github_gpt = GitHubGPT(access_token, repo_url)
github_gpt.read_files()

question = "What is the main function of this code?"
answer = github_gpt.generate_response(question)
print(answer)

code_suggestion_prompt = "Create a function that takes a list of numbers and returns the sum of all even numbers."
code_suggestion = github_gpt.generate_response(code_suggestion_prompt, code_suggestion=True)
print(code_suggestion)
