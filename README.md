🛡️ ScamShield — Check Before You Click



AI-powered scam awareness for suspicious messages, emails, and URLs — understand the warning signs before you take action.













🎯 What is ScamShield?



ScamShield is a cybersecurity-focused web application that uses Google Gemini to analyze suspicious SMS messages, emails, and URLs.



Instead of simply saying "Scam" or "Safe", ScamShield provides an explainable result containing:



📊 A 0–100 risk score



🚦 A LOW / MEDIUM / HIGH risk level



🏷️ A Scam / Suspicious / Likely Legitimate classification



⚠️ The specific warning signs detected



💡 A short explanation of the assessment



🛡️ Practical safe actions the user can take



The core workflow



Paste → Analyze → Understand → Act Safely



The goal is to make scam detection easier to understand, especially for users who may recognize that a message "feels wrong" but do not know exactly why.



✨ Why ScamShield?



Scam messages commonly use social-engineering techniques such as:



Urgency and time pressure



Threats of account suspension



Prize or reward claims



Requests for OTPs or sensitive information



Requests for payments



Suspicious or deceptive links



Impersonation-style wording



ScamShield turns these signals into a simple security report that a user can understand before clicking, paying, or sharing sensitive information.



🖥️ Product Preview



Live Demo: Add your deployed Streamlit URL here after deployment.



┌─────────────────────────────────────────────────────────────────────┐

│ 🛡️ ScamShield                                      AI SECURITY ENGINE│

├─────────────────────────────────────────────────────────────────────┤

│                                                                     │

│                    CHECK BEFORE YOU CLICK                           │

│                                                                     │

│  ┌──────────────────────────┐    ┌────────────────────────────────┐ │

│  │ MESSAGE TO ANALYZE       │    │ THREAT ANALYSIS                │ │

│  │                          │    │                                │ │

│  │ Paste a suspicious       │    │ HIGH RISK                      │ │

│  │ SMS, email, or URL...    │    │ 95 / 100                       │ │

│  │                          │    │                                │ │

│  │ \[ Analyze Message ]      │    │ ⚠ Urgency                      │ │

│  │                          │    │ ⚠ OTP request                  │ │

│  └──────────────────────────┘    │ ⚠ Suspicious link              │ │

│                                  │                                │ │

│                                  │ 🛡️ Don't click • Don't pay      │ │

│                                  └────────────────────────────────┘ │

└─────────────────────────────────────────────────────────────────────┘



🎬 Demo scenarios



The application includes three ready-to-test examples:



Scenario



Purpose



🚨 Scam SMS



Tests urgency, account threats, OTP requests, and suspicious links



✅ Legitimate Message



Demonstrates that not every message is classified as a scam



🔗 Suspicious URL



Tests URL-focused threat signals



Screenshots / GIF: Add your final deployed-app screenshot or demo GIF here when available. Keeping visual evidence in the README is recommended for hackathon judging and portfolio use.



🧠 How the System Works



&#x20;                   ┌─────────────────────┐

&#x20;                   │       USER          │

&#x20;                   │ SMS / Email / URL   │

&#x20;                   └──────────┬──────────┘

&#x20;                              │

&#x20;                              ▼

&#x20;                   ┌─────────────────────┐

&#x20;                   │   STREAMLIT UI      │

&#x20;                   │ Input + Dashboard   │

&#x20;                   └──────────┬──────────┘

&#x20;                              │

&#x20;                              ▼

&#x20;                   ┌─────────────────────┐

&#x20;                   │    ANALYZER.PY      │

&#x20;                   │ Prompt + API call   │

&#x20;                   └──────────┬──────────┘

&#x20;                              │

&#x20;                              ▼

&#x20;                   ┌─────────────────────┐

&#x20;                   │    GOOGLE GEMINI    │

&#x20;                   │ AI threat analysis  │

&#x20;                   └──────────┬──────────┘

&#x20;                              │

&#x20;                        Structured JSON

&#x20;                              │

&#x20;                              ▼

&#x20;            ┌─────────────────────────────────────┐

&#x20;            │          SCAMSHIELD REPORT          │

&#x20;            ├─────────────────────────────────────┤

&#x20;            │ Risk Score                          │

&#x20;            │ Risk Level                          │

&#x20;            │ Classification                      │

&#x20;            │ Warning Signs                       │

&#x20;            │ Explanation                         │

