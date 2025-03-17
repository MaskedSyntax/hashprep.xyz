import requests
import json
import time
from collections import defaultdict

# Base API URLs
FILTERS_API_URL = "https://www.naukri.com/code360/api/v3/public_section/all_filters?slug=love-babbar-dsa-sheet-problems&request_differentiator=1742162220255&app_context=publicsection&naukri_request=true"
PROBLEMS_API_URL = "https://www.naukri.com/code360/api/v3/public_section/top_list_questions"

# Headers to mimic a real browser request
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Accept": "application/json"
}

# Step 1: Fetch all available topics
def get_topics():
    response = requests.get(FILTERS_API_URL, headers=HEADERS)
    
    if response.status_code == 200:
        data = response.json()
        practice_topics = data["data"].get("practice_topic[]", {})  # Fixing key name

        # Extract all topic names
        topics = []
        for category, topic_list in practice_topics.items():
            topics.extend(topic_list)
        
        return topics
    else:
        print("Failed to fetch topics. Status code:", response.status_code)
        return []


# Step 2: Fetch problems for each topic
def get_problems_by_topic(topic):
    params = {
        "count": 100, 
        "page": 1, 
        "search": "", 
        "attempt_status": "NOT_ATTEMPTED", 
        "sort_entity": "", 
        "sort_order": "", 
        "slug": "love-babbar-dsa-sheet-problems", 
        "request_differentiator": "1742162114021", 
        "app_context": "publicsection", 
        "naukri_request": "true",
        "practice_topic[]": topic
    }
    
    response = requests.get(PROBLEMS_API_URL, headers=HEADERS, params=params)
    
    if response.status_code == 200:
        return response.json().get("data", {}).get("problem_list", [])
    else:
        print(f"Failed to fetch problems for topic: {topic}. Status code:", response.status_code)
        return []

# Step 3: Aggregate all problems with topics
def map_problems_to_topics():
    topics = get_topics()
    print(topics)
    problem_dict = defaultdict(lambda: {
        "Problem Name": "",
        "Difficulty": "",
        "Platform": "Coding Ninjas",
        "Link": "",
        "Companies": [],
        "Tags": [],
        "Solved Status": 0,
        "Needs Revision": False,
        "Notes": ""
    })
    
    for topic in topics:
        problems = get_problems_by_topic(topic)
        
        for problem in problems:
            problem_id = problem["id"]
            problem_name = problem["name"]
            difficulty = problem["difficulty"]
            problem_link = "https://www.naukri.com/code360/problems/" + problem["slug"]
            company_list = [company["name"] for company in problem["company_list"]]

            # Store data if it's not already present
            if not problem_dict[problem_id]["Problem Name"]:
                problem_dict[problem_id]["Problem Name"] = problem_name
                problem_dict[problem_id]["Difficulty"] = difficulty
                problem_dict[problem_id]["Link"] = problem_link
                problem_dict[problem_id]["Companies"] = company_list
            
            # Add topic to Tags (ensuring unique topics)
            if topic not in problem_dict[problem_id]["Tags"]:
                problem_dict[problem_id]["Tags"].append(topic)
        
        # Sleep to avoid hitting API rate limits
        time.sleep(1)

    return problem_dict

# Run the mapping function
problems_with_topics = map_problems_to_topics()
# print(problems_with_topics)

# Save output to a text file
output_file = "problems_output_v2.txt"

with open(output_file, "w", encoding="utf-8") as file:
    for problem_id, problem_data in problems_with_topics.items():
        file.write(json.dumps(problem_data, indent=4) + "\n\n")

print(f"✅ Output saved to {output_file}")
