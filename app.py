from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_file
import os
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
import csv
import re
from collections import Counter
from textblob import TextBlob
import spacy
import matplotlib.pyplot as plt

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# Base directory for CSV data
base_dir = "D:/Temenos/data_tem"

# Global variable to store CSR amount
csr_data = {"amount": 0}

# Path to user_data.csv
user_data_path = "user_data.csv"

# Path to survey_results.xlsx
SURVEY_RESULTS_FILE = "survey_results.xlsx"




SURVEY_QUESTIONS = {
    "education": [
        "Number of Training Sessions Conducted",
        "Number of Participants Completing the Course",
        "Post-Training Assessment Score",
        "Improvement in Literacy Rate (%)",
        "Job Placements After Training",
        "Scholarships Awarded",
        "Dropout Rate Reduction (%)",
        "Number of Schools Upgraded",
        "Students Receiving Learning Materials",
        "Increase in Digital Literacy (%)",
        "Teachers Trained in New Teaching Methods",
        "Average Improvement in Test Scores (%)",
        "Number of Vocational Training Courses Offered",
        "Internships Secured Post-Training",
        "Reduction in Unemployment Rate (%)",
        "Hours of Online Learning Provided",
        "Number of Special Education Programs Launched",
        "Students Enrolled in STEM Programs",
        "Increase in Higher Education Enrollment (%)",
        "Number of Mobile Learning Units Deployed",
        "Books Distributed to Underprivileged Students",
        "Infrastructure Improvements in Schools"
    ],
    "healthcare": [
        "Number of Medical Camps Organized",
        "Patients Treated",
        "Vaccination Coverage (%)",
        "Reduction in Disease Incidents (%)",
        "Health Awareness Campaigns Conducted",
        "Number of Free Health Check-ups Provided",
        "Infant Mortality Rate Reduction (%)",
        "Maternal Health Improvements (%)",
        "Access to Clean Drinking Water Installations",
        "Number of Mental Health Support Programs",
        "Emergency Medical Services Provided",
        "Number of Hospitals Upgraded",
        "Reduction in Malnutrition Cases (%)",
        "Increase in Medical Staff Training Hours",
        "Surgeries Performed Successfully",
        "Increase in Health Insurance Coverage (%)",
        "Reduction in Hospital Readmission Rates (%)",
        "Expansion of Telemedicine Services",
        "Percentage Increase in Organ Donations",
        "Average Wait Time Reduction for Treatments",
        "Number of Ambulance Services Added",
        "Medical Equipment Distributed"
    ],
    "environment": [
        "Number of Trees Planted",
        "Air Quality Improvement (%)",
        "Water Conservation Efforts (liters)",
        "Reduction in Carbon Emission (%)",
        "Wildlife Protection Initiatives",
        "Green Energy Installations Completed",
        "Number of Plastic-Free Campaigns",
        "Reduction in Industrial Waste (%)",
        "Increase in Green Spaces (%)",
        "Public Transport Utilization Increase (%)",
        "Households Using Renewable Energy (%)",
        "Recycling Programs Implemented",
        "Reduction in Single-Use Plastic (%)",
        "Reduction in Water Pollution (%)",
        "Increase in Sustainable Farming (%)",
        "Reduction in Noise Pollution Levels (dB)",
        "Protected Land Areas Expanded (sq km)",
        "Increase in Biodiversity Index (%)",
        "Number of Eco-Friendly Infrastructure Projects",
        "Wildlife Population Increase (%)",
        "Community Engagements in Green Initiatives"
    ],
    "welfare": [
        "Number of Women Empowered",
        "Children Provided with Education",
        "Reduction in Domestic Violence Cases",
        "Skill Development Programs Conducted",
        "Increase in Female Employment (%)",
        "Number of Women Entrepreneurs Supported",
        "Legal Aid Cases Assisted",
        "Reduction in Child Marriage Cases (%)",
        "Increase in Women’s Health Awareness (%)",
        "Reduction in Gender Pay Gap (%)",
        "Number of Women in Leadership Positions",
        "Microfinance Loans Distributed",
        "Number of Child Nutrition Programs Launched",
        "Increase in Women Voter Participation (%)",
        "Reduction in Child Mortality Rate (%)",
        "Access to Sanitary Products Provided",
        "Reduction in Gender-Based Discrimination Cases",
        "Number of Self-Help Groups Formed",
        "Increase in Women's Literacy Rate (%)",
        "Child Welfare Centers Established",
        "Reduction in Homelessness for Women and Children"
    ],
    "rural": [
        "Number of Houses Built",
        "Increase in Literacy Rate (%)",
        "Access to Clean Drinking Water",
        "Income Growth in Rural Areas (%)",
        "Small Business Grants Provided",
        "New Road Infrastructure Built (km)",
        "Increase in Agricultural Productivity (%)",
        "Electrification of Villages (%)",
        "Increase in Rural Employment (%)",
        "Number of Healthcare Centers Established",
        "Reduction in Rural Poverty Rate (%)",
        "Access to Internet Facilities Expanded",
        "Increase in Rural Banking Services (%)",
        "Number of Farmers Trained in Modern Techniques",
        "Subsidies Provided for Farming Equipment",
        "Increase in Livestock Productivity (%)",
        "Reduction in Rural-to-Urban Migration (%)",
        "Number of Community Centers Built",
        "Small-Scale Industries Established",
        "Percentage of Villages with Waste Management Systems",
        "Increase in Access to Public Transport"
    ],
    "disaster": [
        "Relief Packages Distributed",
        "People Rescued",
        "Temporary Shelters Provided",
        "Funds Raised for Rehabilitation",
        "Infrastructure Rebuilt",
        "Number of Emergency Response Units Deployed",
        "Increase in Disaster Preparedness (%)",
        "Reduction in Response Time (minutes)",
        "Water and Food Supplies Distributed (kg)",
        "Percentage of Affected Population Assisted",
        "Mobile Health Clinics Deployed",
        "Damaged Roads Repaired (km)",
        "Schools Rebuilt After Disaster",
        "Communication Networks Restored",
        "Number of Disaster Training Workshops Conducted",
        "Evacuation Drills Conducted",
        "Flood Barriers Constructed (meters)",
        "Earthquake-Resistant Buildings Constructed",
        "Emergency Relief Workers Trained",
        "Increase in Community Resilience Index (%)",
        "Tents and Clothing Distributed"
    ]
}


