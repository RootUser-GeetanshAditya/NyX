# NYX Cybersecurity Portfolio Website

## Overview

This is a professional cybersecurity portfolio website for NYX, a cybersecurity specialist focusing on reverse engineering, digital forensics and incident response (DFIR), penetration testing, and exploit development. The website serves as both a showcase of expertise and a platform for sharing technical content through blogs and CTF writeups. The site features a dynamic content generation system that converts Markdown files into HTML pages, allowing for easy content management and publication.

## User Preferences

Preferred communication style: Simple, everyday language.

## Recent Changes (Migration Completed - Aug 14, 2025)

✓ **Dependency Management Fixed**: Resolved missing pygments dependency issue by implementing graceful fallback for code highlighting
✓ **Template System Improved**: Fixed placeholder replacement issue in index.html - now properly shows actual blog and writeup content instead of {{latest_blogs}} and {{latest_writeups}} placeholders
✓ **File Structure Enhanced**: Modified main.py to generate HTML files in their original folder structure:
  - Blog posts: Generated in `Blog/[folder-name]/[filename].html` format
  - Writeup posts: Generated in `Writeups/[folder-name]/[filename].html` format
✓ **Navigation System Updated**: Fixed navigation links in nested folders to properly reference parent directory paths (../../)
✓ **Web Server Setup**: Configured Python HTTP server on port 5000 for development preview
✓ **SEO Enhancement**: Added XML sitemap generation for Google Search Console and robots.txt for better search engine indexing
✓ **GitHub Actions**: Implemented automated deployment workflow that regenerates the site on any repository changes
✓ **Cleanup**: Removed outdated blog/writeup HTML files in root directory - content now properly organized in folder structure
✓ **Migration Complete**: Project successfully migrated from Replit Agent to standard Replit environment

## System Architecture

### Frontend Architecture
The website uses a traditional multi-page HTML structure with a shared design system built around CSS custom properties and modern layout techniques. The design follows a cybersecurity aesthetic with a dark navy theme (#0B1220) and accent colors in green (#00C48C) and light blue (#7DD3FC). The frontend is built with semantic HTML5 and modern CSS using Grid and Flexbox for responsive layouts.

**Design System Components:**
- CSS custom properties for consistent theming
- Inter font for body text and JetBrains Mono for headings/code
- Responsive grid layouts that adapt from multi-column to single-column
- Hover animations and transitions for enhanced user experience
- Accessible design with proper ARIA labels and color contrast

**Page Structure:**
- Navigation bar with brand logo and main menu items
- Hero section with call-to-action buttons
- Content preview sections for blogs and writeups
- Individual pages for about, services, contact, and content listings

### Content Management System
The core architecture revolves around a Python-based static site generator (`main.py`) that processes Markdown files and generates HTML pages using a template system. This approach allows for easy content creation while maintaining a consistent site structure.

**Content Processing Pipeline:**
- Markdown files stored in `Blog/` and `Writeups/` directories
- Python script parses Markdown with metadata extraction
- Template system combines content with HTML templates
- Generated pages include proper navigation and styling

**Template System:**
- Base template (`templates/base.html`) provides common structure
- Page-specific templates for different content types
- Placeholder system for dynamic content insertion
- Consistent navigation and footer across all pages

### Static Asset Management
The website uses a simple static asset approach with all stylesheets contained in a single CSS file (`assets/style.css`). External dependencies are minimal, relying only on Google Fonts for typography and Font Awesome for icons via CDN.

**Asset Organization:**
- Single CSS file with modular organization
- External font loading from Google Fonts
- Icon system using Font Awesome CDN
- Responsive images and graphics support

### Content Structure
The website supports two main content types: technical blogs and CTF writeups. Each content type has its own directory structure and can include metadata for categorization and organization.

**Content Categories:**
- Blogs: Technical articles on cybersecurity topics
- Writeups: CTF challenge solutions and analysis
- Each content piece includes metadata for title, description, tags, and dates
- Support for content categorization and tagging

## External Dependencies

### Content Processing Dependencies
- **Python Markdown Library**: Converts Markdown content to HTML with support for metadata, code highlighting, and table of contents
- **Python Standard Library**: File system operations, path handling, and date/time processing

### Frontend Dependencies
- **Google Fonts**: Typography system using Inter and JetBrains Mono font families
- **Font Awesome**: Icon system via CDN for UI elements and visual enhancement
- **Modern CSS Features**: CSS Grid, Flexbox, and custom properties for layout and theming

### Development Dependencies
- **Python 3**: Runtime environment for the static site generator
- **File System**: Local storage for Markdown content and generated HTML files

### SEO and Deployment
- **XML Sitemap**: Automatically generated sitemap.xml for Google Search Console submission
- **Robots.txt**: Search engine crawling instructions with sitemap reference
- **GitHub Actions**: Automated deployment pipeline that regenerates the site on repository changes
- **GitHub Pages**: Static hosting platform integration for automatic deployment

The architecture is designed to be simple and maintainable, with minimal external dependencies and a clear separation between content creation (Markdown) and presentation (HTML/CSS). The static site generation approach ensures fast loading times and easy deployment to any web hosting platform.