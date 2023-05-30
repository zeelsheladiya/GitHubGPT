import os
import requests
import torch
from github import Github
from transformers import GPT2LMHeadModel, GPT2Tokenizer


class GitHubGPT:
    def __init__(self, github_token):
        self.github_token = github_token
        self.model_name = 'gpt2'
        self.model = GPT2LMHeadModel.from_pretrained(self.model_name)
        self.tokenizer = GPT2Tokenizer.from_pretrained(self.model_name)

    def clone_repository(self, repo_url):
        repo_name = repo_url.split('/')[-1]
        os.system(f'git clone {repo_url}')
        return repo_name

    def get_code_snippets(self, repo_name):
        code_snippets = []
        for root, dirs, files in os.walk(repo_name):
            for file in files:
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    code_snippets.append(f.read())
        return code_snippets

    def generate_code_suggestions(self, prompt, code_snippets):
        suggestions = []
        input_ids = self.tokenizer.encode(prompt, return_tensors='pt')
        for code in code_snippets:
            code_ids = self.tokenizer.encode(code, return_tensors='pt')
            input_ids = input_ids.to(self.model.device)
            code_ids = code_ids.to(self.model.device)
            input_ids = torch.cat([input_ids, code_ids], dim=1)
            output = self.model.generate(input_ids, max_length=100, num_return_sequences=1, temperature=0.8)
            decoded_code = self.tokenizer.decode(output[0], skip_special_tokens=True)
            suggestions.append(decoded_code)
        return suggestions

    def cleanup_repository(self, repo_name):
        os.system(f'rm -rf {repo_name}')

    def generate_suggestions_for_repository(self, repo_url, prompt):
        repo_name = self.clone_repository(repo_url)
        code_snippets = self.get_code_snippets(repo_name)
        suggestions = self.generate_code_suggestions(prompt, code_snippets)
        self.cleanup_repository(repo_name)
        return suggestions