# Function to search and aggregate metrics
def search_and_aggregate(category, subcategory, pincode, budget):
    file_path = os.path.join(base_dir, category, f"{subcategory}.csv")
    if not os.path.exists(file_path):
        return None, None

    df_sub = pd.read_csv(file_path)
    matching_instances = df_sub[(df_sub['Location (Pincode)'] == int(pincode)) & (df_sub['Budget'] == int(budget))]

    if not matching_instances.empty:
        metrics = matching_instances.select_dtypes(include=['number']).mean().to_dict()
        return metrics, generate_map(pincode)

    return None, None


# Function to generate map
def generate_map(pincode):
    map_center = [13.0827, 80.2707]  # Example: Chennai
    m = folium.Map(location=map_center, zoom_start=10)
    MarkerCluster().add_to(m)
    folium.Marker(map_center, popup=f"Pincode: {pincode}").add_to(m)

    map_path = "static/map.html"
    m.save(map_path)
    return map_path


# Route: Home Page
@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html")


# Route: User Options
@app.route("/user_options", methods=["GET", "POST"])
def user_options():
    if request.method == "POST":
        print(request.form)  # Debugging: Print the form data
        if "submit_info" in request.form:
            print("User Info button clicked")  # Debugging log
            return redirect(url_for("user"))
        elif "submit_feedback" in request.form:
            print("Feedback Form button clicked")  # Debugging log
            return redirect(url_for("feedback_form"))
    return render_template("user_options.html")


# Route: User Login
@app.route("/user_login", methods=["GET", "POST"])
def user():
    if request.method == "POST":
        # Handle user login logic (if needed)
        return redirect(url_for("user"))
    return render_template("user_login.html")





@app.route("/volunteer_login", methods=["GET", "POST"])
def volunteer_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        # Simple authentication (replace with proper logic)
        if username == "volunteer" and password == "password":
            session["logged_in"] = True
            return redirect(url_for("problem_selection"))
        else:
            return "Invalid credentials. Please try again."
    return render_template("volunteer_login.html")


@app.route("/problem_selection", methods=["GET", "POST"])
def problem_selection():
    if not session.get("logged_in"):
        return redirect(url_for("volunteer_login"))

    if request.method == "POST":
        project = request.form.get("project")
        return redirect(url_for("survey", project=project))  # Pass project as a query parameter
    return render_template("problem_selection.html")


