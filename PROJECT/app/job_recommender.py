import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.createTags import CreateTags

class JobRecommender():
    def __init__(self, resume_data):
        self.resume_data=resume_data
        ct=CreateTags(resume_data)
        tags_without_projects=ct.createTagWithoutProjects()
        tags_without_projects=ct.format_tags(tags_without_projects)
        self.tags_without_projects=tags_without_projects

    def recommend_jobs(self):
        df=pd.read_csv('PROJECT\\app\\static\\Formatted_Jobs.csv')
        tags=df['tags'].tolist()
        tags.append(self.tags_without_projects)

        tfidf=TfidfVectorizer(max_features=5000, stop_words='english')
        vector=tfidf.fit_transform(tags)
        cosine_sim=cosine_similarity(vector[-1], vector[:-1])

        df['Similarity Scores']=cosine_sim[0]
        top_jobs=df.sort_values(by='Similarity Scores', ascending=False).head(50)

        return top_jobs