&#x20;            │ Recommended Safe Actions            │

&#x20;            └─────────────────────────────────────┘



🔄 Analysis Flow



The user pastes a suspicious message, email, or URL.



ScamShield sends the content to the analysis layer.



The analysis layer asks Google Gemini to return a structured JSON assessment.



The application parses the result.



The dashboard converts the result into an easy-to-read security report.



The user receives warning signs and safer next steps.



🧩 Core Features



1\. 🤖 AI-Powered Analysis



ScamShield uses Google Gemini to interpret the submitted content and identify potential scam/social-engineering indicators.



2\. 📊 Risk Scoring



Every analysis produces a numeric risk score from 0 to 100.



The application also maps the result to:



LOW



MEDIUM



HIGH



3\. 🏷️ Explainable Classification



The model returns one of:



Scam



Suspicious



Likely Legitimate



The classification is accompanied by supporting warning signs rather than being presented as an unexplained verdict.



4\. ⚠️ Warning Signs



The dashboard highlights concise reasons supported by the submitted content.



Examples include:



Unusual urgency



Sensitive-information request



Payment request



Suspicious link



Threatening account language



5\. 🛡️ Safe Actions



The application provides practical safety guidance such as:



Do not click unknown links



Do not share OTPs or passwords



Do not send money based only on the message



Verify through the organization's official app or website



6\. 🧪 Built-in Test Scenarios



Users can quickly load predefined examples for:



A high-risk scam



A legitimate-looking notification



A suspicious URL



7\. 🌙 Cybersecurity Dashboard



The Streamlit interface uses a custom dark cybersecurity-style dashboard with:



Threat-analysis panel



Risk score visualization



Warning-sign cards



Recommended-action cards



Scan metadata



Session scan statistics



Responsive styling



🛠️ Technology Stack



Layer



Technology



Purpose



UI



Streamlit



Interactive web application



Language



Python



Application and analysis logic



AI



Google Gemini



Message threat analysis



SDK



google-genai



Gemini API integration



Configuration



python-dotenv



Secure local environment configuration



Styling



HTML + CSS



Custom cybersecurity dashboard



No database required



The current MVP does not require a database or external application server. Analysis is performed through the Streamlit application and Gemini API.



📁 Project Structure



ScamShield/

│

├── app.py                  # Main Streamlit application

├── analyzer.py             # Gemini analysis engine

├── test\_gemini.py          # Gemini connection test

├── requirements.txt        # Python dependencies

├── README.md               # Project documentation

├── .gitignore              # Excludes secrets and local files

├── .env                    # Local Gemini API key (NOT committed)

└── venv/                   # Local virtual environment (NOT committed)



⚙️ Developer Setup



Prerequisites



Install:



Python 3.10 or newer



A Google Gemini API key



Git



A modern web browser



The project was developed and tested with:



Python 3.10+

Streamlit 1.64.0

google-genai 2.24.0

python-dotenv 1.2.3



1\. Clone the repository



git clone YOUR\_GITHUB\_REPOSITORY\_URL

cd ScamShield



Replace YOUR\_GITHUB\_REPOSITORY\_URL with the actual GitHub repository URL.



2\. Create a virtual environment



Windows PowerShell



python -m venv venv

.\\venv\\Scripts\\Activate.ps1



macOS / Linux



python3 -m venv venv

source venv/bin/activate



3\. Install dependencies



pip install -r requirements.txt



Expected dependencies:



streamlit==1.64.0

python-dotenv==1.2.3

google-genai==2.24.0



4\. Configure the Gemini API key



Create a file named .env in the project root:



GEMINI\_API\_KEY=YOUR\_GEMINI\_API\_KEY



The application reads the key through python-dotenv.



🔐 Important



Never commit your real API key to GitHub.



The repository should contain:



.env



in .gitignore, while the repository should not contain the actual .env file.



5\. Test the Gemini connection



Run:



python test\_gemini.py



A successful connection should report:



ScamShield Gemini connection successful.



6\. Launch ScamShield



streamlit run app.py



Streamlit will provide a local URL, normally similar to:



http://localhost:8501



Open that address in your browser.



🧪 Testing Payloads



These examples can be copied directly into ScamShield.



🚨 Test 1 — High-Risk Scam



URGENT! Your bank account will be blocked today. Verify your account immediately by clicking this link and entering your OTP: http://example.com



Expected signals



