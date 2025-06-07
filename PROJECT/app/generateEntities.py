import os
from dotenv import load_dotenv
import google.generativeai as genai
import re
import string
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


class ResumeScreening():
    def __init__(self):
        self.input=input

    def generateChat(self, input):
        prompt='''
            You are an expert Data Analyst and your work is to generate the following entities
            from the given Resume in string or text format. You have to scrape the data or entities
            in the given format :
            {
                "Name" : <name>,
                "Email" : <email>,
                "Phone No." : <phone no.>,
                "Location" : <location>,
                "Degree" : <degree>,
                "College Name" : <college name>,
                "GPA" : <gpa>,
                "Graduation Year" : <graduation year>,
                "Skills" : <skills>,
                "Certified Courses Done" : <certified courses done>,
                "Designation" : <designation>,
                "Companies worked at" : <companies worked at>,
                "Years of Experience" : <years of experience>,
                "Projects" : [{<project1>:<short description of project1>},{<project2>:<short description of project2>,{....}]
                "LinkedIn Profile" : <linkedin link>,
                "GITHUB Profile" : <github link>,
                "Achievements" : <achievements>,
                "Awards" : <awards>
            }
            Dont provide space or quotes after '[' and '{' in projects.
            1. If there is any Designation, just put it without square braces, otherwise set it to null.
            2. If there is any Companies worked at, just put it without square braces, otherwise set it to null.
            3. If any of the entity is missing the value of the key parameter must be set to null.
            4. Add the https and www protocols to each links provided as input. Don't change your output style each time and 
               follow a fixed output syntax. 
            5. If there is no Certified Courses Done, just make it null.
            6. If there are no projects make it null and ignore the newline (\\n) from the prompt and the response must be free from it.
            7. Provide the entire project-1 in one quote and the next quote in other quote.
            7. Dont generate anything except these.
            '''
        model=genai.GenerativeModel("gemini-1.5-flash")
        response=model.generate_content([prompt, input])
        return response.text
    
    def format_json(self, input):
        output=self.generateChat(input)
        cleaned_output=output.strip('```json\n')
        return cleaned_output
    
    def format_output(self, output):
        output_dict={}

        patterns={
            "Name": r'"Name": (null|".*?")',
            "Email": r'"Email": (null|".*?")',
            "Phone No.": r'"Phone No.": (null|".*?")',
            "Location": r'"Location": (null|".*?")',
            "Degree": r'"Degree": (null|".*?")',
            "College Name": r'"College Name": (null|".*?")',
            "GPA": r'"GPA": (null|".*?")',
            "Graduation Year": r'"Graduation Year": (null|".*?")',
            "Skills": r'"Skills": (null|".*?")',
            "Certified Courses": r'"Certified Courses Done": (null|".*?)',
            "Designation": r'"Designation": (null|".*?")',
            "Companies worked at": r'"Companies worked at": (null|".*?")',
            "Years of Experience": r'"Years of Experience": (null|".*?")',
            "Achievements": r'"Achievements": (null|".*?")',
            "Awards": r'"Awards": (null|".*?")',
            "LinkedIn Profile": r'"LinkedIn Profile": (null|".*?")',
            "GITHUB Profile": r'"GITHUB Profile": (null|".*?")',
            "Projects": r'"Projects": (null|\[.*?\])'
        }
        for key, pattern in patterns.items():
            match=re.search(pattern, output)
            if match:
                if match.group(1)=="null":
                    output_dict[key]=None
                else:
                    if key=="Projects":
                        output_dict[key] = eval(match.group(1))
                    else:
                        output_dict[key]=match.group(1)
        
        return output_dict
    
    