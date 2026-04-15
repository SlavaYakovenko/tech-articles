# AGENTS.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
This repository is a collection of technical articles covering networking, IoT, microboards, and data processing. Each article is organized into its own directory following a strict style guide.

## Repository Structure
- `README.md`: The main index listing all available articles.
- `STYLE-GUIDE.md`: Detailed standards for article structure, naming, and formatting.
- `article-name/`: Individual article directories.
    - `README.md`: The main article content.
    - `images/`: Article-specific diagrams and screenshots.
    - `assets/`: Scripts, configurations, and additional resources.
    - `code/`: Extensive code examples.

## Development Standards

### Article Creation & Modification
- **Naming**: Use `kebab-case` for directory names (e.g., `mesh-vpn-raspberry-pi`).
- **Structure**: Follow the Header Template defined in `STYLE-GUIDE.md` (Problem $\rightarrow$ Solution $\rightarrow$ Benefits $\rightarrow$ Conclusion $\rightarrow$ Quick Reference).
- **Images**: 
    - Place in `images/` folder.
    - Use descriptive names with sequence numbers (e.g., `setup-step-1.png`).
    - Always include meaningful alt text in Markdown.
- **Code Blocks**:
    - Include comments in bash scripts.
    - Provide the file path in a comment above configuration examples.
    - Support multiple OS platforms where applicable (Ubuntu, CentOS, macOS).
- **Index**: Any new article must be added to the root `README.md`.

### Git Workflow
- **Commits**: Use conventional commits (`feat:`, `fix:`, `docs:`).
- **Branching**: 
    - `main`: Published articles.
    - `draft/article-name`: Work in progress.
    - `update/article-name`: Updates to existing articles.

## Common Tasks
- **Adding a new article**:
    1. Create a directory in `kebab-case`.
    2. Create `README.md` following the style guide.
    3. Add images to `images/` and assets to `assets/`.
    4. Update the root `README.md` with a link and description.
- **Updating an article**:
    1. Modify the article's `README.md`.
    2. Ensure all new images follow the naming convention.
    3. Verify the root `README.md` still accurately reflects the content.
