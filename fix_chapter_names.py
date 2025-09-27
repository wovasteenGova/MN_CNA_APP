#!/usr/bin/env python3
import json
import re
from collections import Counter

def analyze_question_content(question_text):
    """Analyze question content to determine likely chapter"""
    question_lower = question_text.lower()
    
    # Define keywords for different chapters
    chapter_keywords = {
        'Safety': [
            'safety', 'hazard', 'fire', 'emergency', 'accident', 'injury', 'fall', 'burn', 
            'poison', 'electrical', 'disaster', 'elopement', 'workplace violence', 'restraint',
            'incident', 'risk', 'prevention', 'protective equipment', 'ppe'
        ],
        'Infection Control': [
            'infection', 'microbe', 'bacteria', 'virus', 'contamination', 'sterile', 'asepsis',
            'hand hygiene', 'gloves', 'mask', 'gown', 'isolation', 'pathogen', 'disinfection',
            'sterilization', 'transmission', 'precaution', 'hai', 'nosocomial'
        ],
        'Personal Care': [
            'bath', 'hygiene', 'grooming', 'perineal', 'oral care', 'skin care', 'hair care',
            'nail care', 'denture', 'shaving', 'dressing', 'undressing', 'morning care',
            'evening care', 'am care', 'pm care'
        ],
        'Vital Signs': [
            'temperature', 'pulse', 'blood pressure', 'respiration', 'vital signs', 'thermometer',
            'stethoscope', 'sphygmomanometer', 'tachycardia', 'bradycardia', 'hypertension',
            'hypotension', 'fever', 'afebrile', 'febrile'
        ],
        'Data Collection': [
            'observe', 'report', 'document', 'record', 'measure', 'assessment', 'signs',
            'symptoms', 'objective', 'subjective', 'normal', 'abnormal'
        ],
        'Basic Nursing Skills': [
            'positioning', 'transfer', 'mobility', 'bed making', 'feeding', 'nutrition',
            'elimination', 'catheter', 'enema', 'specimen', 'wound care', 'dressing change'
        ],
        'Mental Health': [
            'mental health', 'depression', 'anxiety', 'dementia', 'alzheimer', 'confusion',
            'behavior', 'psychiatric', 'cognitive', 'emotional', 'psychological'
        ],
        'Exercise and Activity': [
            'exercise', 'activity', 'mobility', 'range of motion', 'rom', 'ambulation',
            'walking', 'physical therapy', 'rehabilitation', 'movement', 'positioning'
        ],
        'Comfort, Rest, and Sleep': [
            'comfort', 'pain', 'rest', 'sleep', 'positioning', 'relaxation', 'comfort measures',
            'pain management', 'sleep disorders', 'insomnia'
        ],
        'Role and Responsibility': [
            'nursing assistant', 'cna', 'scope of practice', 'delegation', 'responsibility',
            'ethics', 'legal', 'certification', 'job description', 'supervision'
        ],
        'Communication': [
            'communication', 'listening', 'speaking', 'nonverbal', 'therapeutic', 'barriers',
            'language', 'interpreter', 'documentation', 'reporting'
        ],
        'Resident Rights': [
            'rights', 'privacy', 'dignity', 'confidentiality', 'consent', 'abuse', 'neglect',
            'ombudsman', 'grievance', 'advance directive'
        ]
    }
    
    # Score each chapter based on keyword matches
    scores = {}
    for chapter, keywords in chapter_keywords.items():
        score = 0
        for keyword in keywords:
            if keyword in question_lower:
                score += 1
        if score > 0:
            scores[chapter] = score
    
    # Return the chapter with the highest score
    if scores:
        return max(scores.items(), key=lambda x: x[1])[0]
    
    return None

def categorize_unknown_questions(questions):
    """Categorize questions in Unknown chapters based on content"""
    categorized = {}
    
    for question in questions:
        question_text = question.get('question', '')
        answer = question.get('answer', '')
        
        # Analyze both question and answer for context
        full_text = f"{question_text} {answer}"
        predicted_chapter = analyze_question_content(full_text)
        
        if predicted_chapter:
            if predicted_chapter not in categorized:
                categorized[predicted_chapter] = []
            categorized[predicted_chapter].append(question)
        else:
            # If we can't categorize, put in General/Miscellaneous
            if 'General' not in categorized:
                categorized['General'] = []
            categorized['General'].append(question)
    
    return categorized

def fix_chapter_names(filename):
    """Fix Unknown chapter names by analyzing content"""
    
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Analyzing {len(data)} chapters...")
    
    new_chapters = []
    unknown_questions_processed = 0
    
    for chapter in data:
        chapter_name = chapter['chapter']
        
        if 'Unknown Part' in chapter_name:
            print(f"\nProcessing {chapter_name} with {len(chapter['questions'])} questions...")
            
            # Categorize these questions
            categorized = categorize_unknown_questions(chapter['questions'])
            
            print(f"  Found content for: {list(categorized.keys())}")
            
            # Create new chapters based on categorization
            for new_chapter_name, questions in categorized.items():
                print(f"    - {new_chapter_name}: {len(questions)} questions")
                
                # Check if we need to split this category into parts
                if len(questions) <= 50:
                    new_chapters.append({
                        'chapter': new_chapter_name,
                        'questions': questions
                    })
                else:
                    # Split into parts
                    for i in range(0, len(questions), 50):
                        part_num = (i // 50) + 1
                        part_name = f"{new_chapter_name} Part {part_num}"
                        part_questions = questions[i:i+50]
                        
                        new_chapters.append({
                            'chapter': part_name,
                            'questions': part_questions
                        })
                        print(f"      Split into {part_name}: {len(part_questions)} questions")
            
            unknown_questions_processed += len(chapter['questions'])
            
        else:
            # Keep non-Unknown chapters as they are
            new_chapters.append(chapter)
    
    print(f"\n=== CHAPTER NAME FIXING SUMMARY ===")
    print(f"Unknown questions processed: {unknown_questions_processed}")
    print(f"Total chapters after fixing: {len(new_chapters)}")
    
    # Write the fixed file
    output_filename = filename.replace('.json', '_fixed.json')
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(new_chapters, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Fixed file written to: {output_filename}")
    
    # Show final chapter breakdown
    print(f"\n📊 Final chapter breakdown:")
    for chapter in sorted(new_chapters, key=lambda x: x['chapter']):
        print(f"  - {chapter['chapter']}: {len(chapter['questions'])} questions")
    
    return output_filename

def main():
    print("=== Fixing Unknown Chapter Names ===\n")
    
    # Fix the chapter names
    fixed_filename = fix_chapter_names('public/questions.json')
    
    # Validate the fixed file
    try:
        with open(fixed_filename, 'r', encoding='utf-8') as f:
            json.load(f)
        print(f"\n✅ Fixed JSON file is valid!")
    except Exception as e:
        print(f"\n❌ Fixed JSON validation error: {e}")
    
    # Replace the original file with the fixed one
    import shutil
    shutil.move(fixed_filename, 'public/questions.json')
    print(f"✅ Replaced original file with properly named chapters")

if __name__ == "__main__":
    main()
