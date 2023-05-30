import base64
from github import Github
from transformers import GPT2LMHeadModel, GPT2Tokenizer

class GitHubGPT:
    def __init__(self, access_token, repo_url, model_name='gpt2'):
        self.access_token = access_token
        self.repo_url = repo_url
        self.owner, self.repo_name = self._extract_repo_info()
        self.github = Github(self.access_token)
        self.repo = self._get_repo()
        self.file_contents = []

        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        self.model = GPT2LMHeadModel.from_pretrained(model_name)

    def _extract_repo_info(self):
        repo_info = self.repo_url.split('/')[-2:]
        return repo_info[0], repo_info[1]

    def _get_repo(self):
        return self.github.get_user(self.owner).get_repo(self.repo_name)

    def read_files(self, contents=None):
        if contents is None:
            contents = self.repo.get_contents('')

        for content in contents:
            if content.type == 'dir':
                self.read_files(self.repo.get_contents(content.path))
            else:
                file_content = base64.b64decode(content.content).decode('utf-8')
                self.file_contents.append(file_content)

    def generate_response(self, prompt, max_length=100, code_suggestion=False):
        if code_suggestion:
            prompt = f"Generate code suggestion for the following:\n{prompt}\n\n"
        else:
            prompt = f"{prompt}\n\n"

        for file_content in self.file_contents:
            prompt += f"File content:\n{file_content}\n\n"

        input_ids = self.tokenizer.encode(prompt, return_tensors='pt')
        output = self.model.generate(input_ids, max_length=max_length, num_return_sequences=1)
        response = self.tokenizer.decode(output[0], skip_special_tokens=True).strip()

        return response