from githubgpt import GitHubGPT


# Usage example
access_token = 'your_github_personal_access_token'
repo_url = 'https://github.com/username/repository_name'

github_gpt = GitHubGPT(access_token, repo_url)
github_gpt.read_files()

question = "What is the main function of this code?"
answer = github_gpt.answer_question(question)
print(answer)
