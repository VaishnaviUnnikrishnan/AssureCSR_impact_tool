CSR Implementation and Impact Measuring Platform

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

![Screenshot 2025-03-15 175748](https://github.com/user-attachments/assets/00b027d0-b688-4e9c-bc9b-f49a1f1312ce)

![Screenshot 2025-03-15 175800](https://github.com/user-attachments/assets/3a40512b-85c1-4b00-9862-931011e8689c)

![Screenshot 2025-03-15 175814](https://github.com/user-attachments/assets/c50de386-6dfb-41f7-b783-7bd08e16fb9d)

![Screenshot 2025-03-15 180056](https://github.com/user-attachments/assets/5a03864e-bf97-435f-8af9-e9d6dc1de3ff)

![Screenshot 2025-03-15 175945](https://github.com/user-attachments/assets/97910e3a-a96d-4aff-8727-5f48aa89234d)





