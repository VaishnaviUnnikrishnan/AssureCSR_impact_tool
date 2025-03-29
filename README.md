# CSR Implementation and Impact Measuring Platform

Overview
This is a Corporate Social Responsibility (CSR) measuring and implementation tool designed to connect companies, volunteers, and users/commoners to effectively identify social issues, allocate CSR budgets, and track project impact.

Features
1. User (Commoner)
- Logs in and specifies their **location**.
- Raises an **issue** that needs attention.
- Uploads **proofs** (images, documents, complaint letters, etc.) for verification using an ML model.
- Once verified, the issue is added to the *CSR project list* for companies to consider.

2. Company Employee
- Logs in and **registers their company**.
- Provides **company revenue**, based on which the CSR budget is calculated (following Indian CSR rules).
- Specifies **location** and budget allocation.
- Can implement CSR projects in **two ways**:
  1. **Addressing issues raised by users** in the company’s region.
  2. **Initiating internal CSR projects** (e.g., eco-friendly raw materials, employee education support, etc.).
- Uses a **chatbot (under development)** to get tailored project ideas.
- **Predicts the impact** of a CSR project using an ML model trained on past projects.
- Views a **dashboard of impact**, displaying project effectiveness using visual charts and maps.
- If they decide to proceed, a **budget breakdown, timeline, and assigned volunteer contact** are generated.

### 3. Volunteer
- Logs in and **selects the project** they are assigned to.
- Uploads **proofs (images, documents, etc.)** to verify project progress.
- Proofs are validated using an ML model (ideas needed for verification).
- Views a **dashboard** comparing actual impact vs. predicted impact.
- Once verified, the company employee sees the project in the **completed projects list** and can access the final dashboard.

Machine Learning Models Used
1. **Verification of Proofs (User & Volunteer)**
   - Image recognition models for validating photo authenticity.
   - OCR-based document verification for complaint letters and documents.
   - Fake detection techniques to prevent fraudulent claims.
2. **Impact Prediction Model (Company Employee)**
   - A model trained on previous CSR projects to predict the expected impact.
   - Provides insights through charts and maps on the project’s potential.

Tech Stack
- **Backend:** Python (Flask)
- **Frontend:** HTML,CSS,Folium
- **Machine Learning:** TensorFlow/PyTorch, OpenCV, NLP 



Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/VaishnaviUnnikrishnan/AssureCSR_impact_tool.git
   cd AssureCSR_impact_tool
   ```
2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # Mac/Linux
   venv\Scripts\activate  # Windows
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Run the application:
   ```sh
   python app.py
   

Future Enhancements
- Improve chatbot accuracy for CSR project suggestions.
- Implement blockchain for project transparency.
- AI-based fraud detection for proof verification.

License
This project is licensed under the MIT License.

Contact
For any queries, reach out to v.ukrishnan8@gmail.com.

![Screenshot 2025-03-15 175748](https://github.com/user-attachments/assets/58c23f62-6814-4ef7-ac29-5123402ac6fc)

![Screenshot 2025-03-15 180056](https://github.com/user-attachments/assets/5b35b49d-78f1-4359-86b3-6f73a6a39324)

![Screenshot 2025-03-15 180116](https://github.com/user-attachments/assets/785cd525-022a-47e2-a01b-5fb27c26bcc8)

![Screenshot 2025-03-15 175845](https://github.com/user-attachments/assets/93d32a19-51e3-41d5-9a77-5a5a8545323a)

![Screenshot 2025-03-15 175945](https://github.com/user-attachments/assets/1d71f335-dff6-43eb-8214-a2ec72308012)


