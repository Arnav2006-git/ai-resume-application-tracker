"""
Semantic ATS Resume-Job Matching Engine
Performs intelligent semantic analysis for resume-to-job matching with:
- Meaningful hiring signal extraction
- Semantic equivalence detection
- Technical skill relevance scoring
- Gap analysis
"""

import re
from typing import Dict, List, Tuple, Set

class SemanticATSMatcher:
    """Advanced semantic matching engine for ATS systems"""
    
    # Generic words to ignore (low signal value)
    GENERIC_WORDS = {
        'role', 'student', 'preferred', 'based', 'involving', 'building',
        'projects', 'workflows', 'text', 'data', 'systems', 'small',
        'focused', 'team', 'company', 'organization', 'position', 'job',
        'work', 'experience', 'project', 'background', 'skill', 'skills',
        'responsibility', 'ability', 'knowledge', 'understanding', 'strong',
        'excellent', 'good', 'great', 'better', 'best', 'experienced',
        'application', 'applications', 'development', 'dev', 'code', 'coding',
        'support', 'technical', 'requirement', 'requirements', 'required',
        'collaborat', 'communicate', 'creative', 'innovative', 'motivated',
        'seeking', 'looking', 'ideal', 'candidate', 'professional', 'modern',
        'new', 'working', 'worked', 'works', 'help', 'helping', 'manage',
        'manage', 'responsible', 'led', 'lead', 'leading', 'created',
        'create', 'design', 'designed', 'implement', 'implemented',
        'industry', 'field', 'level', 'levels', 'area', 'areas',
        'opportunity', 'opportunities', 'member', 'engineer', 'developer',
        'across', 'various', 'diverse', 'wide', 'range', 'ability',
        'features', 'functionality', 'feature', 'functionality'
    }
    
    # High-value technical keywords that should be prioritized
    HIGH_VALUE_KEYWORDS = {
        'programming_languages': {
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#',
            'go', 'rust', 'ruby', 'php', 'swift', 'kotlin', 'scala',
            'r', 'matlab', 'sql', 'html', 'css', 'bash', 'shell'
        },
        'frameworks_libraries': {
            'react', 'vue', 'angular', 'django', 'flask', 'fastapi',
            'spring', 'spring boot', 'express', 'node.js', 'next.js',
            'nuxt', 'laravel', 'pytorch', 'tensorflow', 'scikit-learn',
            'pandas', 'numpy', 'jquery', 'bootstrap', 'tailwind'
        },
        'platforms_clouds': {
            'aws', 'azure', 'gcp', 'google cloud', 'heroku', 'vercel',
            'netlify', 'docker', 'kubernetes', 'openstack', 'ibm cloud'
        },
        'databases': {
            'postgresql', 'mysql', 'mongodb', 'redis', 'elasticsearch',
            'cassandra', 'dynamodb', 'oracle', 'sqlite', 'firebase',
            'firestore', 'cosmos db', 'sql server'
        },
        'tools_platforms': {
            'git', 'github', 'gitlab', 'jenkins', 'circleci', 'travis',
            'docker', 'kubernetes', 'terraform', 'ansible', 'jira',
            'confluence', 'slack', 'agile', 'scrum', 'rest api', 'graphql',
            'websocket', 'oauth', 'jwt', 'api gateway', 'microservices'
        },
        'methodologies': {
            'agile', 'scrum', 'kanban', 'ci/cd', 'tdd', 'bdd',
            'devops', 'microservices', 'serverless', 'rest', 'graphql'
        },
        'soft_skills': {
            'leadership', 'mentorship', 'problem-solving', 'communication',
            'collaboration', 'time management', 'analytical'
        }
    }
    
    # Semantic equivalence mappings
    SEMANTIC_MAPPINGS = {
        'rest api': {'api endpoint', 'rest endpoint', 'http api', 'rest service'},
        'api endpoint': {'rest api', 'rest endpoint', 'http endpoint', 'endpoint'},
        'browser extension': {'chrome extension', 'firefox extension', 'extension'},
        'client-server': {'client-server architecture', 'client server interaction'},
        'frontend framework': {'react', 'vue', 'angular', 'sitefinity'},
        'backend framework': {'django', 'flask', 'express', 'spring'},
        'file upload': {'file upload support', 'upload', 'multipart form'},
        'pasted text': {'text input', 'text processing', 'text extraction'},
        'content extraction': {'jsoup', 'parsing', 'scraping', 'web scraping'},
        'responsive design': {'mobile responsive', 'mobile-first', 'responsive'},
        'version control': {'git', 'github', 'gitlab', 'bitbucket'},
        'testing': {'unit test', 'integration test', 'e2e', 'testing framework'},
        'database': {'sql', 'nosql', 'postgresql', 'mongodb', 'relational'},
        'authentication': {'oauth', 'jwt', 'saml', 'session management'},
        'deployment': {'ci/cd', 'continuous integration', 'continuous deployment'},
        'containerization': {'docker', 'container', 'orchestration'},
        'scalability': {'load balancing', 'caching', 'distributed', 'horizontal scaling'},
        'real-time': {'websocket', 'socket.io', 'live', 'streaming'},
        'machine learning': {'ml', 'ai', 'neural network', 'deep learning'},
        'full-stack': {'frontend', 'backend', 'fullstack'},
    }
    
    @staticmethod
    def extract_meaningful_terms(text: str) -> Set[str]:
        """Extract high-value technical terms from text"""
        if not text:
            return set()
        
        # Convert to lowercase and remove special characters
        text = text.lower()
        text = re.sub(r'[^\w\s\-./+#]', ' ', text)
        
        # Extract programming languages and tools
        terms = set()
        
        # Multi-word terms first (to avoid partial matches)
        multi_word_patterns = [
            r'(?:machine learning|ml model)',
            r'(?:machine learning|deep learning)',
            r'(?:client[- ]server)',
            r'(?:rest\s+api)',
            r'(?:api\s+endpoint)',
            r'(?:chrome\s+extension|firefox\s+extension)',
            r'(?:ci[/ ]cd)',
            r'(?:file\s+upload|pasted\s+text)',
            r'(?:content\s+extraction)',
            r'(?:responsive\s+design)',
            r'(?:version\s+control)',
            r'(?:unit\s+test|integration\s+test)',
            r'(?:google\s+cloud|gcp)',
            r'(?:spring\s+boot)',
            r'(?:node\.?js|nodejs)',
            r'(?:socket\.io|websocket)',
            r'(?:full[- ]?stack)',
        ]
        
        for pattern in multi_word_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            terms.update(matches)
        
        # Single words and high-value keywords
        words = re.findall(r'\b[\w\-./+#]+\b', text)
        for word in words:
            if len(word) < 2:
                continue
            if word not in SemanticATSMatcher.GENERIC_WORDS:
                terms.add(word)
        
        return terms
    
    @staticmethod
    def find_semantic_matches(resume_terms: Set[str], job_terms: Set[str]) -> List[Dict]:
        """Find semantically equivalent matches between resume and job terms"""
        semantic_matches = []
        matched_resume = set()
        matched_job = set()
        
        # Check all semantic mappings
        for key, equivalents in SemanticATSMatcher.SEMANTIC_MAPPINGS.items():
            all_forms = {key} | equivalents
            
            # Check if any form appears in both resume and job
            resume_matches = resume_terms & all_forms
            job_matches = job_terms & all_forms
            
            if resume_matches and job_matches:
                resume_term = list(resume_matches)[0]
                job_term = list(job_matches)[0]
                
                if resume_term not in matched_resume and job_term not in matched_job:
                    semantic_matches.append({
                        'job_term': job_term,
                        'resume_term': resume_term,
                        'reason': f'Semantic equivalence: {job_term} ≈ {resume_term}'
                    })
                    matched_resume.add(resume_term)
                    matched_job.add(job_term)
        
        return semantic_matches
    
    @staticmethod
    def categorize_match(term: str) -> str:
        """Categorize a term by its type"""
        term_lower = term.lower()
        
        for category, keywords in SemanticATSMatcher.HIGH_VALUE_KEYWORDS.items():
            if any(keyword in term_lower for keyword in keywords):
                return category
        
        return 'general'
    
    @staticmethod
    def calculate_relevance_score(term: str, category: str) -> float:
        """Calculate relevance score for a term"""
        # Programming languages and frameworks are highest priority
        if category in ['programming_languages', 'frameworks_libraries', 'databases']:
            return 1.0
        elif category in ['platforms_clouds', 'tools_platforms', 'methodologies']:
            return 0.85
        elif category == 'soft_skills':
            return 0.6
        else:
            return 0.5
    
    @staticmethod
    def match_resume_and_job(resume_text: str, job_description: str) -> Dict:
        """
        Perform comprehensive semantic ATS matching
        
        Args:
            resume_text: Raw resume text
            job_description: Raw job description text
            
        Returns:
            Detailed matching analysis with score and insights
        """
        if not resume_text or not job_description:
            raise ValueError("Resume text and job description are required")
        
        # Extract meaningful terms
        resume_terms = SemanticATSMatcher.extract_meaningful_terms(resume_text)
        job_terms = SemanticATSMatcher.extract_meaningful_terms(job_description)
        
        # Find direct matches
        direct_matches = list(resume_terms & job_terms)
        
        # Find semantic matches
        semantic_matches = SemanticATSMatcher.find_semantic_matches(resume_terms, job_terms)
        
        # Calculate matches count (including semantic)
        matched_keywords = set(direct_matches)
        for match in semantic_matches:
            matched_keywords.add(match['resume_term'])
        
        # Find missing keywords
        missing_keywords = list(job_terms - resume_terms)
        
        # Remove semantic matches from missing (they were handled above)
        semantic_matched_job_terms = {m['job_term'] for m in semantic_matches}
        missing_keywords = [k for k in missing_keywords if k not in semantic_matched_job_terms]
        
        # Categorize and score
        matched_with_scores = []
        for keyword in matched_keywords:
            category = SemanticATSMatcher.categorize_match(keyword)
            score = SemanticATSMatcher.calculate_relevance_score(keyword, category)
            matched_with_scores.append({'term': keyword, 'score': score, 'category': category})
        
        # Identify strong match areas
        strong_areas = {}
        for match in matched_with_scores:
            category = match['category']
            if category not in strong_areas:
                strong_areas[category] = []
            strong_areas[category].append(match['term'])
        
        strong_match_areas = [
            f"{category}: {', '.join(terms)}"
            for category, terms in sorted(strong_areas.items())
            if category != 'general'
        ]
        
        # Identify gaps
        gaps = []
        critical_keywords = SemanticATSMatcher.HIGH_VALUE_KEYWORDS.get('programming_languages', set())
        critical_keywords.update(SemanticATSMatcher.HIGH_VALUE_KEYWORDS.get('frameworks_libraries', set()))
        critical_keywords.update(SemanticATSMatcher.HIGH_VALUE_KEYWORDS.get('databases', set()))
        
        for keyword in missing_keywords:
            if keyword in critical_keywords:
                gaps.append(f"Missing critical skill: {keyword}")
            elif keyword not in SemanticATSMatcher.GENERIC_WORDS:
                gaps.append(f"Missing skill: {keyword}")
        
        gaps = gaps[:10]  # Limit to top 10 gaps
        
        # Calculate match score
        if not job_terms:
            match_score = 0
        else:
            # Calculate base match percentage
            matched_high_value = sum(
                score for item in matched_with_scores
                if item['category'] != 'general'
                for score in [item['score']]
            )
            
            total_job_terms = len(job_terms)
            direct_match_ratio = len(direct_matches) / total_job_terms
            semantic_match_ratio = len(semantic_matches) / total_job_terms
            high_value_bonus = matched_high_value / (total_job_terms * 0.8)
            
            # Weighted score calculation
            base_score = (direct_match_ratio * 0.5 + semantic_match_ratio * 0.3) * 100
            bonus = min(high_value_bonus * 20, 20)
            match_score = min(base_score + bonus, 100)
            
            # Apply gap penalty for critical missing skills
            critical_gaps = len([g for g in gaps if 'critical' in g])
            if critical_gaps > 0:
                match_score = max(match_score - (critical_gaps * 10), 0)
            
            match_score = round(match_score, 1)
        
        # Generate reasoning
        reasoning = SemanticATSMatcher.generate_reasoning(
            match_score,
            len(direct_matches),
            len(semantic_matches),
            len(missing_keywords),
            gaps
        )
        
        return {
            'match_score': int(match_score),
            'matched_keywords': sorted(list(matched_keywords))[:20],
            'missing_keywords': missing_keywords[:15],
            'semantic_matches': semantic_matches,
            'strong_match_areas': strong_match_areas,
            'gaps': gaps,
            'reasoning': reasoning,
            'confidence_level': SemanticATSMatcher.get_confidence_level(match_score),
            'recommendation': SemanticATSMatcher.get_recommendation(match_score)
        }
    
    @staticmethod
    def generate_reasoning(score: float, direct_matches: int, semantic_matches: int, 
                          missing: int, gaps: List[str]) -> str:
        """Generate human-readable reasoning for the score"""
        if score >= 90:
            return (f"Excellent semantic alignment. Resume demonstrates {direct_matches} "
                   f"direct matches and {semantic_matches} semantic equivalences. "
                   f"Strong technical foundation with minimal gaps.")
        elif score >= 75:
            return (f"Strong match with relevant qualifications. Found {direct_matches} "
                   f"direct matches and {semantic_matches} semantic matches. "
                   f"{missing} skill gaps identified but not critical.")
        elif score >= 60:
            return (f"Moderate match. Candidate has {direct_matches} relevant skills with "
                   f"{semantic_matches} semantically equivalent competencies. "
                   f"However, {missing} important skills are missing.")
        elif score >= 40:
            return (f"Weak-moderate match. Only {direct_matches} direct matches found with "
                   f"{semantic_matches} semantic equivalences. Multiple significant skill gaps.")
        else:
            return (f"Poor alignment. Minimal overlap between resume qualifications and "
                   f"job requirements. Significant reskilling needed.")
    
    @staticmethod
    def get_confidence_level(score: float) -> str:
        """Determine confidence level in the match"""
        if score >= 85:
            return 'VERY HIGH'
        elif score >= 70:
            return 'HIGH'
        elif score >= 50:
            return 'MODERATE'
        elif score >= 30:
            return 'LOW'
        else:
            return 'VERY LOW'
    
    @staticmethod
    def get_recommendation(score: float) -> str:
        """Get hiring recommendation based on score"""
        if score >= 85:
            return 'STRONG CANDIDATE - Highly recommended for interview'
        elif score >= 70:
            return 'QUALIFIED - Suitable for interview with some skill gaps'
        elif score >= 50:
            return 'POTENTIAL - Candidate may need training on critical skills'
        elif score >= 30:
            return 'CONSIDER WITH CAUTION - Significant skill gaps identified'
        else:
            return 'NOT RECOMMENDED - Poor alignment with job requirements'