The application should identify signals such as:



Urgency



Account-blocking threat



OTP request



Suspicious/external link



The exact AI score may vary because the analysis is generated dynamically.



✅ Test 2 — Likely Legitimate



Your Amazon order #402-7812345-6789012 has been shipped. It will arrive on September 22. Track your package through the Amazon app.



Purpose



This test demonstrates that ScamShield is not designed to classify every message as a scam.



A legitimate-looking message should generally receive a lower risk assessment than the scam example.



🔗 Test 3 — Suspicious URL



http://secure-bank-login.example.com/verify



Expected signals



Possible indicators include:



Deceptive-looking domain



Generic verification path



Unencrypted HTTP



Bank-login impersonation pattern



Again, the AI-generated score may vary between requests.



🔐 Security \& Privacy



ScamShield follows a simple principle:



Keep secrets out of source code.



The Gemini API key is loaded from the environment:



from dotenv import load\_dotenv

import os



load\_dotenv()



api\_key = os.getenv("GEMINI\_API\_KEY")



The .gitignore excludes:



.env

venv/

\_\_pycache\_\_/



API key safety checklist



Before pushing to GitHub:



\[ ] .env exists locally

\[ ] .env is listed in .gitignore

\[ ] No API key is hard-coded in Python files

\[ ] No API key appears in README.md

\[ ] No API key appears in screenshots

\[ ] git status does not show .env



🧪 Current MVP Scope



ScamShield currently focuses on text-based analysis of:



SMS messages



Email-like messages



Suspicious URLs



The current project intentionally keeps the core workflow simple:



INPUT

&#x20; ↓

AI ANALYSIS

&#x20; ↓

EXPLANATION

&#x20; ↓

SAFE ACTIONS



This makes the application easy to demonstrate while leaving room for additional cybersecurity integrations.



🚀 Future Roadmap



Potential future enhancements include:



🔍 Advanced Detection



URL reputation checks



Domain-age and registration checks



Email-header analysis



QR-code analysis



Known phishing-domain intelligence



Threat-intelligence integrations



🖼️ Multimodal Analysis



Screenshot upload



Image-based scam-message analysis



OCR for screenshots



Detection of suspicious QR codes



🌍 Accessibility



Multi-language support



Simplified explanations for non-technical users



Voice input/output



📈 Product Features



Persistent scan history



Exportable security reports



User accounts



Analytics dashboard



Deployment-ready secret management



🤝 Contributing



Contributions are welcome.



Suggested workflow



Fork the repository.



Create a feature branch:



git checkout -b feature/your-feature



Make your changes.



Test the application locally.



Commit your changes:



git add .

git commit -m "Add your feature"



Push the branch:



git push origin feature/your-feature



Open a Pull Request.



Contribution guidelines



When contributing:



Keep changes focused.



Do not commit API keys or secrets.



Preserve the existing application workflow.



Test changes before submitting a pull request.



Update the README when adding major functionality.



🐛 Reporting Issues



When reporting a bug, include:



Operating system



Python version



Streamlit version



Steps to reproduce



Expected behavior



Actual behavior



Relevant error message



Do not include your Gemini API key or other private credentials in an issue.



📄 License



License: Not yet specified.



This project is currently a hackathon project. A formal open-source license can be added before public redistribution.



If the project is later released under MIT, Apache-2.0, or another license, update this section and add the corresponding LICENSE file.



⚠️ Disclaimer



ScamShield is an AI-assisted cybersecurity awareness tool.



It does not guarantee that a message is safe, malicious, fraudulent, or legitimate. AI-generated analysis can be incorrect, incomplete, or uncertain.



For sensitive situations, verify requests independently through official channels.



Never share:



Passwords



OTPs



PINs



Recovery codes



Banking credentials



Private keys



based solely on an AI-generated result.



🏆 Hackathon Project



Project: ScamShield — Check Before You Click



Category: Open Innovation / Cybersecurity



Core idea: Use explainable AI to help people understand suspicious digital messages before they click, pay, or share sensitive information.



Project value proposition



Traditional approach:

"Is this a scam?"



ScamShield approach:

"Here is the risk,

here are the signals,

here is why they matter,

and here is what you can safely do next."



👨‍💻 Author



Subrat Gouda



Built as an independent hackathon project.



⭐ ScamShield



Check before you click. Understand before you act. Stay safer online. 🛡️