# Route: Survey (Volunteer)
@app.route("/survey", methods=["GET", "POST"])
def survey():
    if not session.get("logged_in"):
        print("User not logged in. Redirecting to volunteer login.")
        return redirect(url_for("volunteer_login"))

    project = request.args.get("project")  # Retrieve project from query parameters
    questions = SURVEY_QUESTIONS.get(project, [])

    if request.method == "POST":
        data = request.form.to_dict()
        data["project"] = project

        df = pd.DataFrame([data])

        # Save results
        if os.path.exists(SURVEY_RESULTS_FILE):
            df_existing = pd.read_excel(SURVEY_RESULTS_FILE)
            df = pd.concat([df_existing, df], ignore_index=True)

        df.to_excel(SURVEY_RESULTS_FILE, index=False)

        print("Survey data saved. Redirecting to v_dashboard.")
        return redirect(url_for("v_dashboard"))

    return render_template("survey.html", project=project, questions=questions)


@app.route("/v_dashboard", methods=["GET"])
def v_dashboard():
    if not session.get("logged_in"):
        return redirect(url_for("volunteer_login"))

    if os.path.exists(SURVEY_RESULTS_FILE):
        df = pd.read_excel(SURVEY_RESULTS_FILE)
        survey_data = df.to_dict(orient="records")
    else:
        survey_data = []
    return render_template("v_dashboard.html", survey_data=survey_data)


# Route: Company Login
@app.route("/company_login", methods=["GET", "POST"])
def company_login():
    if request.method == "POST":
        # Handle company login logic (if needed)
        return redirect(url_for("csr_selection"))
    return render_template("company_login.html")


# Route: CSR Eligibility Calculator (Index Page)
@app.route("/csr_calculator", methods=["GET", "POST"])
def csr_calculator():
    if request.method == "POST":
        net_worth = float(request.form["net_worth"])
        turnover = float(request.form["turnover"])
        net_profit = float(request.form["net_profit"])

        # CSR Eligibility Logic
        csr_amount = 0
        if net_worth >= 500 or turnover >= 1000 or net_profit >= 5:
            csr_amount = net_profit * 0.02
            csr_result = f"Eligible for CSR. CSR Amount: ₹{csr_amount:.2f} crores."
        else:
            csr_result = "Not eligible for CSR."

        return render_template("company_login.html", csr_result=csr_result, csr_amount=csr_amount)

    return render_template("company_login.html")


# Route: CSR Calculation (Corrected)
@app.route("/calculate_csr/", methods=["POST"])
def calculate_csr():
    net_worth = float(request.form["net_worth"])
    turnover = float(request.form["turnover"])
    net_profit = float(request.form["net_profit"])

    if net_worth >= 500 or turnover >= 1000 or net_profit >= 5:
        csr_amount = max(turnover * 0.002, 0)  # 0.2% of Turnover
        message = f"The minimum amount you need to spend on CSR is ₹{csr_amount:.2f}"
        csr_data["amount"] = csr_amount  # Store CSR amount
    else:
        message = "You are not eligible for CSR."
        csr_data["amount"] = 0

    return render_template("company_login.html", csr_result=message, csr_amount=csr_data["amount"])


# Route: CSR Selection
@app.route("/project_details/", methods=["GET"])
def csr_selection():
    return render_template("csr_selection.html")


@app.route("/select_csr", methods=["POST"])
def select_csr():
    option = request.form.get("csr_option")
    if option == "outside_csr":
        return redirect(url_for("input_page"))
    else:
        return "Inside CSR page is under development."  # Placeholder for future implementation


# Route: Project Input Form
@app.route("/input", methods=["GET", "POST"])
def input_page():
    if request.method == "POST":
        if "view_problems" in request.form:
            return redirect(url_for("view_problems"))
        else:
            category = request.form["category"]
            subcategory = request.form["subcategory"]
            pincode = request.form["pincode"]
            budget = request.form["budget"]

            metrics, map_path = search_and_aggregate(category, subcategory, pincode, budget)

            if metrics:
                return render_template("dashboard.html", metrics=metrics, map_path=map_path)
            else:
                return "No projects available for the selected category in your region."

    return render_template("input.html")

