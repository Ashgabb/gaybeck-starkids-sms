# Website Deployment Guide

## Quick Start

### Local Testing
```batch
cd website
python -m http.server 8000
```
Then open: http://localhost:8000

### With Backend API
```batch
cd website
pip install -r requirements-backend.txt
python app.py
```
Then open: http://localhost:5000

---

## What's New: Testing & Demo Features

### 🆕 "Try Before You Buy" Section
- Interactive demo tabs with sample data
- All 6 modules demonstrated
- No login/registration required
- Full feature preview

### 🆕 Feature Comparison Page
- Desktop vs Web App vs Demo comparison
- Side-by-side feature matrix
- Pricing and recommendation guide
- Links to testing environment

### 🆕 Sample Data
- 8+ sample students
- Multiple classes
- Attendance records
- Grade data
- Financial summaries
- Analytics insights

### 🆕 Backend API Endpoints
- `/api/demo/students` - Sample student data
- `/api/demo/attendance/<class>` - Attendance records
- `/api/demo/grades/<student>` - Grade information
- `/api/demo/analytics` - Analytics data
- `/api/demo/financial` - Financial summaries

See `TESTING_GUIDE.md` for complete testing documentation.

---

## Deployment Options

## 1. GitHub Pages (Recommended)

### Step 1: Prepare Repository
```bash
# Navigate to project root
cd c:\Users\User\Desktop\GAYBECK STARKIDS SMS

# Add website folder if not already tracked
git add website/
git commit -m "feat: Add professional marketing website with testing demo"
git push origin main
```

### Step 2: Enable GitHub Pages
1. Go to your GitHub repository: `https://github.com/Ashgabb/gaybeck-starkids-sms`
2. Click **Settings** tab
3. Scroll to **Pages** section
4. Under "Build and deployment":
   - **Source**: Deploy from a branch
   - **Branch**: Select `main`
   - **Folder**: Select `/website`
5. Click **Save**

### Step 3: Access Your Website
- **URL**: `https://ashgabb.github.io/gaybeck-starkids-sms/`
- **Demo**: `https://ashgabb.github.io/gaybeck-starkids-sms/#demo`
- **Comparison**: `https://ashgabb.github.io/gaybeck-starkids-sms/comparison.html`
- Wait 2-3 minutes for GitHub to build and deploy
- Check "Actions" tab to see deployment status

### Step 4: Custom Domain (Optional)
1. In **Settings → Pages**
2. Under "Custom domain", enter your domain (e.g., `sms.gaybeckstarkids.com`)
3. Add DNS records pointing to GitHub (GitHub provides instructions)
4. GitHub will automatically set up HTTPS

---

## 2. Alternative Hosting Services

### Netlify
1. Sign up at netlify.com
2. Connect your GitHub repository
3. Set build settings:
   - **Base directory**: `website`
   - **Publish directory**: `website`
4. Deploy automatically on each push

### Vercel
1. Sign up at vercel.com
2. Import GitHub project
3. Set project root to `website`
4. Deploy

### AWS S3 + CloudFront
1. Create S3 bucket
2. Upload website files
3. Enable static website hosting
4. Set up CloudFront distribution
5. Use Route53 for DNS

---

## 3. Traditional Web Hosting

### Using FTP
1. Get FTP credentials from hosting provider
2. Use FTP client (FileZilla, WinSCP)
3. Connect to server
4. Upload all files from `website/` folder to `public_html/` or `www/` directory
5. Ensure directory structure:
   ```
   /public_html/
   ├── index.html
   ├── styles.css
   ├── script.js
   └── start_server.bat (optional - not needed on production)
   ```

### Using Control Panel (cPanel)
1. Log in to cPanel
2. File Manager → public_html
3. Upload files directly
4. Or use "Import from URL" for GitHub

---

## Pre-Deployment Checklist

- [ ] All HTML, CSS, and JavaScript files created
- [ ] Links in navigation all point to correct sections
- [ ] Contact form works and validates email
- [ ] Download button link is correct
- [ ] Images/icons load properly
- [ ] Responsive design tested on mobile
- [ ] All buttons and links are functional
- [ ] No console errors (F12 in browser)
- [ ] Page loads in < 3 seconds
- [ ] Cross-browser tested (Chrome, Firefox, Edge)
- [ ] HTTPS will be enabled
- [ ] Meta tags and descriptions added
- [ ] Favicon displays correctly

---

## Post-Deployment Steps

### 1. Verify Deployment
```
1. Visit your deployed URL
2. Test all links and buttons
3. Check responsive design on mobile
4. View browser console (F12) for errors
```

