import json
import os
import re
import requests

# Helper functions
def username(repo_url):
    if not repo_url:
        return None
    path = requests.utils.urlparse(repo_url).path
    if path.startswith('/'):
        path = path[1:]
    return path.split('/')[0]

def format_module_name(name):
    name = name.replace('-', ' ')
    return ' '.join(word.capitalize() for word in name.split())

# Main function to generate the markdown table
def generate_modules_table():
    # Load modules from modules.json
    with open('modules.json', 'r', encoding='utf-8') as f:
        modules = json.load(f)

    # Sort modules by the formatted name
    def sort_key(module):
        return module['name'].lower()

    modules.sort(key=sort_key)

    # Build the markdown table
    md_table = "| Module | Stats |\n"
    md_table += "|:---------------------------|:-----------:|\n"

    for module in modules:
        github_url = module['githubUrl']
        user_name = username(github_url)
        profile_url = f"http://github.com/{user_name}"
        repo_name = github_url.split('.com/')[1]
        formatted_name = format_module_name(module['name'])

        md_table += f"| **[{formatted_name} - `{module['name'].lower()}`]({github_url})** <br/> by [{user_name}]({profile_url}) <br/>"
        md_table += f"{module['description']}  <br/>"

        dockerhub_image = module.get('dockerhubImage', '')
        if dockerhub_image:
            md_table += f"Docker Image: **`{dockerhub_image}`**  <br/>"
        md_table += f"| "

        md_table += f"![Github Stars](https://img.shields.io/github/stars/{repo_name}) <br/>"
        if dockerhub_image:
            docker_user = dockerhub_image.split('/')[0]
            docker_repo = dockerhub_image.split('/')[1].split(':')[0]
            md_table += f"![Docker Pulls](https://img.shields.io/docker/pulls/{docker_user}/{docker_repo})"
        md_table += f"|\n"

    return md_table.strip()

# Read the README file and update the markdown content
def update_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    with open(readme_path, 'r', encoding='utf-8') as f:
        readme_content = f.read()

    # Define the marker tags
    start_tag = "<!-- ⛔️ AUTO-GENERATED-CONTENT:START -->"
    end_tag = "<!-- ⛔️ AUTO-GENERATED-CONTENT:END -->"

    # Generate the new content
    new_content = generate_modules_table()

    # Replace the existing content with the new content
    updated_content = re.sub(
        f"{start_tag}.*?{end_tag}",
        f"{start_tag}\n{new_content}\n{end_tag}",
        readme_content,
        flags=re.DOTALL,
    )

    # Write the updated content back to the README file
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    print("Docs updated!")

# Run the update process
if __name__ == "__main__":
    update_readme()