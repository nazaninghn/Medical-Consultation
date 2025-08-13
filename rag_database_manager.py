#!/usr/bin/env python3
"""
RAG Database Manager for GP Medical Assistant
Tool to view, manage, and analyze the RAG database
"""

import os
import json
from datetime import datetime
from typing import Dict, List

class RAGDatabaseManager:
    """Manager for RAG database operations"""
    
    def __init__(self, knowledge_base_path: str = "medical_knowledge"):
        self.knowledge_base_path = knowledge_base_path
        self.json_file = os.path.join(knowledge_base_path, "medical_knowledge.json")
        self.vector_store_path = os.path.join(knowledge_base_path, "vector_store")
    
    def get_database_info(self) -> Dict:
        """Get comprehensive database information"""
        info = {
            "database_location": os.path.abspath(self.knowledge_base_path),
            "json_database": os.path.abspath(self.json_file),
            "vector_database": os.path.abspath(self.vector_store_path),
            "database_exists": os.path.exists(self.json_file),
            "vector_store_exists": os.path.exists(self.vector_store_path),
            "total_size_mb": 0,
            "files": []
        }
        
        # Calculate database size
        if os.path.exists(self.knowledge_base_path):
            total_size = 0
            for root, dirs, files in os.walk(self.knowledge_base_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    file_size = os.path.getsize(file_path)
                    total_size += file_size
                    
                    info["files"].append({
                        "name": file,
                        "path": os.path.relpath(file_path),
                        "size_kb": round(file_size / 1024, 2),
                        "modified": datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()
                    })
            
            info["total_size_mb"] = round(total_size / (1024 * 1024), 2)
        
        return info
    
    def get_knowledge_statistics(self) -> Dict:
        """Get statistics about the knowledge base content"""
        if not os.path.exists(self.json_file):
            return {"error": "Knowledge base not found"}
        
        with open(self.json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Analyze content
        categories = {}
        total_content_length = 0
        titles = []
        
        for item in data:
            category = item.get('category', 'unknown')
            categories[category] = categories.get(category, 0) + 1
            total_content_length += len(item.get('content', ''))
            titles.append(item.get('title', 'Untitled'))
        
        return {
            "total_documents": len(data),
            "categories": categories,
            "total_content_characters": total_content_length,
            "average_content_length": round(total_content_length / len(data)) if data else 0,
            "document_titles": titles
        }
    
    def search_knowledge_base(self, query: str) -> List[Dict]:
        """Search the knowledge base for specific content"""
        if not os.path.exists(self.json_file):
            return []
        
        with open(self.json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        query_lower = query.lower()
        results = []
        
        for item in data:
            title = item.get('title', '').lower()
            content = item.get('content', '').lower()
            category = item.get('category', '').lower()
            
            # Check if query matches title, content, or category
            title_match = query_lower in title
            content_match = query_lower in content
            category_match = query_lower in category
            
            if title_match or content_match or category_match:
                # Calculate relevance score
                score = 0
                if title_match:
                    score += 3
                if category_match:
                    score += 2
                if content_match:
                    score += 1
                
                results.append({
                    "title": item.get('title', 'Untitled'),
                    "category": item.get('category', 'unknown'),
                    "content_preview": item.get('content', '')[:200] + "...",
                    "relevance_score": score,
                    "matches": {
                        "title": title_match,
                        "content": content_match,
                        "category": category_match
                    }
                })
        
        # Sort by relevance score
        results.sort(key=lambda x: x['relevance_score'], reverse=True)
        return results
    
    def add_knowledge_entry(self, title: str, content: str, category: str = "custom") -> bool:
        """Add a new knowledge entry to the database"""
        try:
            # Load existing data
            if os.path.exists(self.json_file):
                with open(self.json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = []
            
            # Add new entry
            new_entry = {
                "category": category,
                "title": title,
                "content": content,
                "added_date": datetime.now().isoformat(),
                "source": "manual_addition"
            }
            
            data.append(new_entry)
            
            # Save updated data
            os.makedirs(self.knowledge_base_path, exist_ok=True)
            with open(self.json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"Error adding knowledge entry: {e}")
            return False
    
    def backup_database(self, backup_path: str = None) -> str:
        """Create a backup of the RAG database"""
        if backup_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"rag_backup_{timestamp}.json"
        
        try:
            if os.path.exists(self.json_file):
                with open(self.json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                backup_data = {
                    "backup_date": datetime.now().isoformat(),
                    "original_path": self.json_file,
                    "total_documents": len(data),
                    "knowledge_base": data
                }
                
                with open(backup_path, 'w', encoding='utf-8') as f:
                    json.dump(backup_data, f, indent=2, ensure_ascii=False)
                
                return f"Backup created: {os.path.abspath(backup_path)}"
            else:
                return "No database found to backup"
                
        except Exception as e:
            return f"Backup failed: {e}"
    
    def restore_database(self, backup_path: str) -> str:
        """Restore database from backup"""
        try:
            if not os.path.exists(backup_path):
                return f"Backup file not found: {backup_path}"
            
            with open(backup_path, 'r', encoding='utf-8') as f:
                backup_data = json.load(f)
            
            # Extract knowledge base data
            if "knowledge_base" in backup_data:
                knowledge_data = backup_data["knowledge_base"]
            else:
                # Assume the file is a direct knowledge base export
                knowledge_data = backup_data
            
            # Save restored data
            os.makedirs(self.knowledge_base_path, exist_ok=True)
            with open(self.json_file, 'w', encoding='utf-8') as f:
                json.dump(knowledge_data, f, indent=2, ensure_ascii=False)
            
            return f"Database restored from {backup_path}"
            
        except Exception as e:
            return f"Restore failed: {e}"
    
    def print_database_summary(self):
        """Print a comprehensive database summary"""
        print("🗄️  RAG Database Summary")
        print("=" * 50)
        
        # Database info
        db_info = self.get_database_info()
        print(f"📍 Database Location: {db_info['database_location']}")
        print(f"📊 Total Size: {db_info['total_size_mb']} MB")
        print(f"✅ JSON Database: {'Exists' if db_info['database_exists'] else 'Missing'}")
        print(f"🔍 Vector Store: {'Exists' if db_info['vector_store_exists'] else 'Missing'}")
        
        print("\n📁 Database Files:")
        for file_info in db_info['files']:
            print(f"   - {file_info['name']}: {file_info['size_kb']} KB")
        
        # Knowledge statistics
        if db_info['database_exists']:
            stats = self.get_knowledge_statistics()
            print(f"\n📚 Knowledge Base Statistics:")
            print(f"   Total Documents: {stats['total_documents']}")
            print(f"   Total Content: {stats['total_content_characters']:,} characters")
            print(f"   Average Length: {stats['average_content_length']} characters")
            
            print(f"\n🏷️  Categories:")
            for category, count in stats['categories'].items():
                print(f"   - {category}: {count} documents")
            
            print(f"\n📋 Document Titles:")
            for i, title in enumerate(stats['document_titles'][:10], 1):
                print(f"   {i}. {title}")
            if len(stats['document_titles']) > 10:
                print(f"   ... and {len(stats['document_titles']) - 10} more")

def main():
    """Main function for database management"""
    manager = RAGDatabaseManager()
    
    print("🧠 RAG Database Manager")
    print("=" * 30)
    
    while True:
        print("\nOptions:")
        print("1. Show database summary")
        print("2. Search knowledge base")
        print("3. Add knowledge entry")
        print("4. Backup database")
        print("5. Restore database")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == "1":
            manager.print_database_summary()
        
        elif choice == "2":
            query = input("Enter search query: ").strip()
            if query:
                results = manager.search_knowledge_base(query)
                print(f"\n🔍 Found {len(results)} results for '{query}':")
                for i, result in enumerate(results[:5], 1):
                    print(f"\n{i}. {result['title']} ({result['category']})")
                    print(f"   Score: {result['relevance_score']}")
                    print(f"   Preview: {result['content_preview']}")
        
        elif choice == "3":
            title = input("Enter title: ").strip()
            category = input("Enter category: ").strip() or "custom"
            print("Enter content (press Enter twice to finish):")
            content_lines = []
            while True:
                line = input()
                if line == "" and content_lines and content_lines[-1] == "":
                    break
                content_lines.append(line)
            
            content = "\n".join(content_lines[:-1])  # Remove last empty line
            
            if title and content:
                success = manager.add_knowledge_entry(title, content, category)
                if success:
                    print("✅ Knowledge entry added successfully!")
                else:
                    print("❌ Failed to add knowledge entry")
        
        elif choice == "4":
            backup_path = manager.backup_database()
            print(f"📦 {backup_path}")
        
        elif choice == "5":
            backup_file = input("Enter backup file path: ").strip()
            if backup_file:
                result = manager.restore_database(backup_file)
                print(f"🔄 {result}")
        
        elif choice == "6":
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()