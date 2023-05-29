import requests
from transformers import GPT2LMHeadModel, GPT2Tokenizer


class GitHubGPT:
    def __init__(self, repo_url, model_name):
        self.repo_url = repo_url
        self.code_files = []

        # Load the tokenizer and model
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        self.model = GPT2LMHeadModel.from_pretrained(model_name)

    def fetch_code_from_github(self):
        # Extract the repository owner and name from the URL
        owner, repo = self.extract_owner_and_repo()

        # API endpoint to fetch the repository contents
        url = f'https://api.github.com/repos/{owner}/{repo}/contents'

        try:
            response = requests.get(url)
            response.raise_for_status()
            contents = response.json()

            for item in contents:
                # Fetch only files (excluding directories)
                if item['type'] == 'file':
                    file_url = item['download_url']
                    file_content = self.fetch_file_content(file_url)
                    self.code_files.append(file_content)

        except requests.exceptions.RequestException as e:
            print(f"Error occurred while fetching code from GitHub: {e}")

    def extract_owner_and_repo(self):
        # Extract owner and repo name from the GitHub repository URL
        # Modify this function based on the URL pattern you expect
        # Example URL: https://github.com/owner/repo
        parts = self.repo_url.split('/')
        owner = parts[-2]
        repo = parts[-1]
        return owner, repo

    def fetch_file_content(self, file_url):
        try:
            response = requests.get(file_url)
            response.raise_for_status()
            return response.text

        except requests.exceptions.RequestException as e:
            print(f"Error occurred while fetching file content: {e}")
            return ''

    def generate_ai_text(self):
        # Concatenate all code files into a single string
        code = "\n".join(self.code_files)

        # Tokenize the code
        inputs = self.tokenizer.encode(code, return_tensors='pt')

        # Generate AI text using the GPT model
        outputs = self.model.generate(inputs, max_length=100, num_return_sequences=1)
        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Return the generated AI text
        return generated_text

