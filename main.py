#!/usr/bin/env python3
"""
NYX Cybersecurity Portfolio Website Generator
Dynamically generates HTML files from Blog and Writeups folders
"""

import os
import glob
import markdown
import re
from datetime import datetime
from pathlib import Path
import json
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound

class PortfolioGenerator:
    def __init__(self):
        self.base_dir = Path(".")
        self.blog_dir = self.base_dir / "Blog"
        self.writeups_dir = self.base_dir / "Writeups"
        self.templates_dir = self.base_dir / "templates"
        self.output_dir = self.base_dir
        
        # Ensure directories exist
        self.blog_dir.mkdir(exist_ok=True)
        self.writeups_dir.mkdir(exist_ok=True)
        
        # Initialize markdown processor with enhanced extensions
        self.md = markdown.Markdown(extensions=[
            'meta', 
            'codehilite', 
            'toc', 
            'fenced_code',
            'tables',
            'nl2br'
        ], extension_configs={
            'codehilite': {
                'css_class': 'highlight',
                'use_pygments': True,
                'noclasses': False
            }
        })
        
        # Initialize Pygments formatter for syntax highlighting
        self.code_formatter = HtmlFormatter(
            style='monokai',
            cssclass='highlight',
            noclasses=False
        )
    
    def process_custom_boxes(self, content):
        """Process custom info boxes in markdown content"""
        box_patterns = {
            'StartGreenBox': ('success-box', 'EndGreenBox'),
            'StartRedBox': ('danger-box', 'EndRedBox'),
            'StartBlueBox': ('info-box', 'EndBlueBox'),
            'StartPurpleBox': ('note-box', 'EndPurpleBox'),
            'StartYellowBox': ('warning-box', 'EndYellowBox')
        }
        
        processed_content = content
        
        for start_tag, (css_class, end_tag) in box_patterns.items():
            pattern = f"{start_tag}(.*?){end_tag}"
            def replace_box(match):
                box_content = match.group(1).strip()
                return f'<div class="{css_class}">{box_content}</div>'
            
            processed_content = re.sub(pattern, replace_box, processed_content, flags=re.DOTALL)
        
        return processed_content

    def parse_markdown_file(self, file_path):
        """Parse markdown file and extract metadata"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Process custom info boxes before markdown conversion
            content = self.process_custom_boxes(content)
            
            # Reset markdown processor
            self.md.reset()
            html_content = self.md.convert(content)
            
            # Extract metadata
            metadata = getattr(self.md, 'Meta', {})
            
            # Get file stats
            stat = os.stat(file_path)
            created_date = datetime.fromtimestamp(stat.st_ctime)
            modified_date = datetime.fromtimestamp(stat.st_mtime)
            
            # Determine if this is a folder-based post
            folder_name = Path(file_path).parent.name
            if folder_name in ['Blog', 'Writeups']:
                # This is a root-level file, use filename
                slug = Path(file_path).stem
            else:
                # This is a folder-based post, use folder name
                slug = folder_name
            
            return {
                'title': metadata.get('title', [Path(file_path).stem.replace('-', ' ').title()])[0],
                'description': metadata.get('description', [''])[0],
                'tags': metadata.get('tags', []),
                'category': metadata.get('category', ['General'])[0],
                'date': metadata.get('date', [created_date.strftime('%Y-%m-%d')])[0],
                'content': html_content,
                'filename': slug,
                'file_path': str(file_path),
                'folder_path': str(Path(file_path).parent)
            }
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            return None
    
    def get_blog_posts(self):
        """Get all blog posts from Blog directory (including folder-based posts)"""
        blogs = []
        
        # Get direct markdown files in Blog directory
        blog_files = glob.glob(str(self.blog_dir / "*.md"))
        for file_path in blog_files:
            blog_data = self.parse_markdown_file(file_path)
            if blog_data:
                blogs.append(blog_data)
        
        # Get folder-based blog posts (look for index.md in subdirectories)
        blog_folders = [d for d in self.blog_dir.iterdir() if d.is_dir()]
        for folder in blog_folders:
            index_file = folder / "index.md"
            if index_file.exists():
                blog_data = self.parse_markdown_file(str(index_file))
                if blog_data:
                    blogs.append(blog_data)
        
        # Sort by date (newest first)
        blogs.sort(key=lambda x: x['date'], reverse=True)
        return blogs
    
    def get_writeups(self):
        """Get all CTF writeups from Writeups directory (including folder-based writeups)"""
        writeups = []
        
        # Get direct markdown files in Writeups directory
        writeup_files = glob.glob(str(self.writeups_dir / "*.md"))
        for file_path in writeup_files:
            writeup_data = self.parse_markdown_file(file_path)
            if writeup_data:
                writeups.append(writeup_data)
        
        # Get folder-based writeups (look for index.md in subdirectories)
        writeup_folders = [d for d in self.writeups_dir.iterdir() if d.is_dir()]
        for folder in writeup_folders:
            index_file = folder / "index.md"
            if index_file.exists():
                writeup_data = self.parse_markdown_file(str(index_file))
                if writeup_data:
                    writeups.append(writeup_data)
        
        # Sort by date (newest first)
        writeups.sort(key=lambda x: x['date'], reverse=True)
        return writeups
    
    def load_template(self, template_name):
        """Load HTML template"""
        template_path = self.templates_dir / template_name
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print(f"Template {template_name} not found")
            return ""
    
    def replace_template_variables(self, template_content, variables):
        """Replace template variables with actual content"""
        for key, value in variables.items():
            placeholder = f"{{{{{key}}}}}"
            template_content = template_content.replace(placeholder, str(value))
        return template_content
    
    def generate_blog_cards(self, blogs, limit=None):
        """Generate HTML cards for blog posts"""
        if limit:
            blogs = blogs[:limit]
        
        cards_html = ""
        for blog in blogs:
            # Extract first 150 characters for excerpt
            excerpt = re.sub('<[^<]+?>', '', blog['content'])[:150] + "..."
            
            tags_html = " ".join([f'<span class="tag">{tag}</span>' for tag in blog['tags']])
            
            cards_html += f'''
            <article class="content-card">
                <h3><a href="blog-{blog['filename']}.html">{blog['title']}</a></h3>
                <p class="excerpt">{excerpt}</p>
                <div class="meta">
                    <span class="date">{blog['date']}</span>
                    <div class="tags">{tags_html}</div>
                </div>
                <a href="blog-{blog['filename']}.html" class="read-more-btn">Read More</a>
            </article>
            '''
        
        return cards_html
    
    def generate_writeup_cards(self, writeups, limit=None):
        """Generate HTML cards for CTF writeups"""
        if limit:
            writeups = writeups[:limit]
        
        cards_html = ""
        for writeup in writeups:
            excerpt = re.sub('<[^<]+?>', '', writeup['content'])[:150] + "..."
            tags_html = " ".join([f'<span class="tag">{tag}</span>' for tag in writeup['tags']])
            
            cards_html += f'''
            <article class="content-card">
                <h3><a href="writeup-{writeup['filename']}.html">{writeup['title']}</a></h3>
                <p class="excerpt">{excerpt}</p>
                <div class="meta">
                    <span class="date">{writeup['date']}</span>
                    <span class="category">{writeup['category']}</span>
                    <div class="tags">{tags_html}</div>
                </div>
                <a href="writeup-{writeup['filename']}.html" class="read-more-btn">Read Writeup</a>
            </article>
            '''
        
        return cards_html
    
    def generate_individual_pages(self, blogs, writeups):
        """Generate individual blog and writeup pages"""
        base_template = self.load_template('base.html')
        
        # Generate individual blog pages
        for blog in blogs:
            page_content = f'''
            <main class="content-page">
                <article class="blog-post">
                    <header class="post-header">
                        <h1>{blog['title']}</h1>
                        <div class="post-meta">
                            <span class="date">{blog['date']}</span>
                            <div class="tags">
                                {" ".join([f'<span class="tag">{tag}</span>' for tag in blog['tags']])}
                            </div>
                        </div>
                    </header>
                    <div class="post-content">
                        {blog['content']}
                    </div>
                </article>
                <nav class="post-navigation">
                    <a href="blogs.html" class="back-link">← Back to Blogs</a>
                </nav>
            </main>
            '''
            
            variables = {
                'page_title': f"{blog['title']} - NYX Cybersecurity",
                'main_content': page_content
            }
            
            final_html = self.replace_template_variables(base_template, variables)
            
            output_path = self.output_dir / f"blog-{blog['filename']}.html"
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(final_html)
        
        # Generate individual writeup pages
        for writeup in writeups:
            page_content = f'''
            <main class="content-page">
                <article class="writeup-post">
                    <header class="post-header">
                        <h1>{writeup['title']}</h1>
                        <div class="post-meta">
                            <span class="date">{writeup['date']}</span>
                            <span class="category">{writeup['category']}</span>
                            <div class="tags">
                                {" ".join([f'<span class="tag">{tag}</span>' for tag in writeup['tags']])}
                            </div>
                        </div>
                    </header>
                    <div class="post-content">
                        {writeup['content']}
                    </div>
                </article>
                <nav class="post-navigation">
                    <a href="writeups.html" class="back-link">← Back to Writeups</a>
                </nav>
            </main>
            '''
            
            variables = {
                'page_title': f"{writeup['title']} - NYX Cybersecurity",
                'main_content': page_content
            }
            
            final_html = self.replace_template_variables(base_template, variables)
            
            output_path = self.output_dir / f"writeup-{writeup['filename']}.html"
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(final_html)
    
    def generate_all_pages(self):
        """Generate all website pages"""
        print("Generating NYX Cybersecurity Portfolio...")
        
        # Get content data
        blogs = self.get_blog_posts()
        writeups = self.get_writeups()
        
        print(f"Found {len(blogs)} blog posts and {len(writeups)} writeups")
        
        # Load base template
        base_template = self.load_template('base.html')
        
        # Generate main pages
        pages = [
            ('index.html', 'index.html', {
                'latest_blogs': self.generate_blog_cards(blogs, 3),
                'latest_writeups': self.generate_writeup_cards(writeups, 3)
            }),
            ('blogs.html', 'blogs.html', {
                'all_blogs': self.generate_blog_cards(blogs)
            }),
            ('writeups.html', 'writeups.html', {
                'all_writeups': self.generate_writeup_cards(writeups)
            }),
            ('services.html', 'services.html', {}),
            ('about.html', 'about.html', {}),
            ('contact.html', 'contact.html', {})
        ]
        
        for output_file, template_file, extra_vars in pages:
            template_content = self.load_template(template_file)
            
            if template_content:
                # Replace template variables
                variables = {
                    'page_title': f"NYX Cybersecurity - {output_file.split('.')[0].title()}",
                    **extra_vars
                }
                
                final_html = self.replace_template_variables(base_template, variables)
                final_html = self.replace_template_variables(final_html, variables)
                final_html = final_html.replace('{{main_content}}', template_content)
                
                # Write output file
                output_path = self.output_dir / output_file
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(final_html)
                
                print(f"Generated: {output_file}")
        
        # Generate individual blog and writeup pages
        self.generate_individual_pages(blogs, writeups)
        
        print("Portfolio generation complete!")

if __name__ == "__main__":
    generator = PortfolioGenerator()
    generator.generate_all_pages()
