import requests
import openai


class GitHubGPT:
    def __init__(self, repo_url, api_key):
        self.repo_url = repo_url
        self.code_files = []

        # Set up OpenAI API credentials
        openai.api_key = api_key

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

        # Generate AI text using AutoGPT
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=code,
            max_tokens=100
        )

        # Return the generated AI text
        return response.choices[0].text

