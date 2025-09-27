#!/usr/bin/env python3
import json
from collections import defaultdict

def consolidate_chapters(filename):
    """Consolidate chapters with the same name and split large ones"""
    
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Consolidating {len(data)} chapters...")
    
    # Group questions by chapter name (ignoring "Part X" suffixes for now)
    chapter_groups = defaultdict(list)
    
    for chapter in data:
        chapter_name = chapter['chapter']
        
        # Remove "Part X" from chapter names for grouping
        base_name = chapter_name
        if ' Part ' in chapter_name:
            base_name = chapter_name.split(' Part ')[0]
        
        # Add all questions to the base chapter
        chapter_groups[base_name].extend(chapter['questions'])
    
    print(f"Consolidated into {len(chapter_groups)} base chapters")
    
    # Now split chapters that are too large (>50 questions) into parts
    final_chapters = []
    
    for chapter_name, questions in chapter_groups.items():
        if len(questions) <= 50:
            # Keep as single chapter
            final_chapters.append({
                'chapter': chapter_name,
                'questions': questions
            })
            print(f"  {chapter_name}: {len(questions)} questions")
        else:
            # Split into parts
            parts_created = []
            for i in range(0, len(questions), 50):
                part_num = (i // 50) + 1
                part_name = f"{chapter_name} Part {part_num}"
                part_questions = questions[i:i+50]
                
                final_chapters.append({
                    'chapter': part_name,
                    'questions': part_questions
                })
                parts_created.append(f"{part_name} ({len(part_questions)} questions)")
            
            print(f"  {chapter_name}: {len(questions)} questions → split into {len(parts_created)} parts:")
            for part in parts_created:
                print(f"    - {part}")
    
    # Sort chapters alphabetically
    final_chapters.sort(key=lambda x: x['chapter'])
    
    print(f"\n=== CONSOLIDATION SUMMARY ===")
    print(f"Final chapters: {len(final_chapters)}")
    total_questions = sum(len(ch['questions']) for ch in final_chapters)
    print(f"Total questions: {total_questions}")
    
    # Write the consolidated file
    output_filename = filename.replace('.json', '_consolidated.json')
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(final_chapters, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Consolidated file written to: {output_filename}")
    
    # Show final chapter breakdown
    print(f"\n📊 Final chapter breakdown:")
    for chapter in final_chapters:
        print(f"  - {chapter['chapter']}: {len(chapter['questions'])} questions")
    
    return output_filename

def main():
    print("=== Consolidating Chapters ===\n")
    
    # Consolidate the chapters
    consolidated_filename = consolidate_chapters('public/questions.json')
    
    # Validate the consolidated file
    try:
        with open(consolidated_filename, 'r', encoding='utf-8') as f:
            json.load(f)
        print(f"\n✅ Consolidated JSON file is valid!")
    except Exception as e:
        print(f"\n❌ Consolidated JSON validation error: {e}")
    
    # Replace the original file with the consolidated one
    import shutil
    shutil.move(consolidated_filename, 'public/questions.json')
    print(f"✅ Replaced original file with consolidated chapters")

if __name__ == "__main__":
    main()
