<p align="center">
  <img src="./img.png" alt="Project Banner" width="100%">
</p>

# Community Platform 🎯

## Basic Details

### Team Name: Dilba

### Team Members
- Member 1: [Your Name] - [Your College]
- Member 2: [Team Member] - [College]

### Hosted Project Link
`localhost:5000` (Local Development)

### Project Description
A comprehensive community platform that allows residents to connect, share information, and support each other. Users can post lost and found items, file complaints, and ask for help within their community.

### The Problem statement
Community members often struggle to report lost items, file complaints effectively, and seek help from their neighbors due to lack of a centralized platform.

### The Solution
We've built an integrated web application that provides a dedicated space for community members to post lost/found items, file complaints, and ask for help or share resources within their neighborhood.

---

## Technical Details

### Technologies/Components Used

**For Software:**
- Languages used: Python, HTML, CSS, JavaScript
- Frameworks used: Flask 2.3+
- Libraries used: 
  - werkzeug (password hashing and file handling)
  - Jinja2 (template rendering)
  - sqlite3 (database)
- Tools used: VS Code, Git, SQLite

**Database:**
- SQLite3 (community.db)
- Tables: users, lostfound, complaint, help

---

## Features

List the key features of your project:
- **User Authentication**: Secure sign-up and login system with password hashing
- **Lost & Found**: Post and view lost/found items with images and detailed descriptions
- **Complaints Management**: File and view community complaints with attachment support
- **Help & Sharing**: Request help or share resources with the community
- **Responsive Design**: Works seamlessly across different devices
- **User Sessions**: Secure session management for logged-in users
- **Image Upload**: Support for image uploads with secure file handling

---

## Implementation

### For Software:

#### Installation
```bash
# 1. Clone the repository
git clone https://github.com/yourusername/dilba-tinkherhack4.0.git
cd dilba-tinkherhack4.0

# 2. Create a virtual environment (recommended)
python -m venv venv

# 3. Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install Flask werkzeug
```

#### Run
```bash
# Start the Flask application
python app.py

# The application will be available at:
# http://localhost:5000
```

#### Database Initialization
The database is automatically created on first run. The application creates the following tables:
- **users**: Stores user account information with hashed passwords
- **lostfound**: Lost and found item postings
- **complaint**: Community complaints
- **help**: Help requests and resource sharing

---

## Project Documentation

### For Software:

#### Screenshots (Add at least 3)

![Landing Page](docs/landing-page.png)
*Landing page with Login and Sign Up options*

![Dashboard](docs/dashboard.png)
*Home page showing all available services*

![Lost & Found](docs/lostfound.png)
*Lost & Found section with item postings and filters*

#### Diagrams

**System Architecture:**

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │ HTTP/HTTPS
       ▼
┌─────────────────────┐
│   Flask App         │
│  - Routes           │
│  - Authentication   │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│   SQLite Database   │
│  - Users            │
│  - Items            │
│  - Complaints       │
│  - Help Requests    │
└─────────────────────┘
```

**Database Schema:**

Users Table:
```
┌──────────────┬─────────────┐
│ id (PK)      │ INTEGER     │
│ username     │ TEXT UNIQUE │
│ email        │ TEXT UNIQUE │
│ password     │ TEXT        │
└──────────────┴─────────────┘
```

Lost & Found Table:
```
┌──────────────┬─────────┐
│ id (PK)      │ INTEGER │
│ name         │ TEXT    │
│ category     │ TEXT    │
│ type         │ TEXT    │
│ item         │ TEXT    │
│ description  │ TEXT    │
│ image        │ TEXT    │
└──────────────┴─────────┘
```

**Application Workflow:**

```
START
  │
  ├─► Landing Page (/)
  │     ├─► Login (/login)
  │     │    └─► Dashboard (/home)
  │     │
  │     └─► Sign Up (/signup)
  │          └─► Create Account
  │               └─► Login (/login)
  │
  ├─► Authenticated User
  │     ├─► Lost & Found (/lostfound)
  │     ├─► Complaints (/complaint)
  │     └─► Help & Sharing (/help)
  │
  └─► Logout (/logout)
       └─► Landing Page (/)
```

---

## Additional Documentation

### API Documentation

**Base URL:** `http://localhost:5000`

##### Endpoints