# Route: View Problems
@app.route("/view_problems", methods=["GET", "POST"])
def view_problems():
    if request.method == "POST":
        category = request.form.get("category")
        subcategory = request.form.get("subcategory")
        pincode = request.form.get("pincode")
        budget = request.form.get("budget")

        if os.path.exists(user_data_path):
            user_data = pd.read_csv(user_data_path)
            matching_instances = user_data[
                (user_data["Location (Pincode)"] == int(pincode)) &
                (user_data["Budget"] == int(budget)) &
                (user_data["MainCategory"] == category) &
                (user_data["SubCategory"] == subcategory)
                ]
            if not matching_instances.empty:
                return render_template("view_problems.html", instances=matching_instances.to_dict(orient="records"))
            else:
                return "No matching instances found."
        else:
            return "No user data available."

    return render_template("input.html")


# Route: Dashboard Display
@app.route("/dashboard", methods=["POST"])
def dashboard():
    category = request.form["category"]
    subcategory = request.form["subcategory"]
    pincode = request.form["pincode"]
    budget = request.form["budget"]

    metrics, map_path = search_and_aggregate(category, subcategory, pincode, budget)

    if metrics:
        return render_template("dashboard.html", metrics=metrics, map_path=map_path)
    else:
        return "No projects available for the selected category in your region."


# Route: User Input Form
@app.route("/user", methods=["GET", "POST"])
def user_input():
    if request.method == "POST":
        pincode = request.form["pincode"]
        budget = request.form["budget"]
        main_category = request.form["main_category"]
        sub_category = request.form["sub_category"]

        user_data = pd.DataFrame([[pincode, budget, sub_category, main_category]],
                                 columns=["Location (Pincode)", "Budget", "SubCategory", "MainCategory"])
        if os.path.exists(user_data_path):
            user_data.to_csv(user_data_path, mode='a', header=False, index=False)
        else:
            user_data.to_csv(user_data_path, index=False)

        # Redirect to the success page
        return redirect(url_for("success"))

    return render_template("user_login.html")


# Feedback and PDF Generation
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_FOLDER = os.path.join(BASE_DIR, "pdfs")
CSV_FILE = os.path.join(BASE_DIR, "feedback_data.csv")
os.makedirs(PDF_FOLDER, exist_ok=True)

nlp = spacy.load("en_core_web_sm")

FEEDBACK_CATEGORIES = [
    "CSR Hackathons", "Afforestation", "Emergency Aid",
    "Households Utility Reports", "Medical Camps", "Women Empowerment"
]

if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            ["Company Name", "Location", "Date", "Report Type", "Report", "Sentiment", "Keywords", "Extracted Numbers"])


@app.route("/feedback")
def feedback_form():
    """Render the feedback form."""
    return render_template("form.html", categories=FEEDBACK_CATEGORIES)


@app.route("/submit", methods=["POST"])
def submit_feedback():
    """Process and store feedback while generating PDF."""
    company_name = request.form.get("company_name")
    location = request.form.get("location")
    date_of_completion = request.form.get("date_of_completion")
    report_type = request.form.get("report_type")
    report = request.form.get("report")

    if len(report.split()) < 100:
        return render_template("form.html", categories=FEEDBACK_CATEGORIES,
                               error="The report must contain at least 100 words.")

    safe_company_name = re.sub(r'\W+', '_', company_name)
    pdf_filename = os.path.join(PDF_FOLDER, f"{safe_company_name}_{report_type}.pdf")

    sentiment_score = TextBlob(report).sentiment.polarity
    sentiment = "Positive" if sentiment_score > 0 else "Negative" if sentiment_score < 0 else "Neutral"

    doc = nlp(report)
    keywords = [token.text.lower() for token in doc if token.is_alpha and not token.is_stop]
    keyword_freq = Counter(keywords).most_common(5)
    keyword_str = ", ".join([kw[0] for kw in keyword_freq])

    numbers = re.findall(r'\b\d+\b', report)
    numbers_str = ", ".join(numbers)

    c = canvas.Canvas(pdf_filename, pagesize=letter)
    c.setFont("Helvetica-Bold", 14)
    y = 750
    c.drawString(50, y, f"{report_type} Feedback Report")
    y -= 30
    c.setFont("Helvetica", 12)

    details = [
        f"Company Name: {company_name}",
        f"Location: {location}",
        f"Date of Completion: {date_of_completion}",
        f"Sentiment: {sentiment}",
        f"Keywords: {keyword_str}",
        f"Numbers: {numbers_str}",
    ]

    for line in details:
        y -= 20
        c.drawString(50, y, line)

    c.save()

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            [company_name, location, date_of_completion, report_type, report, sentiment, keyword_str, numbers_str])

    return send_file(pdf_filename, as_attachment=True)


