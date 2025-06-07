from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Optional, Literal

load_dotenv()

def screenResume(cv):
    class ResumeAnalysis(BaseModel):
        Name: Optional[str]=Field(default=None, description="Write the name of the resume holder")
        Email: Optional[str]=Field(default=None, description="Write the email address of the resume holder")
        Phone_No: Optional[str]=Field(default=None, description="Write the phone number of the resume holder")
        Location: Optional[str]=Field(default=None, description="Write the location/address of the resume holder")
        Degree: Optional[str]=Field(default=None, description="Write the degree mentioned in the resume")
        College_Name: Optional[str]=Field(default=None, description="Write only the college name mentioned with the degree in the resume")
        GPA: Optional[str]=Field(default="0.0", description="Write the CGPA/GPA of the resume holder")
        Graduation_Year: Optional[str]=Field(default=None, description="Write the year of graduation of the resume holder, if mentioned present then write present as output")
        Skills: Optional[str]=Field(default=None, description="Write all the skills and soft skills mantioned in the resume in comma-separated format")
        Certified_Courses: Optional[str]=Field(default=None, description="Write the certified courses mentioned in the resume in comma-separated format")
        Designation: Optional[str]=Field(default=None, description="Write the designations mentioned in the related Work Experience/Experience section in the resume in comma-separated format")
        Companies_Worked: Optional[str]=Field(default=None, description="Write the companies where the resume holder has worked in comma-separated format")
        Years_of_Experience: Optional[str]=Field(default=None, description="Write the total work experience of the resume holder")
        Achievements: Optional[str]=Field(default=None, description="Write all the achievements mentioned in the resume in comma-separated format")
        Awards: Optional[str]=Field(default=None, description="Write all the awards mentioned in the resume in comma-separated format")
        LinkedIn_Profile: Optional[str]=Field(default=None, description="Write the linkedin link provided in the resume")
        GITHUB_Profile: Optional[str]=Field(default=None, description="Write the GITHUB link provided in the resume")
        Projects: Optional[list[str]]=Field(default=None, description="Write all the projects and project descriptions inside a list")
        Layout_Score: float=Field(gt=0, lt=10, description="Score the resume as per the layout, sections, word length and use of professional words at a level of (0-10)")
        Layout_Tips: str=Field(description="Provide the remarks and tips/suggestions to improve the layout of the resume considering its layout, section, word length and use of words")
        Smart_Project_Score: float=Field(GT=0, lt=10, description="Analyzing the skillsets and projects, score the overall projects out of 10 as a company recruiter based on project depth")
        Project_Tips: str=Field(description="Provide the remarks and tips/suggestions on the analysis of the depth of the projects as per skills and also improvements to be made")
        Numerical_Metrics: Literal["Yes", "No"]=Field(description="Check and write in Yes or No if numerical percentages or numerical factors are used in the projects or not")
        Top_Skillset: dict[str, float]=Field(description="Choose top 5 skills from the skills in the resume and based on the projects made on the skills score the skills in the level of 0-100. Make sure to put the skills as keys of the dictionary and scores as values")
        Rate: float=Field(gt=0, lt=10, description="Rate the resume at the level of 0-10 for getting jobs and professionalism.")

    pydantic_parser=PydanticOutputParser(pydantic_object=ResumeAnalysis)

    llm=ChatGoogleGenerativeAI(model="gemini-1.5-flash")

    chat_template=PromptTemplate(
        template='''
        You are an expert Data Analyst and your work is to generate the following entities from the given Resume in string or text format. You have to scrape the data or entities as per the instructions given below.\n
        {format_instructions}
        
        Resume :
        \"\"\"
        {resume}
        \"\"\"
        ''',
        input_variables=["resume"],
        partial_variables={"format_instructions": pydantic_parser.get_format_instructions()}
    )

    chain=chat_template | llm | pydantic_parser

    final_result=chain.invoke({"resume":cv})

    output=dict(final_result)

    print(output)
    return output

