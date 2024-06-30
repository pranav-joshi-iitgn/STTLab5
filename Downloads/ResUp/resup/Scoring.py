from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .Preprocessor import *
from .Skill_preprocessor import *

skill_weightage = 0.4
tech_weightage = 0.4
sim_weightage = 0.2

skills_reward = 8
tech_reward = 8
skills_penalty = 2
tech_penalty = 2
subskills_reward = 2
subtech_reward = 2
subskills_penalty = 2
subtech_penalty = 2

def score(Candidate_resume_path, candidate_CGPA, candidate_Working_exp, candidate_Branch, candidate_education, jd, skills, technologies, CGPA_Req, Working_exp, Branch_req, education_req):
    # Preprocess the job description
    jd_processed_ls = preprocess_text_lemma_stem(jd)
    jd_processed_l = preprocess_text_lemma(jd)
    # Preprocess the skills and technologies
    preprocessed_skills = preprocess_skills(skills)
    preprocessed_technologies = preprocess_skills(technologies)
    if candidate_CGPA < CGPA_Req:
        return ("Candidate does not meet the CGPA requirement")
    elif candidate_Working_exp < Working_exp:
        return ("Candidate does not meet the Working Experience requirement")
    elif candidate_Branch not in Branch_req:
        return ("Candidate does not meet the Branch requirement")
    elif candidate_education not in education_req:
        return ("Candidate does not meet the Education requirement")
    else:
        # Extract text from the resume
        candidate_resume = extract_text(Candidate_resume_path, "pdf")
        # print("aws" in candidate_resume)
        candidate_resume_processed_ls = preprocess_text_lemma_stem(candidate_resume)
        # print("aws" in candidate_resume_processed_ls)
        candidate_resume_processed_l = preprocess_text_lemma(candidate_resume)
        # print("aws" in candidate_resume_processed_l)

        skillscore = 0
        total_skills = 0
        absent_skills = []
        # Check if the candidate has the required skills
        for skill in preprocessed_skills:
            skillpresent = False
            for subskill in skill:
                total_skills += skills_reward
                if subskill in candidate_resume_processed_l:
                    skillpresent = True
                    skillscore += subskills_reward
                else:
                    skillscore -= subskills_penalty
            if not skillpresent:
                absent_skills.append(skill)
            else:
                skillscore += skills_reward

        techscore = 0
        total_tech = 0
        absent_tech = []
        # Check if the candidate has the required technologies
        for technology in preprocessed_technologies:
            techpresent = False
            for subtech in technology:
                total_tech += tech_reward
                if subtech in candidate_resume_processed_l:
                    techpresent = True
                    techscore += subtech_reward
                else:
                    techscore -= subtech_penalty
            if not techpresent:
                absent_tech.append(technology)
            else:
                techscore += tech_reward

        text_l = [jd_processed_l, candidate_resume_processed_l]
        # text_ls = [jd_processed_ls, candidate_resume_processed_ls]

        # Calculate the similarity between the job description and the resume
        cv = CountVectorizer()
        count_matrix = cv.fit_transform(text_l)
        sim = cosine_similarity(count_matrix)
        sim_score = sim[0][1]

        # Calculate the final score
        final_score = (skill_weightage * (skillscore / total_skills)) + (tech_weightage * (techscore / total_tech)) + (
                    sim_weightage * sim_score)

        return final_score, absent_skills, absent_tech, skillscore, techscore, sim_score

