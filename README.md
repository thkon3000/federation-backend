\# Federation Management Backend Platform



This project is a backend platform designed for federations or nonprofit organizations that manage multiple member-based clubs or associations.



The platform acts as a \*\*centralized system of record\*\*, replacing fragmented Excel-based workflows while preserving the familiar way organizations already work.



It is built with \*\*FastAPI\*\*, \*\*PostgreSQL\*\*, and \*\*Microsoft Azure\*\*, with a strong focus on \*\*role-based access control\*\*, \*\*GDPR compliance\*\*, and \*\*cost-efficient cloud deployment\*\*.



---



\## 🎯 Purpose \& Philosophy



Many federations and nonprofit organizations rely heavily on Excel files to manage members, clubs, and historical data.  

This platform is designed to:



\- Centralize all data without changing existing workflows

\- Preserve historical records instead of overwriting or deleting them

\- Allow easy Excel uploads as a first-class feature

\- Provide full oversight to the federation while protecting club-level data

\- Be GDPR-compliant by design

\- Run entirely within \*\*Azure Nonprofit Sponsorship credits\*\*, with zero additional infrastructure cost



The goal is not to eliminate Excel, but to \*\*understand it and evolve it into a secure platform\*\*.



---



\## 👤 Roles \& Access Model



\### Federation (Central Administrator)



The federation has \*\*full access\*\* to the platform and all data.



Capabilities include:

\- View and manage all clubs

\- View all members across all clubs

\- Access all club-uploaded files

\- Export data for reporting or GDPR requests

\- Perform audits and maintain historical records



---



\### Clubs



Each club has access \*\*only to its own data\*\*.



Clubs can:

\- View and manage their own members

\- Upload Excel files to update member lists

\- Correct or enrich member information

\- Upload and manage club-related documents



Clubs \*\*cannot\*\*:

\- View data from other clubs

\- Access federation-level configuration

\- Modify system-wide structures



---



\## 👥 Member Management



\### Central Member Registry



The platform maintains a \*\*single, unified registry\*\* of all members who have ever been registered, regardless of:



\- Current activity status

\- Membership renewal

\- Club association changes



This mirrors real-world administrative needs and existing Excel practices.



---



\### Membership Status \& History



For each member, the system supports:

\- Historical registration data

\- Membership renewal status per year

\- Generation of yearly active-member lists

\- Long-term historical tracking



No data is silently deleted or overwritten.



---



\## 📊 Excel Upload (Core Feature)



Excel uploads are a \*\*core workflow\*\*, not an afterthought.



Clubs and the federation can:

\- Upload Excel files with member data

\- Have columns automatically recognized

\- Insert new members or update existing ones

\- Preserve historical records

\- Avoid accidental data loss



The guiding principle:

> \*“Upload Excel files the same way you always have — the system understands them.”\*



---



\## ☁️ Club File Storage (Mini Cloud)



Each club has its own isolated file storage area where it can upload documents such as:



\- Meeting minutes

\- Board decisions

\- Legal documents

\- Internal records



Features include:

\- Logical separation per club

\- Optional tagging (e.g. elections, legal, financial)

\- Federation-wide visibility across all club files



Effectively, each club gets a \*\*private cloud folder\*\*, while the federation retains full oversight.



---



\## 🔐 Security \& GDPR Compliance



The platform is designed with GDPR principles at its core:



\- Strict role-based access control

\- No data leakage between clubs

\- GDPR-compliant data export (per member)

\- Data deletion where legally required

\- Audit logs tracking who did what and when



Security is enforced at:

\- API level

\- Database access level

\- Cloud storage access level



---



\## 💾 Backups \& Data Integrity



The system supports:

\- Automated database backups

\- Secure storage backups

\- Historical change tracking

\- Recovery to previous states when required



The platform acts as a \*\*long-term memory\*\* for the federation.



---



\## ☁️ Cloud Infrastructure \& Cost Model



The entire platform runs on \*\*Microsoft Azure\*\*, using:



\- Azure Container Apps

\- Azure PostgreSQL Flexible Server

\- Azure Blob Storage



The architecture is intentionally designed to fit within \*\*Azure Nonprofit Sponsorship credits (~$2000/year)\*\*, ensuring:



\- No out-of-pocket infrastructure costs

\- Sustainable long-term operation

\- Cloud-native scalability without vendor sprawl



---



\## 🛠️ Tech Stack



\- \*\*Backend:\*\* FastAPI (Python)

\- \*\*Database:\*\* PostgreSQL

\- \*\*ORM:\*\* SQLAlchemy

\- \*\*File Storage:\*\* Azure Blob Storage

\- \*\*Containerization:\*\* Docker

\- \*\*Cloud Platform:\*\* Microsoft Azure

\- \*\*Deployment:\*\* Azure Container Apps

\- \*\*Authentication:\*\* Admin login (JWT planned)

\- \*\*Data Processing:\*\* Pandas (Excel parsing)



---



\## 🚧 Project Status \& Roadmap



Current state:

\- Core backend structure implemented

\- Member management and Excel upload functional

\- Club management and file storage implemented

\- Azure deployment completed



Planned next steps:

\- JWT-based authentication with user roles

\- Club-level user accounts

\- Full audit logging

\- Database migrations (Alembic)

\- GitHub → Azure CI/CD pipeline

\- API documentation and testing



---



\## 📌 Disclaimer



This repository represents a \*\*generic federation / nonprofit management platform\*\*.  

It is not tied to any specific organization and is designed to be adaptable to multiple real-world use cases.