**GET /**
- **Description:** Landing page with login and signup options
- **Authentication:** Not required
- **Response:** Renders index.html

**POST /login**
- **Description:** Authenticate user with credentials
- **Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```
- **Response:**
```json
{
  "status": "success",
  "message": "Login successful!"
}
```
- **Error Responses:**
  - Invalid credentials: 401 Unauthorized
  - Missing fields: 400 Bad Request

**POST /signup**
- **Description:** Create a new user account
- **Request Body:**
```json
{
  "username": "string",
  "email": "string",
  "password": "string",
  "confirm_password": "string"
}
```
- **Validation Rules:**
  - Password minimum length: 6 characters
  - Passwords must match
  - Username and email must be unique
- **Response:**
```json
{
  "status": "success",
  "message": "Account created! Please login."
}
```
- **Error Responses:**
  - Username exists: 409 Conflict
  - Email exists: 409 Conflict
  - Passwords don't match: 400 Bad Request

**GET /home**
- **Description:** User dashboard (requires authentication)
- **Authentication:** Required (session['username'])
- **Response:** Renders home.html with username

**GET /logout**
- **Description:** End user session
- **Authentication:** Required
- **Response:** Redirects to landing page

**GET/POST /lostfound**
- **Description:** View and post lost/found items
- **Authentication:** Required
- **POST Parameters:**
  - name (string): Your name
  - category (string): School, College, Office, Hostel, Apartment
  - type_item (string): Lost or Found
  - item (string): Item name
  - description (string): Item description
  - image (file): Optional image upload
- **Response:** Renders lostfound.html with all items

**GET/POST /complaint**
- **Description:** View and submit complaints
- **Authentication:** Required
- **POST Parameters:**
  - name (string): Your name
  - issue (string): Complaint description
  - image (file): Optional image upload
- **Response:** Renders complaint.html with all complaints

**GET/POST /help**
- **Description:** View and post help requests/resources
- **Authentication:** Required
- **POST Parameters:**
  - name (string): Your name
  - help_text (string): Message or request
  - share_file (file): Optional file attachment
- **Response:** Renders help.html with all messages

---

## Project Demo

### Features Demo

**User Registration & Login:**
- Simple signup process with email validation
- Secure password hashing using werkzeug
- Session-based authentication

**Lost & Found Management:**
- Post items with category, type (Lost/Found), description
- Upload images for better identification
- Browse all community postings

**Community Complaints:**
- File complaints with detailed descriptions
- Attach supporting images/evidence
- Track all reported issues

**Help & Resource Sharing:**
- Request help from community members
- Share useful resources and files
- Community support system

### Video
[Add your project demo video link here]

*Walkthrough of the application from signup to using all features*

---

## AI Tools Used (Optional - For Transparency Bonus)

If you used AI tools during development, document them here for transparency:

**Tool Used:** GitHub Copilot / Claude / ChatGPT

**Purpose:** Code generation and assistance
- Generated Flask route structure and boilerplate
- Password hashing implementation
- SQL query optimization
- HTML/CSS template generation
- Bug debugging and fixes

**Key Prompts Used:**
- "Create a Flask authentication system with password hashing"
- "Generate HTML templates for a community platform"
- "Fix the sqlite3 table schema error"
- "Create CSS styling for a responsive web application"

**Percentage of AI-generated code:** ~30% (boilerplate and templates)

**Human Contributions:**
- Overall application architecture and planning
- Database schema design
- Feature implementation logic
- Integration and testing
- Bug fixes and optimization
- Project documentation

*Note: Proper documentation of AI usage demonstrates transparency!*

---

## Team Contributions

- **[Your Name]**: Full-stack development, authentication system, database design
- **[Team Member 2]**: Frontend design, HTML/CSS styling, template creation
- **[Team Member 3]**: Testing, documentation, deployment setup

---

## Future Enhancements

- [ ] Email notifications for lost item matches
- [ ] User profile pages with avatar support
- [ ] Real-time chat between users
- [ ] Map integration for location-based posts
- [ ] Mobile app version
- [ ] Advanced search and filtering
- [ ] Admin dashboard for moderation
- [ ] Payment integration for services
- [ ] Rating and review system
- [ ] Export data to CSV/PDF

---

## Troubleshooting

### Common Issues

**Issue: "ModuleNotFoundError: No module named 'flask'"**
- Solution: Install Flask with `pip install Flask`

**Issue: "Database locked" error**
- Solution: Ensure only one instance of the app is running

**Issue: "TemplateNotFound: [filename]"**
- Solution: Ensure all HTML files are in the `templates/` directory

**Issue: "Password incorrect" after signup**
- Solution: Make sure you're using the correct password you entered during signup

**Issue: Images not uploading**
- Solution: Check that `static/uploads/` directory exists and has write permissions

---

## Support & Contact

For questions or support, please contact:
- **Email:** [your-email@example.com]
- **GitHub Issues:** Create an issue on our GitHub repository
- **Discord:** [Your Discord server link if applicable]

---

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**You are free to:**
- Use this project for personal or commercial purposes
- Modify the code
- Distribute the project
- Use it privately

**Conditions:**
- You must include a copy of the license and copyright notice
- The software is provided as-is without warranty

---

Made with ❤️ at TinkerHub
