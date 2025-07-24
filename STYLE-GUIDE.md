# Tech Articles Style Guide

## Repository Structure

```
tech-articles/
├── README.md                           # Main index with article list
├── article-name/
│   ├── README.md                      # Main article content
│   ├── images/                        # All images for the article
│   │   ├── diagram-1.png
│   │   └── screenshot-2.png
│   ├── assets/                        # Scripts, configs, additional files
│   │   ├── setup-script.sh
│   │   └── config-example.conf
│   └── code/                          # Code examples (if extensive)
│       ├── python/
│       └── java/
└── future-article/
    └── ... (same structure)
```

## Article Naming Convention

- Use kebab-case: `mesh-vpn-raspberry-pi`
- Be descriptive but concise
- Include main technology: `docker-deployment-aws`
- Target length: 2-4 words

## Markdown Structure

### Header Template
```markdown
# Article Title

![Main Diagram](./images/main-diagram.png)

Brief introduction paragraph explaining what readers will learn.

## The Problem

Describe the problem or challenge this article solves.

## The Solution

Main content with step-by-step instructions.

### Step 1: Title
### Step 2: Title
### Step 3: Title

## Benefits/Results

What advantages does this approach provide?

## Conclusion

Summary and what's next.

---

## Quick Reference

### Essential Commands
```bash
# Commands here
```

### Useful Links
- [Official Documentation](link)
- [Related Resource](link)
```

## Code Formatting Standards

### Command Blocks
```bash
# Always include comments
sudo apt update
sudo apt install package-name

# Explain what happens next
sudo systemctl enable service-name
```

### Configuration Examples
```yaml
# config.yml
# Always include file path in comment above
setting: value
nested:
  option: true
```

### Multi-language Support
When showing commands for different systems:

```bash
# Ubuntu/Debian
sudo apt install package

# CentOS/RHEL  
sudo yum install package

# macOS
brew install package
```

## Image Guidelines

### File Naming
- Use descriptive names: `network-topology-before.png`
- Include sequence numbers: `setup-step-1.png`, `setup-step-2.png`
- Keep consistent style across article

### Alt Text Requirements
Always include meaningful alt text:
```markdown
![Network topology showing Raspberry Pi connected to router](./images/network-diagram.png)
```

### Image Size
- Optimize for web (< 500KB per image)
- Use PNG for diagrams, JPG for photos
- Consistent width (800px recommended)

## Content Style

### Target Audience
- **Primary**: Developers, DevOps engineers, IoT enthusiasts
- **Secondary**: Hobbyists, students, tech-curious individuals
- **Tone**: Professional but approachable, avoid jargon without explanation

### Writing Guidelines
- Start with problem statement
- Provide step-by-step instructions
- Include troubleshooting section
- End with practical next steps
- Use active voice
- Include "why" explanations, not just "how"

### Code Examples
- Always test commands before publishing
- Include error handling where relevant
- Provide complete, working examples
- Add comments explaining non-obvious steps

## Tags/Topics Guidelines

### Required Tags (choose 5-8)
**Technology-specific:**
- Main platform: `raspberry-pi`, `arduino`, `esp32`
- Main software: `docker`, `kubernetes`, `tailscale`
- Programming language: `python`, `java`, `bash`

**Category tags:**
- `iot`, `networking`, `security`, `automation`
- `tutorial`, `guide`, `how-to`

**Difficulty level:**
- `beginner`, `intermediate`, `advanced`

### Tag Selection Rules
- Maximum 10 tags total
- Include both specific and general tags
- Use existing popular tags when possible
- Be consistent across similar articles

## File Organization

### Assets Folder
```
assets/
├── scripts/           # Installation/setup scripts
├── configs/          # Configuration file examples  
├── data/            # Sample data files
└── templates/       # Template files
```

### Images Folder
```
images/
├── diagrams/        # Network diagrams, flowcharts
├── screenshots/     # UI screenshots, terminal output
└── photos/         # Physical setup photos
```

## Quality Checklist

Before publishing an article:

- [ ] All commands tested on target platform
- [ ] Images optimized and properly named
- [ ] All links working
- [ ] Code examples complete and functional
- [ ] Spelling and grammar checked
- [ ] Consistent formatting throughout
- [ ] Alt text for all images
- [ ] Quick reference section included
- [ ] GitHub topics/tags added
- [ ] Article added to main README.md

## LinkedIn Adaptation Guidelines

### Format Differences
- **Length**: 300-800 words (vs 1000+ for GitHub)
- **Structure**: Less headers, more flowing text
- **Call-to-action**: Link back to GitHub for full details
- **Tone**: More personal, less technical

### LinkedIn Template
```
🔧 Just solved a common IoT problem... [hook]

[2-3 paragraphs explaining the problem and solution]

💡 Key benefits:
• Point 1
• Point 2  
• Point 3

Full technical guide with code examples: [GitHub link]

#RaspberryPi #IoT #Networking #TechTutorial
```

## Version Control

### Commit Messages
- Use conventional commits: `feat:`, `fix:`, `docs:`
- Be descriptive: `docs: add troubleshooting section to mesh VPN article`
- Reference issues when applicable

### Branching Strategy
- `main` - published articles
- `draft/article-name` - work in progress
- `update/article-name` - updates to existing articles

---

*This style guide ensures consistency across all articles in the tech-articles repository.*