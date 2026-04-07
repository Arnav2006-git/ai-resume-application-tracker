"""Resume-to-Job matching service"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class ResumeMatcher:
    """Handle resume to job description matching"""
    
    @staticmethod
    def calculate_match_score(resume_text, job_description):
        """Calculate similarity score between resume and job description"""
        try:
            # Create TF-IDF vectors
            vectorizer = TfidfVectorizer(
                max_features=100,
                lowercase=True,
                stop_words='english',
                ngram_range=(1, 2)
            )
            
            # Combine texts for vectorization
            texts = [resume_text, job_description]
            tfidf_matrix = vectorizer.fit_transform(texts)
            
            # Calculate cosine similarity
            semantic_similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            # Extract keywords for keyword-based scoring
            feature_names = vectorizer.get_feature_names_out()
            resume_scores = tfidf_matrix[0].toarray()[0]
            job_scores = tfidf_matrix[1].toarray()[0]
            
            # Get non-zero keywords
            resume_keywords = set(feature_names[i] for i in np.where(resume_scores > 0)[0])
            job_keywords = set(feature_names[i] for i in np.where(job_scores > 0)[0])
            
            # Calculate keyword match ratio
            if len(job_keywords) > 0:
                matched_keywords = len(resume_keywords.intersection(job_keywords))
                keyword_match_ratio = matched_keywords / len(job_keywords)
            else:
                keyword_match_ratio = 0
            
            # Weighted combined score (60% semantic + 40% keyword match)
            combined_score = (semantic_similarity * 0.6) + (keyword_match_ratio * 0.4)
            
            # Convert to percentage (0-100) with slight boost for better user experience
            score = round(min(combined_score * 100, 100), 2)
            return score
        except Exception as e:
            raise Exception(f"Error calculating match score: {str(e)}")
    
    @staticmethod
    def find_matching_keywords(resume_keywords, job_keywords):
        """Find keywords that match between resume and job"""
        resume_set = set(resume_keywords)
        job_set = set(job_keywords)
        matching = list(resume_set.intersection(job_set))
        return sorted(matching)
    
    @staticmethod
    def find_missing_keywords(resume_keywords, job_keywords):
        """Find keywords in job that are missing from resume"""
        resume_set = set(resume_keywords)
        job_set = set(job_keywords)
        missing = list(job_set - resume_set)
        return sorted(missing)
    
    @staticmethod
    def generate_suggestions(resume_keywords, job_keywords, missing_keywords, match_score):
        """Generate improvement suggestions"""
        suggestions = []
        
        # Threshold for improvement suggestions
        if match_score < 50:
            suggestions.append("Consider tailoring your resume more closely to the job description")
        elif match_score < 70:
            suggestions.append("You have a moderate match. Adding more relevant keywords could improve your fit")
        
        if len(missing_keywords) > 0:
            top_missing = missing_keywords[:5]
            suggestions.append(f"Try to include these missing keywords: {', '.join(top_missing)}")
        
        if match_score >= 75:
            suggestions.append("Excellent match! You meet most of the job requirements.")
            suggestions.append("Make sure to highlight your relevant experience in your cover letter.")
        
        return suggestions
    
    @staticmethod
    def get_detailed_analysis(resume_text, resume_keywords, job_text, job_keywords, match_score):
        """Get detailed matching analysis"""
        matching = ResumeMatcher.find_matching_keywords(resume_keywords, job_keywords)
        missing = ResumeMatcher.find_missing_keywords(resume_keywords, job_keywords)
        suggestions = ResumeMatcher.generate_suggestions(resume_keywords, job_keywords, missing, match_score)
        
        analysis = {
            'overall_score': match_score,
            'matching_count': len(matching),
            'missing_count': len(missing),
            'matching_keywords': matching,
            'missing_keywords': missing,
            'suggestions': suggestions,
            'match_percentage': match_score
        }
        
        return analysis
