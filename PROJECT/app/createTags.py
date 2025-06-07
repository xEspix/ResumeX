import string
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

class CreateTags():
    def __init__(self, resume_data):
        self.resume_data=resume_data

    def createTagsWithProjects(self):
        if(self.resume_data.projects is not None):
            projects=self.resume_data.projects
            prjcts=""
            for project in projects:
                prjcts+=project
            tags_with_projects=str(self.resume_data.degree)+' '+str(self.resume_data.cllg_name)+' '+str(self.resume_data.skills)+' '+str(self.resume_data.companies)+' '+str(self.resume_data.experience)+' '+prjcts
            return tags_with_projects
    
    def createTagWithoutProjects(self):
        tags_without_projects=str(self.resume_data.degree)+' '+str(self.resume_data.cllg_name)+' '+str(self.resume_data.skills)+' '+str(self.resume_data.companies)+' '+str(self.resume_data.experience)
        return tags_without_projects
    
    def format_tags(self, tags):
        tags=tags.lower()
        for punc in string.punctuation:
            tags=tags.replace(punc, ' ')

        new_tag=""
        for t in tags:
            if new_tag=='' and t!=' ':
                new_tag+=t
            if new_tag!='':
                if not(t==' ' and new_tag[-1]==' '):
                    new_tag+=t

        format_text=""
        for word in new_tag.split():
            if word!='none':
                format_text+=word+' '
        
        stop=stopwords.words('english')
        new_txt=""
        for word in format_text.split():
            if word not in stop:
                new_txt+=word+' '

        return new_txt
    