from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
import io

@app.route("/track_progress", methods=["GET"])
def track_progress():
    # Load the necessary data
    historical = pd.read_csv("historical.csv")
    user = pd.read_csv("user.csv")

    # Standardize column names
    historical.columns = historical.columns.str.lower().str.strip()
    user.columns = user.columns.str.lower().str.strip()

    # Ensure necessary columns exist
    required_columns = [
        "pincode", "budget", "company id", "% patients diagnosed & treated",
        "% decrease in reported illnesses", "% patients screened for diseases",
        "% patients receiving follow-up treatment", "% increase in vaccination coverage",
        "% people attending awareness programs", "% increase in overall community health"
    ]

    for col in required_columns:
        if col not in user.columns:
            raise KeyError(f"Error: Missing column '{col}' in user dataset!")

    # Identify New and Removed Entries
    new_entries = user[~user['company id'].isin(historical['company id'])]
    removed_entries = historical[~historical['company id'].isin(user['company id'])]

    # Detect Improvements and Declines
    def detect_changes(old_df, new_df, metric):
        merged = old_df.merge(new_df, on='company id', suffixes=('_old', '_new'))
        improved = merged[merged[f'{metric}_new'] > merged[f'{metric}_old']]
        declined = merged[merged[f'{metric}_new'] < merged[f'{metric}_old']]
        return improved[['company id', f'{metric}_old', f'{metric}_new']], declined[
            ['company id', f'{metric}_old', f'{metric}_new']]

    improvements, declines = detect_changes(historical, user, "% increase in overall community health")

    # Generate Bar Chart
    plt.figure(figsize=(8, 4))
    plt.bar(["Improved Programs", "Declined Programs"], [len(improvements), len(declines)], color=['pink', 'violet'])
    plt.xlabel("Program Performance")
    plt.ylabel("Number of Programs")
    plt.title("Health Program Performance Overview")
    plt.savefig("static/performance_chart.png")

    # Generate Line Chart (Trends Over Time)
    plt.figure(figsize=(8, 4))
    user.groupby("pincode")["% increase in overall community health"].mean().plot(kind="line", marker="o", linestyle="-")
    plt.xlabel("Pincode")
    plt.ylabel("Community Health Improvement (%)")
    plt.title("Community Health Trends Over Different Pincodes")
    plt.grid()
    plt.savefig("static/line_chart.png")

    # Generate PDF Report with Bullet Points and Charts
    pdf_filename = "static/progress_report.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 750, "Progress Report")

    # Bullet Points Function
    def draw_bullet_points(canvas, y_start, title, items):
        canvas.setFont("Helvetica-Bold", 12)
        canvas.drawString(50, y_start, title)
        y = y_start - 20
        canvas.setFont("Helvetica", 11)
        if items.empty:
            canvas.drawString(60, y, "- No updates for this period.")
        else:
            for _, row in items.iterrows():
                text = f"- {row.to_list()}"
                canvas.drawString(60, y, text[:90])  # Limit length
                y -= 20
        return y - 10

    # Adding Sections with Bullet Points
    y_position = 730
    y_position = draw_bullet_points(c, y_position, "📌 New Health Programs Introduced:", new_entries)
    y_position = draw_bullet_points(c, y_position, "🚨 Programs No Longer Active:", removed_entries)
    y_position = draw_bullet_points(c, y_position, "📈 Improvements:", improvements)
    y_position = draw_bullet_points(c, y_position, "⚠️ Declines:", declines)

    # Add Images (Bar Chart and Line Chart)
    c.drawImage("static/performance_chart.png", 50, y_position - 180, width=400, height=150)
    c.drawImage("static/line_chart.png", 50, y_position - 360, width=400, height=150)

    c.save()

    return render_template("progress_report.html", improvements=improvements, declines=declines,
                           new_entries=new_entries, removed_entries=removed_entries, pdf_filename=pdf_filename)

@app.route("/success")
def success():
    return render_template("success.html")
if __name__ == "__main__":
    app.run(debug=True)
