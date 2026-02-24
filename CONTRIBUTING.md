# Contributor Guidelines

Thank you for your interest in contributing to Gaybeck Starkids SMS!

## How to Contribute

### Reporting Bugs
1. Check if the bug has already been reported in [Issues](https://github.com/gaybeck/gaybeck-starkids-sms/issues)
2. If not, create a new issue with:
   - Clear description
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots/logs if applicable

### Proposing Features
1. Open a discussion in [GitHub Discussions](https://github.com/gaybeck/gaybeck-starkids-sms/discussions)
2. Or create an [Issue](https://github.com/gaybeck/gaybeck-starkids-sms/issues) with label `enhancement`

### Submitting Code
1. **Fork** the repository
2. **Clone** your fork: `git clone https://github.com/yourusername/gaybeck-starkids-sms.git`
3. **Create a branch**: `git checkout -b feature/your-feature`
4. **Make changes** following our code style
5. **Test** your changes
6. **Commit** with clear messages: `git commit -m "Add feature description"`
7. **Push** to your fork: `git push origin feature/your-feature`
8. **Create a Pull Request** with a clear description

## Code Style

### Python
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use 4-space indentation
- Line length: max 88 characters
- Add docstrings to functions and classes

### JavaScript/React
- Use Prettier for formatting
- Follow ESLint rules
- Use 2-space indentation
- Add comments for complex logic

### Documentation
- Use clear, simple English
- Include examples where applicable
- Keep README.md and docs updated

## Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/gaybeck-starkids-sms.git
cd gaybeck-starkids-sms

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run the desktop app
python sms.py

# Or run the web app
cd web_app/backend
python app.py

# In another terminal
cd web_app/frontend
npm install
npm run dev
```

## Testing

Before submitting a pull request:
1. Test your changes thoroughly
2. Test on both desktop and web versions if applicable
3. Check for errors in the console
4. Test with different user roles (Admin, Teacher, Student)

## Commit Messages

Use clear, descriptive commit messages:
```
✨ Add new feature - Brief description
🐛 Fix bug - What was fixed
📚 Update docs - What was updated
🎨 Refactor code - What was refactored
⚡ Performance - What was optimized
```

## Pull Request Process

1. Update documentation if changes warrant
2. Add any new dependencies to requirements.txt
3. Follow the PR template
4. Link any related issues
5. Be responsive to feedback
6. Your PR will be reviewed within 7 days

## Code of Conduct

- Be respectful to all contributors
- No harassment, discrimination, or hate speech
- Constructive criticism only
- Help others learn and grow

## Questions?

- Check [existing discussions](https://github.com/gaybeck/gaybeck-starkids-sms/discussions)
- Ask in [Issues](https://github.com/gaybeck/gaybeck-starkids-sms/issues) with label `question`
- Email: support@gaybeckstarkids.com

## Maintainers

- @gaybeck - Project Lead
- Community Leaders - TBD

---

Thank you for contributing to make education better! 🎓
