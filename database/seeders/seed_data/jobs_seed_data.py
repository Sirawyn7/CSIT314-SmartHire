

#Each employer in the seed data is assigned 2 jobs to list pulled from these tuple pairs
JOB_PAIRS = [
    (
        {"title": "Frontend Developer", "description": "Build and maintain responsive user interfaces using modern web technologies. Collaborate with designers and backend engineers to deliver high-quality features.", "required_education": "Bachelor", "required_skills": "HTML, CSS, JavaScript, React", "years_experience_required": 2, "work_mode": "Hybrid", "location": "Sydney"},
        {"title": "Backend Developer", "description": "Design and implement server-side logic, APIs, and database integrations. Ensure performance, reliability, and security of core services.", "required_education": "Bachelor", "required_skills": "Python, Flask, SQL, REST APIs", "years_experience_required": 3, "work_mode": "Remote", "location": "Sydney"},
    ),
    (
        {"title": "Data Analyst", "description": "Analyse large datasets to identify trends and provide actionable insights. Produce dashboards and reports for internal stakeholders.", "required_education": "Bachelor", "required_skills": "Python, SQL, Tableau, Excel", "years_experience_required": 2, "work_mode": "On-site", "location": "Melbourne"},
        {"title": "Data Engineer", "description": "Build and maintain scalable data pipelines and warehousing solutions. Work closely with analysts and scientists to ensure data availability.", "required_education": "Bachelor", "required_skills": "Python, SQL, Spark, Airflow", "years_experience_required": 3, "work_mode": "Hybrid", "location": "Melbourne"},
    ),
    (
        {"title": "DevOps Engineer", "description": "Manage CI/CD pipelines, cloud infrastructure, and deployment automation. Improve system reliability and development velocity.", "required_education": "Bachelor", "required_skills": "Docker, Kubernetes, AWS, Terraform", "years_experience_required": 4, "work_mode": "Remote", "location": "Brisbane"},
        {"title": "Site Reliability Engineer", "description": "Ensure platform uptime and performance through monitoring, alerting, and incident response. Drive reliability improvements across engineering teams.", "required_education": "Bachelor", "required_skills": "Linux, Python, Prometheus, Kubernetes", "years_experience_required": 4, "work_mode": "Hybrid", "location": "Brisbane"},
    ),
    (
        {"title": "Machine Learning Engineer", "description": "Develop, train, and deploy machine learning models to production. Work with data scientists to operationalise research outputs.", "required_education": "Master", "required_skills": "Python, TensorFlow, PyTorch, MLflow", "years_experience_required": 3, "work_mode": "Remote", "location": "Sydney"},
        {"title": "Data Scientist", "description": "Apply statistical and machine learning techniques to solve business problems. Communicate findings clearly to technical and non-technical audiences.", "required_education": "Master", "required_skills": "Python, R, scikit-learn, SQL", "years_experience_required": 2, "work_mode": "Hybrid", "location": "Sydney"},
    ),
    (
        {"title": "Product Manager", "description": "Define product vision and roadmap. Work cross-functionally with engineering, design, and business teams to deliver user value.", "required_education": "Bachelor", "required_skills": "Product strategy, Agile, Jira, Stakeholder management", "years_experience_required": 4, "work_mode": "On-site", "location": "Melbourne"},
        {"title": "Business Analyst", "description": "Gather and document business requirements. Bridge communication between technical teams and business stakeholders.", "required_education": "Bachelor", "required_skills": "Requirements analysis, SQL, Agile, Documentation", "years_experience_required": 2, "work_mode": "Hybrid", "location": "Melbourne"},
    ),
    (
        {"title": "UX Designer", "description": "Conduct user research and design intuitive interfaces. Produce wireframes, prototypes, and design specifications for engineering teams.", "required_education": "Bachelor", "required_skills": "Figma, User research, Wireframing, Prototyping", "years_experience_required": 2, "work_mode": "Hybrid", "location": "Perth"},
        {"title": "UI Developer", "description": "Implement pixel-perfect interfaces from design specifications. Ensure accessibility and cross-browser compatibility.", "required_education": "Bachelor", "required_skills": "HTML, CSS, JavaScript, Figma", "years_experience_required": 2, "work_mode": "Remote", "location": "Perth"},
    ),
    (
        {"title": "Cybersecurity Analyst", "description": "Monitor systems for threats, conduct vulnerability assessments, and respond to security incidents. Maintain compliance with security policies.", "required_education": "Bachelor", "required_skills": "Network security, SIEM, Penetration testing, Python", "years_experience_required": 3, "work_mode": "On-site", "location": "Canberra"},
        {"title": "Security Engineer", "description": "Design and implement security controls across infrastructure and applications. Drive security best practices across engineering.", "required_education": "Bachelor", "required_skills": "Cloud security, IAM, Python, Compliance", "years_experience_required": 4, "work_mode": "Hybrid", "location": "Canberra"},
    ),
    (
        {"title": "Cloud Architect", "description": "Design and oversee cloud infrastructure strategy. Lead migration projects and ensure systems are scalable, secure, and cost-effective.", "required_education": "Master", "required_skills": "AWS, Azure, Terraform, Networking", "years_experience_required": 6, "work_mode": "Remote", "location": "Sydney"},
        {"title": "Cloud Engineer", "description": "Implement and manage cloud infrastructure. Automate provisioning and support development teams with platform tooling.", "required_education": "Bachelor", "required_skills": "AWS, Terraform, Linux, Python", "years_experience_required": 3, "work_mode": "Hybrid", "location": "Sydney"},
    ),
    (
        {"title": "Mobile Developer (iOS)", "description": "Build and maintain iOS applications. Work with product and design teams to deliver smooth, native mobile experiences.", "required_education": "Bachelor", "required_skills": "Swift, Xcode, iOS SDK, REST APIs", "years_experience_required": 2, "work_mode": "Hybrid", "location": "Melbourne"},
        {"title": "Mobile Developer (Android)", "description": "Develop and maintain Android applications. Ensure performance and reliability across a range of devices and OS versions.", "required_education": "Bachelor", "required_skills": "Kotlin, Android SDK, Jetpack, REST APIs", "years_experience_required": 2, "work_mode": "Hybrid", "location": "Melbourne"},
    ),
    (
        {"title": "Full Stack Developer", "description": "Build end-to-end features across frontend and backend systems. Contribute to architecture decisions and code reviews.", "required_education": "Bachelor", "required_skills": "Python, JavaScript, React, SQL", "years_experience_required": 3, "work_mode": "Remote", "location": "Adelaide"},
        {"title": "Software Engineer", "description": "Design, develop, and maintain software systems. Participate in agile ceremonies and contribute to a collaborative engineering culture.", "required_education": "Bachelor", "required_skills": "Python, Java, SQL, Git", "years_experience_required": 2, "work_mode": "Hybrid", "location": "Adelaide"},
    ),
    (
        {"title": "QA Engineer", "description": "Design and execute test plans for web and backend systems. Identify, document, and track defects through to resolution.", "required_education": "Bachelor", "required_skills": "Selenium, Python, Test planning, JIRA", "years_experience_required": 2, "work_mode": "Hybrid", "location": "Sydney"},
        {"title": "Automation Test Engineer", "description": "Build and maintain automated test suites for regression and integration coverage. Work with engineers to improve overall test quality.", "required_education": "Bachelor", "required_skills": "Selenium, Pytest, CI/CD, Python", "years_experience_required": 3, "work_mode": "Remote", "location": "Sydney"},
    ),
    (
        {"title": "Technical Writer", "description": "Produce clear, accurate technical documentation for developer and end-user audiences. Work with engineers to document APIs, processes, and systems.", "required_education": "Bachelor", "required_skills": "Technical writing, Markdown, API documentation, Git", "years_experience_required": 2, "work_mode": "Remote", "location": "Brisbane"},
        {"title": "Developer Advocate", "description": "Represent the developer community internally and externally. Create tutorials, write documentation, and present at events.", "required_education": "Bachelor", "required_skills": "Public speaking, Technical writing, Python, REST APIs", "years_experience_required": 3, "work_mode": "Hybrid", "location": "Brisbane"},
    ),
    (
        {"title": "Database Administrator", "description": "Manage and optimise relational and non-relational databases. Ensure data integrity, availability, and performance.", "required_education": "Bachelor", "required_skills": "SQL, PostgreSQL, MySQL, Performance tuning", "years_experience_required": 4, "work_mode": "On-site", "location": "Perth"},
        {"title": "Database Developer", "description": "Design database schemas and write complex queries and stored procedures. Support application teams with data access needs.", "required_education": "Bachelor", "required_skills": "SQL, PostgreSQL, Schema design, Python", "years_experience_required": 2, "work_mode": "Hybrid", "location": "Perth"},
    ),
    (
        {"title": "Scrum Master", "description": "Facilitate agile ceremonies and remove blockers for engineering teams. Coach teams on agile practices and continuous improvement.", "required_education": "Bachelor", "required_skills": "Scrum, Agile coaching, Jira, Facilitation", "years_experience_required": 3, "work_mode": "Hybrid", "location": "Melbourne"},
        {"title": "Agile Delivery Lead", "description": "Lead delivery across multiple agile teams. Own programme-level planning, dependency management, and stakeholder reporting.", "required_education": "Bachelor", "required_skills": "Agile, Programme management, Jira, Stakeholder management", "years_experience_required": 5, "work_mode": "On-site", "location": "Melbourne"},
    ),
    (
        {"title": "IT Support Specialist", "description": "Provide first and second-line technical support to staff. Troubleshoot hardware, software, and network issues promptly.", "required_education": "High School", "required_skills": "Windows, MacOS, Networking, Ticketing systems", "years_experience_required": 1, "work_mode": "On-site", "location": "Canberra"},
        {"title": "Systems Administrator", "description": "Manage on-premise and cloud infrastructure. Handle user provisioning, patching, backups, and system monitoring.", "required_education": "Bachelor", "required_skills": "Linux, Windows Server, Active Directory, Networking", "years_experience_required": 3, "work_mode": "On-site", "location": "Canberra"},
    ),
    (
        {"title": "Research Engineer", "description": "Investigate and prototype new technologies to address engineering challenges. Publish findings and collaborate with product teams on adoption.", "required_education": "Master", "required_skills": "Python, Research methodology, Machine learning, Academic writing", "years_experience_required": 3, "work_mode": "Hybrid", "location": "Sydney"},
        {"title": "Applied Scientist", "description": "Apply cutting-edge research to real-world product problems. Bridge the gap between research publications and production implementation.", "required_education": "PhD", "required_skills": "Python, Statistics, NLP, Deep learning", "years_experience_required": 4, "work_mode": "Remote", "location": "Sydney"},
    ),
    (
        {"title": "Network Engineer", "description": "Design, implement, and maintain network infrastructure. Diagnose and resolve connectivity and performance issues.", "required_education": "Bachelor", "required_skills": "Cisco, Networking protocols, Firewalls, Linux", "years_experience_required": 3, "work_mode": "On-site", "location": "Adelaide"},
        {"title": "Telecommunications Analyst", "description": "Analyse and optimise telecommunications infrastructure and services. Support procurement and vendor management activities.", "required_education": "Bachelor", "required_skills": "Telecommunications, Network analysis, Vendor management, Excel", "years_experience_required": 2, "work_mode": "Hybrid", "location": "Adelaide"},
    ),
    (
        {"title": "ERP Consultant", "description": "Implement and configure ERP systems for clients. Gather requirements, lead training sessions, and provide post-go-live support.", "required_education": "Bachelor", "required_skills": "SAP, ERP implementation, Business analysis, SQL", "years_experience_required": 4, "work_mode": "Hybrid", "location": "Melbourne"},
        {"title": "CRM Developer", "description": "Develop and customise CRM solutions to support sales and customer service teams. Integrate CRM with other business systems.", "required_education": "Bachelor", "required_skills": "Salesforce, CRM customisation, Apex, REST APIs", "years_experience_required": 3, "work_mode": "Remote", "location": "Melbourne"},
    ),
    (
        {"title": "Embedded Systems Engineer", "description": "Design and develop firmware and low-level software for embedded hardware platforms. Work closely with hardware engineers on integrated solutions.", "required_education": "Bachelor", "required_skills": "C, C++, RTOS, Hardware debugging", "years_experience_required": 3, "work_mode": "On-site", "location": "Brisbane"},
        {"title": "Hardware Engineer", "description": "Design, prototype, and test electronic hardware. Collaborate with firmware and software teams to deliver complete product solutions.", "required_education": "Bachelor", "required_skills": "Circuit design, PCB layout, Altium, C", "years_experience_required": 3, "work_mode": "On-site", "location": "Brisbane"},
    ),
    (
        {"title": "Graduate Software Engineer", "description": "Join a structured graduate programme and contribute to real engineering projects from day one. Mentored by senior engineers across multiple teams.", "required_education": "Bachelor", "required_skills": "Python, Java, Git, Problem solving", "years_experience_required": 0, "work_mode": "Hybrid", "location": "Sydney"},
        {"title": "Junior Data Analyst", "description": "Support the analytics team with data cleaning, reporting, and visualisation tasks. A great entry point into a data-driven organisation.", "required_education": "Bachelor", "required_skills": "SQL, Excel, Python, Data visualisation", "years_experience_required": 0, "work_mode": "Hybrid", "location": "Sydney"},
    ),
]