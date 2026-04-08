#!/usr/bin/env python3
"""
Test script for Semantic ATS Matcher
Run from backend directory: python test_semantic_matcher.py
"""

from services.semantic_matcher import SemanticATSMatcher

def test_case_1():
    """Test: Excellent match"""
    resume = """
    Senior Full-Stack Engineer with 7 years experience:
    - Languages: Python, JavaScript, TypeScript
    - Frontend: React, Redux, CSS, HTML
    - Backend: Django, Flask, FastAPI
    - Databases: PostgreSQL, MongoDB, Redis
    - DevOps: Docker, Kubernetes, AWS, CI/CD
    - Testing: pytest, Jest, unit testing, integration testing
    - APIs: REST API design, GraphQL, Microservices
    """
    
    job = """
    Seeking Senior Full-Stack Engineer:
    - Required: Python, JavaScript, React, Django, PostgreSQL
    - Required: Docker, AWS, REST API design
    - Preferred: Kubernetes, GraphQL, Redis
    - Nice to have: Microservices architecture
    """
    
    print("=" * 80)
    print("TEST 1: Excellent Match (Expected: 85-95)")
    print("=" * 80)
    result = SemanticATSMatcher.match_resume_and_job(resume, job)
    print_result(result)
    print()


def test_case_2():
    """Test: Good match with gaps"""
    resume = """
    Full-Stack Developer with 5 years experience:
    - Languages: Python, JavaScript
    - Frontend: React, Vue
    - Backend: Django
    - Database: PostgreSQL
    - Tools: Git, Docker
    """
    
    job = """
    Seeking Full-Stack Developer:
    - Required: React, Python, Django, PostgreSQL
    - Required: REST APIs, Git, responsive design
    - Preferred: TypeScript, Docker, AWS, GraphQL
    - Nice to have: Kubernetes, microservices
    """
    
    print("=" * 80)
    print("TEST 2: Good Match with Gaps (Expected: 70-80)")
    print("=" * 80)
    result = SemanticATSMatcher.match_resume_and_job(resume, job)
    print_result(result)
    print()


def test_case_3():
    """Test: Moderate match, poor fit"""
    resume = """
    Frontend Developer:
    - Specialized in React, Vue, JavaScript
    - Experience with HTML, CSS, responsive design
    - Some backend knowledge in Node.js
    - Used GraphQL for data fetching
    """
    
    job = """
    Senior Backend Engineer - Python:
    - Required: Python, Java, or Go
    - Required: Relational databases, SQL
    - Required: Backend frameworks and architecture
    - Required: Microservices, API design
    - Preferred: Kubernetes, DevOps
    """
    
    print("=" * 80)
    print("TEST 3: Poor Fit (Expected: 30-45)")
    print("=" * 80)
    result = SemanticATSMatcher.match_resume_and_job(resume, job)
    print_result(result)
    print()


def test_case_4():
    """Test: Semantic equivalence recognition"""
    resume = """
    Developer experienced with:
    - Client-server application architecture
    - RESTful endpoints and HTTP services
    - Browser-based extensions
    - Content parsing and extraction
    - File handling and multipart uploads
    """
    
    job = """
    Seeking Developer:
    - Familiar with REST APIs and microservice architecture
    - Built Chrome extensions or browser add-ons
    - Experience with web scraping and data extraction
    - Supported file uploads and pasted text inputs
    """
    
    print("=" * 80)
    print("TEST 4: Semantic Equivalence (Expected: High match with semantic_matches)")
    print("=" * 80)
    result = SemanticATSMatcher.match_resume_and_job(resume, job)
    print_result(result)
    print()


def test_case_5():
    """Test: Generic word filtering"""
    resume = """
    A student working on various projects focused on team building and small development workflows.
    Experience with the following: Python, React, working with teams to manage and build applications.
    Responsible for supporting different areas and coding various systems.
    """
    
    job = """
    Position involving building applications for teams and organizations.
    Required experience with Python and React. Focused on managing projects.
    Role involves various workflows and team collaboration.
    """
    
    print("=" * 80)
    print("TEST 5: Generic Word Filtering (Only core skills matter)")
    print("=" * 80)
    result = SemanticATSMatcher.match_resume_and_job(resume, job)
    print(f"Matched Keywords: {result['matched_keywords']}")
    print(f"Expected: ['python', 'react'] (generic words filtered out)")
    print(f"Score: {result['match_score']} (should be moderate despite generic language)")
    print()


def print_result(result):
    """Pretty print result"""
    print(f"\n📊 MATCH SCORE: {result['match_score']}/100")
    print(f"🔹 Confidence Level: {result['confidence_level']}")
    print(f"✅ Recommendation: {result['recommendation']}\n")
    
    print(f"✓ Matched Keywords ({len(result['matched_keywords'])}):")
    for kw in result['matched_keywords'][:10]:
        print(f"  - {kw}")
    if len(result['matched_keywords']) > 10:
        print(f"  ... and {len(result['matched_keywords']) - 10} more")
    
    print(f"\n✗ Missing Keywords ({len(result['missing_keywords'])}):")
    for kw in result['missing_keywords'][:10]:
        print(f"  - {kw}")
    if len(result['missing_keywords']) > 10:
        print(f"  ... and {len(result['missing_keywords']) - 10} more")
    
    if result['semantic_matches']:
        print(f"\n⚡ Semantic Matches ({len(result['semantic_matches'])}):")
        for match in result['semantic_matches'][:5]:
            print(f"  - '{match['job_term']}' ≈ '{match['resume_term']}'")
            print(f"    {match['reason']}")
        if len(result['semantic_matches']) > 5:
            print(f"  ... and {len(result['semantic_matches']) - 5} more")
    
    if result['strong_match_areas']:
        print(f"\n💪 Strong Match Areas:")
        for area in result['strong_match_areas']:
            print(f"  - {area}")
    
    if result['gaps']:
        print(f"\n⚠️  Gaps:")
        for gap in result['gaps'][:5]:
            print(f"  - {gap}")
        if len(result['gaps']) > 5:
            print(f"  ... and {len(result['gaps']) - 5} more")
    
    print(f"\n📝 Reasoning:")
    print(f"  {result['reasoning']}\n")


def main():
    """Run all tests"""
    print("\n")
    print("🚀" * 40)
    print("SEMANTIC ATS MATCHER - TEST SUITE")
    print("🚀" * 40)
    print("\n")
    
    try:
        test_case_1()
        test_case_2()
        test_case_3()
        test_case_4()
        test_case_5()
        
        print("=" * 80)
        print("✅ All tests completed successfully!")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
