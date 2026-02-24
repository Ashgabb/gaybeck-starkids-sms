# [Gaybeck Starkids SMS](https://github.com/gaybeck/gaybeck-starkids-sms)

> A comprehensive, AI-powered school management system for modern educational institutions

## 🚀 Features

- ✅ Complete student, teacher, and class management
- ✅ AI-powered assessment generation (5 subjects)
- ✅ Real-time analytics and predictive insights
- ✅ Desktop application (Windows) + Web interface
- ✅ Role-based access control
- ✅ Automated financial tracking
- ✅ Real-time data synchronization
- ✅ Comprehensive backup system

## 📥 Quick Start

### Desktop (Windows)
```bash
# Download setup.bat and run it
setup.bat

# Launch the app
launch_sms.vbs
```

### Web Version
```bash
# Backend
cd web_app/backend && pip install -r requirements.txt && python app.py

# Frontend (in new terminal)
cd web_app/frontend && npm install && npm run dev
```

## 📊 System Requirements

| Component | Requirement |
|-----------|------------|
| OS | Windows 10+ / Any modern OS |
| Python | 3.13+ |
| Node.js | 16+ (for web) |
| Disk Space | 500MB+ |
| RAM | 4GB+ |

## 🏗️ Project Structure

```
gaybeck-starkids-sms/
├── sms.py                      # Main desktop app
├── ai_assessment_grading.py    # AI engine
├── realtime_sync.py            # Data sync
├── web_app/
│   ├── backend/                # Flask API
│   └── frontend/               # React UI
├── website/                    # Marketing site
├── database/                   # SQLite & sync
├── docs/                       # Documentation
└── setup.bat                   # Installer
```

## 🔐 Demo Credentials

| Role | Username | Password |
|------|----------|----------|
| Admin | admin | admin123 |
| Teacher | teacher1 | teacher123 |
| Student | student1 | student123 |

## 📚 Documentation

- **[START_HERE.md](START_HERE.md)** - Getting started (5 min)
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Feature guide (10 min)
- **[SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md)** - Detailed setup (15 min)
- **[API Documentation](docs/)** - Full API reference

## 🛠️ Tech Stack

### Desktop
- Python 3.13+ with Tkinter
- SQLite3 database
- scikit-learn, pandas, numpy

### Web
- Flask backend with REST API
- React 18+ frontend
- Shared SQLite database

## 🚀 Deployment

### Desktop Users
- Run `setup.bat` for automated installation
- Get desktop shortcuts automatically
- Automatic dependency management

### Web Deployment
- Deploy backend to Heroku, AWS, or Docker
- Deploy frontend to Netlify, Vercel, or GitHub Pages
- Use `docker-compose.yml` for containerized setup

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

```bash
# Fork, clone, and create a feature branch
git clone https://github.com/yourusername/gaybeck-starkids-sms.git
cd gaybeck-starkids-sms
git checkout -b feature/your-feature
git commit -am "Add your feature"
git push origin feature/your-feature
```

## 📝 License

MIT License - Completely free for personal and commercial use.

See [LICENSE](LICENSE) for details.

## 📧 Support

- **Issues:** [GitHub Issues](https://github.com/gaybeck/gaybeck-starkids-sms/issues)
- **Discussions:** [GitHub Discussions](https://github.com/gaybeck/gaybeck-starkids-sms/discussions)
- **Email:** support@gaybeckstarkids.com

## ⭐ Show Your Support

If you find this helpful, please star the repository! ⭐

---

**Last Updated:** February 24, 2026  
**Version:** 1.0.0  
**Status:** Production Ready ✅
