from app import app, db
from flask import render_template, redirect, url_for, flash, request, session, json
from app.models import User, Resume
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import SignUpForm, SignInForm, UploadForm
from app.generateEntities import ResumeScreening
from app.resume2text import Pdf2Text
from app.ats_score import ATSScore
from app.job_recommender import JobRecommender
import tempfile
import os

@app.route('/home')
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form=SignUpForm()
    if form.validate_on_submit():
        with app.app_context():
            user_data=User(username=form.username.data,
                           email=form.email_address.data,
                           password=form.password.data)
            
            db.session.add(user_data)
            db.session.commit()
            login_user(user_data)
            
        return redirect(url_for('uploadForm'))
    
    if form.errors!={}:
        for err_msg in form.errors.values():
            print(f"There was an error with creating a user : {err_msg}")

    return render_template('sign_up.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form=SignInForm()
    if form.validate_on_submit():
        attempted_user=User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            return redirect(url_for('dashboard'))
        
        else:
            print(f"Username and Password do not match !!! Please try again")

    return render_template('sign_in.html', form=form)

@app.route('/resume', methods=['GET', 'POST'])
def uploadForm():
    form=UploadForm()
   
    if form.validate_on_submit():
        uploaded_file = request.files['file']
    
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_file_path = tmp_file.name
    
        pdf2txt = Pdf2Text(tmp_file_path)
        text=pdf2txt.createText()
        os.remove(tmp_file_path)
        rs=ResumeScreening()
        output=rs.format_json(text)
        output_dict=rs.format_output(output)
        print(output_dict)
        for key in output_dict:
            if(output_dict[key] is not None and key!="Projects"):
                print(output_dict[key])
                output_dict[key]=output_dict[key].strip('"')
            elif(key!="Projects"):
                output_dict[key]="none"
        if(output_dict['GPA']=="none"):
            output_dict['GPA']='0.0'
        with app.app_context():
            resume_data=Resume(username=form.username.data,
                               name=output_dict['Name'],
                               email=output_dict['Email'],
                               phone_no=output_dict['Phone No.'],
                               location=output_dict['Location'],
                               degree=output_dict['Degree'],
                               cllg_name=output_dict['College Name'],
                               gpa=output_dict['GPA'],
                               grad_year=output_dict['Graduation Year'],
                               skills=output_dict['Skills'],
                               courses=output_dict['Certified Courses'],
                               designation=output_dict['Designation'],
                               companies=output_dict['Companies worked at'],
                               experience=output_dict['Years of Experience'],
                               achievements=output_dict['Achievements'],
                               awards=output_dict['Awards'],
                               linkedin=output_dict['LinkedIn Profile'],
                               github=output_dict['GITHUB Profile'],
                               projects=output_dict['Projects'])
                            
            
            db.session.add(resume_data)
            db.session.commit()
        return redirect(url_for('dashboard'))
    
    return render_template('resume.html', form=form)


@login_required
@app.route('/dashboard')
def dashboard():
    with app.app_context():
        resume_data=Resume.query.filter_by(username=current_user.username).order_by(Resume.id.desc()).first()
    return render_template('dashboard.html', resume_data=resume_data)

@login_required
@app.route('/ats-score')
def ats_score():
    with app.app_context():
       resume_data=Resume.query.filter_by(username=current_user.username).order_by(Resume.id.desc()).first()
       ats=ATSScore(resume_data)
       overall_scores, remarks=ats.generateATSscore()
       print(remarks)
    return render_template('ats.html', overall_scores=overall_scores, remarks=remarks)

@login_required
@app.route('/jrs')
def jrs():
    with app.app_context():
        resume_data=Resume.query.filter_by(username=current_user.username).order_by(Resume.id.desc()).first()
        jr=JobRecommender(resume_data)
        top_jobs=jr.recommend_jobs()
        top_jobs_data=top_jobs.to_dict(orient="records")
        for idx, job in enumerate(top_jobs_data):
            job['id']=idx
        
        
    return render_template('jrs.html', jobs=top_jobs_data)

@login_required
@app.route('/job/<int:job_id>')
def job_details(job_id):
    with app.app_context():
        resume_data=Resume.query.filter_by(username=current_user.username).order_by(Resume.id.desc()).first()
        jr=JobRecommender(resume_data)
        top_jobs=jr.recommend_jobs()
        top_jobs_data=top_jobs.to_dict(orient="records")
        for idx, job in enumerate(top_jobs_data):
            job['id']=idx
        job_found=next((job for job in top_jobs_data if job['id']==job_id), None)

        if job_found is None:
            return "Job not found", 404
        
    return render_template('job_details.html', job=job_found)