### 2. Enable HTTPS
- **GitHub Pages**: Automatic ✅
- **Netlify**: Automatic ✅
- **Vercel**: Automatic ✅
- **Traditional Hosting**: Use Let's Encrypt (free) or purchase certificate

### 3. Set Up Analytics
```html
<!-- Add to <head> section of index.html -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_ID');
</script>
```

### 4. SEO Optimization
```html
<!-- Update meta tags in <head> -->
<meta name="description" content="Your description">
<meta name="keywords" content="keywords">
<meta name="author" content="Your Name">

<!-- Open Graph for social sharing -->
<meta property="og:title" content="Gaybeck Starkids SMS">
<meta property="og:description" content="Description">
<meta property="og:image" content="URL_TO_IMAGE">
<meta property="og:url" content="https://your-domain.com">
```

### 5. SSL Certificate
```
For traditional hosting:
1. Install Let's Encrypt certificate
2. Force HTTPS redirect:
   - Apache: Add to .htaccess
   - Nginx: Add to config
   - cPanel: Use AutoSSL
```

### 6. Backup
```bash
# Before each deployment
git commit -m "backup: Website before deployment"
git push origin main
```

---

## Troubleshooting

### Website Not Showing
- [ ] Check DNS settings are correct
- [ ] Verify files are in correct directory
- [ ] Clear browser cache (Ctrl+Shift+Delete)
- [ ] Wait 5-10 minutes for DNS to propagate

### Styles Not Displaying
- [ ] Check CSS file exists in same directory
- [ ] Verify `<link>` tag in HTML head
- [ ] Check file permissions (644 for files)
- [ ] Try different browser

### Links Not Working
- [ ] Verify links use correct href values
- [ ] Check anchor IDs match link targets
- [ ] Test with trailing slashes: `/index.html/`

### Forms Not Submitting
- [ ] Check JavaScript file is loading
- [ ] Verify form validation logic
- [ ] Check backend API endpoint (if used)
- [ ] Test in different browser

### Mobile Not Responsive
- [ ] Add viewport meta tag:
  ```html
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  ```
- [ ] Test on actual mobile device
- [ ] Check media queries in CSS

### Performance Issues
- [ ] Minimize and compress images
- [ ] Enable gzip compression
- [ ] Use CDN for static files
- [ ] Minify CSS and JavaScript
- [ ] Check database queries (if applicable)

---

## Monitoring & Maintenance

### Regular Checks
- [ ] Website uptime (use UptimeRobot.com)
- [ ] Page load speed (use PageSpeed Insights)
- [ ] Broken links (use screaming-frog.com)
- [ ] Security (use Security Headers check)

### Update Content
1. Edit files locally
2. Test with `start_server.bat`
3. Commit and push to GitHub
4. Website updates automatically

### Backup Routine
```bash
# Weekly backup
git commit -m "backup: $(date +%Y-%m-%d)"
git push origin main

# Or manually copy website folder
```

---

## Marketing After Launch

### 1. Social Media
- Share website link on platforms
- Create posts about features
- Post testimonials and success stories
- Share download links

### 2. Email
- Send newsletter with website link
- Update email signature
- Create email campaign

### 3. SEO
- Submit to Google Search Console
- Submit sitemap.xml
- Create blog posts
- Build backlinks

### 4. Advertising
- Google Ads campaign
- Facebook/Instagram ads
- LinkedIn ads (B2B schools)

---

## Advanced: Custom Domain

### Using Godaddy or Namecheap

1. Register domain: `sms.gaybeckstarkids.com`
2. Point to GitHub Pages:
   - Go to DNS settings
   - Add CNAME record:
     - Name: `www`
     - Value: `ashgabb.github.io`
   - Add A records for root domain

3. In GitHub repository settings:
   - Add custom domain
   - Check "Enforce HTTPS"

---

## Version Control for Website

```bash
# Commit after changes
git add website/
git commit -m "update: Fix navigation links"

# Push to GitHub (auto-deploys to GitHub Pages)
git push origin main

# Create release tag
git tag -a v1.0 -m "Website v1.0 released"
git push origin v1.0
```

---

## Contact & Support

For deployment issues:
1. Check GitHub Actions for errors
2. Review this guide
3. Contact hosting provider support
4. Check browser developer console (F12)

---

**Last Updated**: December 10, 2025
**Status**: Ready for Deployment ✅
**Recommended**: GitHub Pages (easiest, free, automatic HTTPS)
