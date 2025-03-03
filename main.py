# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# import google.generativeai as genai
# import os
# import json

# # Initialize FastAPI app
# app = FastAPI()

# # Set Gemini API key
# GEMINI_API_KEY = "AIzaSyDDwBXcI-crWetGL7pa00-Q3qeefQ2Q3G8"
# genai.configure(api_key=GEMINI_API_KEY)

# # Define request payload model
# class SkillRequest(BaseModel):
#     skill_name: str
#     student_level: str
#     education: str

# # Define route to process skill request
# # @app.post("/generate-skill-roadmap")
# # async def generate_skill_roadmap(request: SkillRequest):
# #     try:
# #         prompt = (
# #             f"Provide a structured step-by-step roadmap to learn {request.skill_name} for a {request.student_level} level student with an education background in {request.education}. "
# #             "The roadmap should include: "
# #             "1. A industry ready outline of key topics to master. "
# #             "2. A further breakdown of each topic into smaller, manageable subtopics. "
# #             "3. Suggested online courses or video tutorials from platforms like YouTube, Coursera, Udemy, or other free/paid resources. "
# #             "Return the response as a structured JSON, where each step includes: "
# #             "- 'step_number' (integer) "
# #             "- 'topic' (string) "
# #             "- 'subtopics' (list of strings) "
# #             "- 'recommended_resources' (list of URLs for learning materials)."
# #         )
        
# #         # Generate response using Gemini
# #         model = genai.GenerativeModel("gemini-1.5-flash")
# #         response = model.generate_content(prompt)
        
# #         return {"roadmap": response.text}
# #     except Exception as e:
# #         raise HTTPException(status_code=500, detail=str(e))

# @app.post("/generate-skill-roadmap")
# async def generate_skill_roadmap(request: SkillRequest):
#     try:
#         prompt = (
#             f"Provide a structured step-by-step roadmap to learn {request.skill_name} for a {request.student_level} level student with an education background in {request.education}. "
#             "The roadmap should include: "
#             "1. A industry ready outline of key topics to master. "
#             "2. A further breakdown of each topic into smaller, manageable subtopics. "
#             "3. Suggested online courses or video tutorials from platforms like YouTube, Coursera, Udemy, or other free/paid resources. "
#             "Return the response as a structured JSON, where each step includes: "
#             "- 'step_number' (integer) "
#             "- 'topic' (string) "
#             "- 'subtopics' (list of strings) "
#             "- 'recommended_resources' (list of URLs for learning materials)."
#         )

#         # Send request to Gemini AI
#         model = genai.GenerativeModel("gemini-1.5-flash")
#         response = model.generate_content(prompt)

#         # Ensure the response is valid JSON
#         roadmap_data = response.text.strip("```json").strip("```")  # Remove Markdown code block markers
#         roadmap_json = json.loads(roadmap_data)  # Convert string to JSON

#         return {"roadmap": roadmap_json}  # Return proper JSON

#     except Exception as e:
#         return {"error": str(e)}

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
import json
import re  # Import regex module

# Initialize FastAPI app
app = FastAPI()

# Set Gemini API key
GEMINI_API_KEY = "AIzaSyDDwBXcI-crWetGL7pa00-Q3qeefQ2Q3G8"
genai.configure(api_key=GEMINI_API_KEY)

# Define request payload model
class SkillRequest(BaseModel):
    skill_name: str
    proficiency: str
    education: str
    available_time_per_week: int

@app.post("/generate-skill-roadmap")
async def generate_skill_roadmap(request: SkillRequest):
    try:
        prompt = (
    f"""Think step by step before generating the response.
      Analyze the learning path carefully and ensure it is well-structured and optimized for a {request.proficiency} level student with an education background in {request.education} and for the available time per week of {request.available_time_per_week}.. 
    Provide a structured step-by-step roadmap to learn {request.skill_name}. 
    
    The roadmap should include:
    1. An industry-ready outline of key topics to master.
    2. A further breakdown of each topic into smaller, manageable subtopics.
    3. Suggested online courses, video tutorials, or resources **for each subtopic** from platforms like YouTube, Coursera, Udemy, or other free/paid sources.

    **Think carefully before responding.** Ensure that the roadmap is practical, realistic, and considers the best possible learning path. If needed, revise the structure to improve clarity and depth.

    Return the response as a structured JSON, where each step includes:
    - 'step_number' (integer)
    - 'topic' (string)
    - 'subtopics' (list of objects, where each object has 'subtopic_name' and 'resources')
    - 'recommended_resources' (list of URLs for overall topic learning)

    Example JSON format:
    {{

        "roadmap": [
            {{
                "step_number": 1,
                "topic": "Python Fundamentals",
                "subtopics": [
                    {{
                        "subtopic_name": "Data Types (int, float, str, etc.)",
                        "resources": ["https://www.w3schools.com/python/", "https://docs.python.org/3/tutorial/"]
                    }},
                    {{
                        "subtopic_name": "Control Flow (if-else, loops)",
                        "resources": ["https://realpython.com/python-conditional-statements/"]
                    }}
                ],
                "recommended_resources": [
                    "https://www.python.org/doc/",
                    "https://www.coursera.org/learn/python-for-everybody"
                ]
            }},
            {{
                "step_number": 2,
                "topic": "FastAPI Basics",
                "subtopics": [
                    {{
                        "subtopic_name": "Introduction to FastAPI",
                        "resources": ["https://fastapi.tiangolo.com/tutorial/"]
                    }},
                    {{
                        "subtopic_name": "Creating API Endpoints",
                        "resources": ["https://fastapi.tiangolo.com/tutorial/first-steps/"]
                    }}
                ],
                "recommended_resources": [
                    "https://fastapi.tiangolo.com/",
                    "https://www.udemy.com/course/fastapi-complete-guide/"
                ]
            }}
        ]
    }}
    
    Just return the JSON response, nothing else. Think deeply before responding and ensure the roadmap is logically structured and well-optimized.
    """
)

        # Generate response using Gemini
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        # Extract text content
        roadmap_data = response.text.strip()

        # 🔹 Use regex to remove Markdown code block (```json ... ```) if present
        roadmap_data = re.sub(r"^```json|```$", "", roadmap_data).strip()

        # 🔹 Try parsing the JSON response safely
        try:
            roadmap_json = json.loads(roadmap_data)
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail="Invalid JSON format received from Gemini AI.")

        return {"roadmap": roadmap_json}  # Return properly formatted JSON

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
