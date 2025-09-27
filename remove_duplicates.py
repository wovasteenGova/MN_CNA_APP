#!/usr/bin/env python3
import json
from collections import defaultdict

def remove_duplicates(filename):
    """Remove duplicate questions from the JSON file"""
    
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Original file has {len(data)} chapters")
    
    # Track all unique questions
    seen_questions = set()
    duplicates_removed = 0
    total_questions_before = 0
    total_questions_after = 0
    
    # Process each chapter
    for chapter in data:
        chapter_name = chapter['chapter']
        original_count = len(chapter['questions'])
        total_questions_before += original_count
        
        # Filter out duplicates within this chapter and globally
        unique_questions = []
        
        for question in chapter['questions']:
            # Create a unique key for the question
            question_text = question.get('question', '').strip().lower()
            answer_text = question.get('answer', '').strip().lower()
            
            # Skip empty questions
            if not question_text or not answer_text:
                duplicates_removed += 1
                continue
            
            key = (question_text, answer_text)
            
            if key not in seen_questions:
                seen_questions.add(key)
                unique_questions.append(question)
            else:
                duplicates_removed += 1
                print(f"  Removed duplicate from {chapter_name}: '{question_text[:60]}...'")
        
        chapter['questions'] = unique_questions
        new_count = len(unique_questions)
        total_questions_after += new_count
        
        if original_count != new_count:
            print(f"Chapter '{chapter_name}': {original_count} → {new_count} questions")
    
    # Remove any chapters that became empty
    data = [chapter for chapter in data if len(chapter['questions']) > 0]
    
    print(f"\n=== DEDUPLICATION SUMMARY ===")
    print(f"Total questions before: {total_questions_before}")
    print(f"Total questions after: {total_questions_after}")
    print(f"Duplicates removed: {duplicates_removed}")
    print(f"Chapters remaining: {len(data)}")
    
    # Write the clean file
    output_filename = filename.replace('.json', '_clean.json')
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Clean file written to: {output_filename}")
    
    # Show final chapter breakdown
    print(f"\n📊 Final chapter breakdown:")
    for chapter in data:
        print(f"  - {chapter['chapter']}: {len(chapter['questions'])} questions")
    
    return output_filename

def main():
    print("=== Removing Duplicates from Final JSON ===\n")
    
    # Remove duplicates from the final file
    clean_filename = remove_duplicates('public/questions_final.json')
    
    # Validate the clean file
    try:
        with open(clean_filename, 'r', encoding='utf-8') as f:
            json.load(f)
        print(f"\n✅ Clean JSON file is valid!")
    except Exception as e:
        print(f"\n❌ Clean JSON validation error: {e}")
    
    # Replace the original final file with the clean one
    import shutil
    shutil.move(clean_filename, 'public/questions_final.json')
    print(f"✅ Replaced original file with deduplicated version")

if __name__ == "__main__":
    main()
