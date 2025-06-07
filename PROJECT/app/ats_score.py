import re
from app.syntax_check import CheckFormat
from app.createTags import CreateTags

rs=CheckFormat()

class ATSScore():
    def __init__(self, resume_data):
        self.resume_data=resume_data
        ct=CreateTags(self.resume_data)
        self.ct=ct
    def generateATSscore(self):
        #ATS SCORE GENERATOR
        score_obt=0
        personal_details_score=0

        remarks=[]

        #PERSONAL INFO : TOTAL POINTS = 11

        if(self.resume_data.name is not None):
            personal_details_score+=1
        else:
            remarks.append("Ensure that your full name is prominently displayed at the top of the resume for clear identification.")

        if(self.resume_data.phone_no is not None):
            if(rs.is_valid_phone_number_with_cc(self.resume_data.phone_no)):
                personal_details_score+=2
                
            elif(rs.is_valid_phone_number(self.resume_data.phone_no)):
                personal_details_score+=1
                remarks.append("Including the country code with your phone number is essential, especially if applying for international roles.")
        else:
            remarks.append("Ensure the phone number is accurate and functional for quick and easy communication.")
                

        if(self.resume_data.email is not None):
            if(rs.is_valid_email(self.resume_data.email)):
                personal_details_score+=2
        else:
            remarks.append("Include a valid email address that reflects professionalism. Avoid using overly casual or inappropriate email IDs.")
                

        if(self.resume_data.location is not None):
            personal_details_score+=2
        else:
            remarks.append("A location or address is mandatory to give employers an understanding of where you are based, which can be crucial for certain job roles.")
            
        if(self.resume_data.linkedin is not None):
            if(rs.is_valid_linkedin_url(self.resume_data.linkedin)):
                personal_details_score+=2
        else:
            remarks.append("A valid LinkedIn URL demonstrates a well-rounded professional presence online and gives recruiters an additional way to assess your career history.")
                
        if(self.resume_data.github is not None):
            if(rs.is_valid_github_url(self.resume_data.github)):
                personal_details_score+=2
        else:
            remarks.append("If you're a developer or have a portfolio of coding projects, a GitHub URL showcases your work and technical skills.")
            
        print("PERSONAL DETAILS SCORE = ", personal_details_score)
        score_obt+=personal_details_score

        #SKILLS AND COMPETENCIES : TOTAL POINTS = 18

        skill_scores=0

        if(self.resume_data.skills is not None):
            skills=self.resume_data.skills
            skillsets=[]
            for skill in skills.split(', '):
                skillsets.append(skills)

            if(len(skillsets)>=10):
                skill_scores+=10
            else:
                skill_scores+=len(skillsets)
                remarks.append("Adding more skills to the resume reflects the working capabilities of an applicants.")

            soft_skills=[
            "verbal communication", 
            "written communication", 
            "presentation skills", 
            "active listening", 
            "non-verbal communication", 
            "teamwork",
            "collaboration" 
            "empathy", 
            "conflict resolution", 
            "networking", 
            "emotional intelligence", 
            "leadership", 
            "delegation", 
            "mentoring",
            "coaching", 
            "decision-making", 
            "motivating others", 
            "time management", 
            "multitasking", 
            "project management", 
            "adaptability", 
            "attention to detail", 
            "critical thinking", 
            "creativity", 
            "analytical thinking", 
            "resourcefulness", 
            "decision making", 
            "dependability", 
            "accountability", 
            "commitment", 
            "self-motivation", 
            "integrity", 
            "innovative thinking", 
            "brainstorming", 
            "design thinking", 
            "visionary thinking", 
            "willingness to learn", 
            "change management", 
            "open-mindedness", 
            "stress management", 
            "resilience", 
            "customer-centric approach", 
            "problem resolution", 
            "relationship building", 
            "patience", 
            "persuasiveness", 
            "cooperation", 
            "supportiveness", 
            "compromise", 
            "conflict management", 
            "trustworthiness", 
            "self-improvement", 
            "training others", 
            "research skills", 
            "growth mindset", 
            "professional development", 
            "cultural awareness", 
            "inclusion", 
            "global mindset", 
            "sensitivity", 
            "respect"
            ]
            count_softskills=0
            for skill in skillsets:
                if skill in soft_skills:
                    count_softskills+=1

            if count_softskills>=3:
                skill_scores+=5
            elif count_softskills==2:
                skill_scores+=4
            elif count_softskills==1:
                skill_scores+=3
                remarks.append("Adding more soft skills reflects the management and cooperative skills of a job applicant.")
            else:
                remarks.append("Including a diverse range of technical skills and soft skills (e.g., communication, leadership, time management) will enhance your profile, showing your versatility and competence.")
        else:
            remarks.append("A well-organized skills and competencies section helps recruiters quickly identify your expertise areas and suitability for the role.")

        courses=0

        if(self.resume_data.courses is not None):
            for course in self.resume_data.courses:
                courses+=1

        if courses>2:
            skill_scores+=3
        elif courses==2:
            skill_scores+=2
        elif courses==1:
            skill_scores+=1
        else:
            remarks.append("Include certifications from renowned organizations to showcase your commitment to continuous learning and professional development.")

        print("SKILLS AND COMPETANCIES SCORE = ", skill_scores)
        score_obt+=skill_scores

        #EXPERIENCES AND ACHIEVEMENTS : TOTAL POINTS = 18
        desg=self.resume_data.designation
        work_exp=self.resume_data.experience
        count_desg=0
        comp=0
        exp_scores=0

        if(desg is not None):
            for des in desg.split(', '):
                count_desg+=1
            
            if count_desg>=2:
                exp_scores+=5
            elif count_desg==1:
                exp_scores+=3
        else:
            remarks.append("Adding your previous job titles provides clarity about your roles and responsibilities in prior positions.")

        
        if(self.resume_data.companies is not None):
            for work in work_exp.split(', '):
                comp+=1
            
            if comp>=2:
                exp_scores+=5
            elif comp==1:
                exp_scores+=3
        else:
            remarks.append("Listing previous employers highlights your experience in different industries and work environments.")
        if(self.resume_data.achievements is not None):
            count_achv=0
            for achv in (self.resume_data.achievements):
                count_achv+=1

            if count_achv>=3:
                exp_scores+=5
            elif count_achv==2:
                exp_scores+=3
            elif count_achv==1:
                exp_scores+=2
                remarks.append("Achievements in the resume prove the level of success of an applicant. So more achievements means more capabilities and experiences.")
        else:
            remarks.append("Highlighting significant achievements demonstrates your success and ability to add value to your future employer.")
        if self.resume_data.experience!="none":
            exp_scores+=3
        else:
            remarks.append("Clearly stating the duration of your work experience will reflect your expertise in a particular field.")

        print("EXPERIENCES AND ACHIEVEMENTS SCORES = ", exp_scores)
        score_obt+=exp_scores

        #EDUCATION AND CERTIFICATIONS : TOTAL POINTS = 13
        score_edu=0
        map_edu=[1,1,1,1]
        if(self.resume_data.degree is not None):
            score_edu+=5
        else:
            map_edu[0]=0
        
        if(self.resume_data.cllg_name is not None):
            score_edu+=5
        else:
            map_edu[1]=0

        if(self.resume_data.grad_year is not None):
            score_edu+=1
        else:
            map_edu[2]=0

        if(self.resume_data.gpa!="0.0"):
            score_edu+=2
            print(self.resume_data.gpa)
        else:
            map_edu[3]=0

        print("EDUCATION AND CERTIFICATIONS SCORES = ", score_edu)
        score_obt+=score_edu

        edu_remarks=""
        if map_edu[0]==0:
            edu_remarks+="Degree "
        if map_edu[1]==0:
            edu_remarks+="College Name "
        if map_edu[2]==0:
            edu_remarks+="Graduation Year "
        if map_edu[3]==0:
            edu_remarks+="GPA "
        if map_edu.count(0)==1:
            edu_remarks+"is missing in the resume."
            remarks.append(edu_remarks)
        elif map_edu.count(0)>1:
            edu_remarks+="are missing in the resume."
            remarks.append(edu_remarks)
        #ACCOMPLISHMENTS AND PROJECTS : TOTAL POINTS = 12
        score_proj=0
        proj_num=0
        if self.resume_data.projects is not None:
            for project in self.resume_data.projects:
                proj_num+=1
        if proj_num>=3:
            score_proj+=10
        elif proj_num==2:
            score_proj+=7
        elif proj_num==1:
            score_proj+=5
            remarks.append("More projects shows more working efficiencies and capabilities to work on.")
        else:
            remarks.append("Including notable projects can demonstrate practical application of your skills and your ability to work on complex tasks.")

        score_obt+=score_proj

        score_award=0
        if(self.resume_data.awards is not None):
            award_num=0
            for award in (self.resume_data.awards):
                award_num+=1

            if award_num>=3:
                score_award+=2
            elif award_num>=2:
                score_award+=1
        else:
            remarks.append("Adding awards you’ve received demonstrates recognition of your efforts and success in various fields.")

        score_obt+=score_award

        print("ACCOMPLISHMENTS AND PROJECTS SCORES = ", score_proj+score_award)

        #SPECIAL KEYWORDS : Total : 4
        action_verbs = [
        "achieved", "developed", "managed", "led", "implemented", "improved", 
        "collaborated", "designed", "created", "optimized", "analyzed", 
        "coordinated", "reduced", "enhanced", "executed", "resolved", 
        "oversaw", "directed", "supervised", "generated", "exceeded", 
        "partnered", "delivered", "scoped", "produced", "surpassed", 
        "mentored", "identified", "strategized", "provided", "solved", 
        "assisted", "facilitated", "increased", "decreased", "evaluated", 
        "formulated", "established", "initiated", "spearheaded", "monitored", 
        "streamlined", "promoted", "supported", "conducted", "negotiated", "built"
        ]
        tag_score=0
        tags_matched=0
        tags_with_projects=self.ct.createTagsWithProjects()
        formatted_tags=self.ct.format_tags(tags_with_projects)
        for tag in formatted_tags.split():
            if tag in action_verbs:
                tags_matched+=1

        if(tags_matched>=5):
            tag_score+=4
        elif(tags_matched==3 or tags_matched==4):
            tag_score+=3
        elif(tags_matched==2):
            tag_score+=2
        elif(tags_matched==1):
            tag_score+=1
        else:
            remarks.append("Strengthen your resume by using powerful verbs like achieved, developed, managed, led, implemented, improved, collaborated, designed, and created. These words enhance the impact of your contributions.")

        score_obt+=tag_score

        #Layout Score : Total : 10
        layout_score=self.resume_data.layout_score
        remarks.append(self.resume_data.layout_tips)

        score_obt+=layout_score

        #Smart Project Score : Total : 13
        smart_project_score=self.resume_data.smart_project_score
        remarks.append(self.resume_data.project_tips)

        if(self.resume_data.numerical_metrics=="Yes"):
            smart_project_score+=3
        
        score_obt+=smart_project_score

        #AI based Rating: Total : 30
        score_obt=score_obt+(self.resume_data.rate*3)


        
        print("SCORES OBTAINED = ",score_obt)
        print("TOTAL SCORES = 130")

        perc=(score_obt/130)*100
        fresh_perc=((score_obt-exp_scores)/101)*100
        print("YOUR RESUME SCORED = "+str(perc)+"%.")
        print("IF YOU ARE A FRESHER, YOUR RESUME SCORED = "+str(fresh_perc)+"%.")

        overall_scores=[score_obt, score_obt-exp_scores, perc, fresh_perc, personal_details_score, skill_scores, exp_scores, score_edu, score_proj+score_award, tag_score]
        

        for top_skill in self.resume_data.top_skillset:
            print(top_skill+" : ",
                  self.resume_data.top_skillset[top_skill])

        return overall_scores, remarks



