"""
GitHub Trending Analyzer - Data Collection Script

This script:
1. Crawls GitHub trending page to get top 5 projects
2. Fetches README files for each project
3. Saves the collected data to a JSON file
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re


def get_trending_repos():
    """Get top 5 trending repositories from GitHub"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    url = 'https://github.com/trending'
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch trending page: {response.status_code}")
    
    soup = BeautifulSoup(response.text, 'html.parser')
    repo_list = []
    
    # Find all repository items
    repo_items = soup.select('div.Box article.Box-row')
    print(f"Found {len(repo_items)} repository items")
    
    for i, item in enumerate(repo_items[:5]):  # Top 5 repos
        try:
            # Debug: print raw item
            print(f"Processing item {i}: {item.get_text()[:100]}...")
            
            # Extract repository name - trying different selectors
            repo_name_elem = item.select_one('h2 a') or item.select_one('h1.h3 a') or item.select_one('.h3 a')
            if not repo_name_elem:
                print(f"Could not find repo name element in item {i}")
                continue
                
            repo_name = repo_name_elem.get_text(strip=True).replace('\n', '').replace('  ', ' ').strip()
            
            # Extract repository URL
            if repo_name_elem.get('href'):
                repo_url = 'https://github.com' + repo_name_elem['href']
            else:
                # Try to find the URL differently
                link_elem = item.select_one('h2 a, h1.h3 a, .h3 a')
                if link_elem and link_elem.get('href'):
                    repo_url = 'https://github.com' + link_elem['href']
                else:
                    print(f"Could not find repo URL in item {i}")
                    continue
            
            # Extract description
            desc_elem = item.select_one('p.color-fg-muted') or item.select_one('p')
            description = desc_elem.get_text(strip=True) if desc_elem else "No description"
            
            # Extract language
            lang_elem = item.select_one('span[itemprop="programmingLanguage"]') or item.select_one('span:has(svg)')
            language = lang_elem.get_text(strip=True) if lang_elem else "Not specified"
            
            # Extract stars count
            # Look for the link that contains stargazers
            stars_elem = item.select_one('a[href*="/stargazers"]') or item.select_one('a[href*="stargazers"]')
            stars = 0
            if stars_elem:
                stars_text = stars_elem.get_text(strip=True)
                # Clean and extract number from string like "1,234" or "1.2k"
                stars_cleaned = re.sub(r'[,.]', '', stars_text)
                # Handle abbreviations like "1.2k" -> "1200"
                if 'k' in stars_cleaned.lower():
                    multiplier = 1000
                    stars_cleaned = stars_cleaned.lower().replace('k', '')
                    stars = int(float(stars_cleaned) * multiplier)
                elif 'm' in stars_cleaned.lower():
                    multiplier = 1000000
                    stars_cleaned = stars_cleaned.lower().replace('m', '')
                    stars = int(float(stars_cleaned) * multiplier)
                else:
                    stars = int(stars_cleaned)
            else:
                print(f"No stars element found for item {i}")
            
            # Extract today's stars
            # Find elements that might contain "stars today" information
            today_stars = 0
            all_spans = item.find_all('span')
            for span in all_spans:
                span_text = span.get_text(strip=True)
                if 'stars today' in span_text.lower():
                    today_stars_match = re.search(r'(\d+(?:[,.]\d+)?)\s+stars today', span_text, re.IGNORECASE)
                    if today_stars_match:
                        today_stars = int(re.sub(r'[,.]', '', today_stars_match.group(1)))
                    break
            
            print(f"Successfully extracted: {repo_name} - {description}")
            
            repo_info = {
                'rank': i + 1,
                'name': repo_name,
                'url': repo_url,
                'description': description,
                'language': language,
                'stars': stars,
                'today_stars': today_stars,
                'readme_content': ''
            }
            
            repo_list.append(repo_info)
            
        except Exception as e:
            print(f"Error processing repository item {i}: {str(e)}")
            import traceback
            traceback.print_exc()
            continue
    
    print(f"Collected {len(repo_list)} repositories")
    return repo_list


def get_repo_readme(repo_url):
    """Fetch the README content for a repository"""
    # Try common branch names
    branches = ['main', 'master', 'develop', 'trunk']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    for branch in branches:
        readme_url = f"{repo_url}/raw/{branch}/README.md"
        response = requests.get(readme_url, headers=headers)
        if response.status_code == 200:
            return response.text
    
    # If raw URL doesn't work, try the HTML page and extract content
    for branch in branches:
        readme_url = f"{repo_url}/{branch}/README.md"
        response = requests.get(readme_url, headers=headers)
        if response.status_code == 200:
            # Try to extract the actual README content from the HTML page
            soup = BeautifulSoup(response.text, 'html.parser')
            readme_elem = soup.find('article', {'class': 'markdown-body'})
            if readme_elem:
                return readme_elem.get_text()
                
    print(f"Could not find README for {repo_url}")
    return "README file not found"


def main():
    """Main function to collect data and save to JSON"""
    print("Fetching trending repositories...")
    repos = get_trending_repos()
    
    print("Fetching README files...")
    for repo in repos:
        print(f"Processing {repo['name']}...")
        repo['readme_content'] = get_repo_readme(repo['url'])
        time.sleep(1)  # Be respectful to GitHub's servers
    
    # Prepare summary data
    summary_data = {
        'collection_time': time.strftime('%Y-%m-%d %H:%M:%S'),
        'repositories': []
    }
    
    for repo in repos:
        # Extract key information from README (first 500 chars for summary)
        readme_preview = repo['readme_content'][:500] + "..." if len(repo['readme_content']) > 500 else repo['readme_content']
        
        summary_data['repositories'].append({
            'rank': repo['rank'],
            'name': repo['name'],
            'url': repo['url'],
            'description': repo['description'],
            'language': repo['language'],
            'stars': repo['stars'],
            'today_stars': repo['today_stars'],
            'readme_preview': readme_preview
        })
    
    # Save to JSON file
    filename = f"github_trending_summary_{time.strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
    
    print(f"Data saved to {filename}")
    return summary_data


if __name__ == "__main__":
    main()