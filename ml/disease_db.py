"""
Disease Knowledge Base module mapping prognosis classes to descriptions,
precautions, severity levels, and recommended specialist doctors.
"""

DISEASE_DETAILS = {
    "Fungal infection": {
        "description": "A skin disease caused by a fungus. Common fungal infections include athlete's foot, ringworm, and candidiasis. Fungal infections thrive in warm, moist areas.",
        "severity": "Low to Moderate",
        "doctor": "Dermatologist",
        "precautions": [
            "Keep the affected area clean and dry",
            "Use antifungal creams as prescribed",
            "Avoid sharing personal items like towels and clothing",
            "Wear breathable cotton clothing"
        ]
    },
    "Allergy": {
        "description": "An immune system reaction to a foreign substance (allergen) that is normally harmless, such as pollen, pet dander, or certain foods.",
        "severity": "Low to Moderate",
        "doctor": "Allergist / Immunologist",
        "precautions": [
            "Identify and avoid known allergen triggers",
            "Take prescribed antihistamines",
            "Keep indoor air clean with HEPA filters",
            "Use saline nasal rinses for congestion"
        ]
    },
    "GERD": {
        "description": "Gastroesophageal Reflux Disease is a chronic condition where stomach acid flows back into the esophagus, causing heartburn and acid indigestion.",
        "severity": "Moderate",
        "doctor": "Gastroenterologist",
        "precautions": [
            "Avoid spicy, fatty, and acidic foods",
            "Do not lie down immediately after eating",
            "Eat smaller, more frequent meals",
            "Elevate the head of your bed while sleeping"
        ]
    },
    "Chronic cholestasis": {
        "description": "A condition where bile flow from the liver is reduced or blocked, leading to jaundice and liver discomfort over prolonged periods.",
        "severity": "High",
        "doctor": "Hepatologist / Gastroenterologist",
        "precautions": [
            "Follow a low-fat diet",
            "Avoid alcohol and liver-toxic medications",
            "Consult a specialist for proper diagnostic workup",
            "Take prescribed bile-acid sequestrants or supplements"
        ]
    },
    "Drug Reaction": {
        "description": "An adverse effect caused by taking a medication, ranging from mild rashes to severe allergic reactions (e.g., Stevens-Johnson syndrome).",
        "severity": "Moderate to High",
        "doctor": "General Physician / Dermatologist",
        "precautions": [
            "Stop the suspected drug immediately after consulting a doctor",
            "Report the reaction to your healthcare provider",
            "Keep a list of known drug allergies",
            "Seek emergency care if breathing issues or severe swelling occur"
        ]
    },
    "Peptic ulcer diseae": {
        "description": "Sores that develop on the inside lining of the stomach and the upper portion of the small intestine, commonly caused by H. pylori or NSAID overuse.",
        "severity": "Moderate",
        "doctor": "Gastroenterologist",
        "precautions": [
            "Avoid NSAID pain relievers unless prescribed",
            "Limit alcohol and caffeine consumption",
            "Eat mild, non-irritating foods",
            "Complete antibiotic treatment if H. pylori is detected"
        ]
    },
    "AIDS": {
        "description": "Acquired Immunodeficiency Syndrome is a chronic, potentially life-threatening condition caused by the Human Immunodeficiency Virus (HIV).",
        "severity": "High",
        "doctor": "Infectious Disease Specialist",
        "precautions": [
            "Strict adherence to Antiretroviral Therapy (ART)",
            "Practice safe barrier methods during sexual activity",
            "Avoid sharing needles or unsterile sharp objects",
            "Maintain regular health monitorings and vaccinations"
        ]
    },
    "Diabetes ": {
        "description": "A group of metabolic diseases characterized by elevated levels of blood glucose over a prolonged period due to insulin deficiency or resistance.",
        "severity": "Moderate to High",
        "doctor": "Endocrinologist",
        "precautions": [
            "Monitor blood sugar levels regularly",
            "Maintain a low-glycemic, balanced diet",
            "Engage in regular physical exercise",
            "Take prescribed insulin or oral antidiabetic medications"
        ]
    },
    "Gastroenteritis": {
        "description": "An inflammation of the stomach and intestines, typically resulting from bacterial or viral infection or food poisoning.",
        "severity": "Moderate",
        "doctor": "General Physician / Gastroenterologist",
        "precautions": [
            "Stay hydrated with Oral Rehydration Solution (ORS)",
            "Eat a bland diet (BRAT: Bananas, Rice, Applesauce, Toast)",
            "Practice strict hand hygiene",
            "Avoid dairy, greasy, and spicy foods until recovered"
        ]
    },
    "Bronchial Asthma": {
        "description": "A chronic inflammatory respiratory disease characterized by hyperreactive airways causing wheezing, shortness of breath, and coughing.",
        "severity": "Moderate to High",
        "doctor": "Pulmonologist",
        "precautions": [
            "Keep quick-relief inhalers accessible at all times",
            "Avoid known triggers such as dust, smoke, and cold air",
            "Follow your asthma action plan",
            "Get annual flu and pneumonia vaccinations"
        ]
    },
    "Hypertension ": {
        "description": "High blood pressure is a long-term medical condition in which the blood pressure in the arteries is persistently elevated.",
        "severity": "Moderate to High",
        "doctor": "Cardiologist / General Physician",
        "precautions": [
            "Reduce daily dietary sodium intake",
            "Exercise regularly for at least 30 minutes daily",
            "Manage stress levels effectively",
            "Take prescribed antihypertensive medication consistently"
        ]
    },
    "Migraine": {
        "description": "A neurological condition that can cause severe throbbing pain or a pulsing sensation, usually on one side of the head, often with nausea and light sensitivity.",
        "severity": "Moderate",
        "doctor": "Neurologist",
        "precautions": [
            "Rest in a quiet, dark room during attacks",
            "Identify and avoid trigger foods (e.g., aged cheese, caffeine)",
            "Maintain consistent sleep patterns",
            "Stay well hydrated throughout the day"
        ]
    },
    "Cervical spondylosis": {
        "description": "Age-related wear and tear affecting the spinal disks in your neck. As disks dehydrate and shrink, signs of osteoarthritis develop.",
        "severity": "Moderate",
        "doctor": "Orthopedic Surgeon / Neurologist",
        "precautions": [
            "Maintain proper posture while working on computers",
            "Perform neck strengthening and stretching exercises",
            "Use ergonomic pillows and chairs",
            "Avoid heavy lifting or sudden head movements"
        ]
    },
    "Paralysis (brain hemorrhage)": {
        "description": "Loss of voluntary muscle function in one or more parts of the body caused by bleeding within the brain tissue (hemorrhagic stroke).",
        "severity": "Critical",
        "doctor": "Neurologist / Neurosurgeon",
        "precautions": [
            "Seek IMMEDIATE emergency medical intervention",
            "Undergo rehabilitation and physical therapy",
            "Control high blood pressure strictly",
            "Take prescribed blood thinners or antiplatelet drugs under guidance"
        ]
    },
    "Jaundice": {
        "description": "A yellowish pigmentation of the skin and whites of the eyes caused by high bilirubin levels, often signaling liver dysfunction or bile duct obstruction.",
        "severity": "High",
        "doctor": "Hepatologist / Gastroenterologist",
        "precautions": [
            "Avoid alcohol completely",
            "Drink plenty of clean water and fresh fruit juices",
            "Rest adequately to assist liver recovery",
            "Consult a physician for underlying cause diagnosis"
        ]
    },
    "Malaria": {
        "description": "A mosquito-borne infectious disease caused by Plasmodium parasites, marked by recurring fever, chills, sweating, and anemia.",
        "severity": "High",
        "doctor": "Infectious Disease Specialist / General Physician",
        "precautions": [
            "Complete full course of prescribed antimalarial medication",
            "Use mosquito nets and insect repellent sprays",
            "Eliminate stagnant water around living areas",
            "Wear long-sleeved clothing during evening hours"
        ]
    },
    "Chicken pox": {
        "description": "A highly contagious viral infection caused by the varicella-zoster virus, characterized by an itchy rash with fluid-filled blisters.",
        "severity": "Moderate",
        "doctor": "Pediatrician / General Physician",
        "precautions": [
            "Isolate to prevent spreading to others",
            "Avoid scratching blisters to prevent bacterial infections and scarring",
            "Apply calamine lotion to soothe itching",
            "Take warm baths with baking soda or oatmeal"
        ]
    },
    "Dengue": {
        "description": "A mosquito-borne viral disease causing high fever, severe headache, muscle and joint pain, and characteristic skin rash.",
        "severity": "High",
        "doctor": "Infectious Disease Specialist / General Physician",
        "precautions": [
            "Monitor platelet counts regularly",
            "Hydrate extensively with fluids, coconut water, and ORS",
            "Avoid NSAIDs like ibuprofen or aspirin (use paracetamol only)",
            "Prevent mosquito bites using repellents and screens"
        ]
    },
    "Typhoid": {
        "description": "A bacterial infection caused by Salmonella typhi, spreading through contaminated food and water, presenting with sustained fever and abdominal pain.",
        "severity": "High",
        "doctor": "General Physician / Infectious Disease Specialist",
        "precautions": [
            "Complete the entire course of prescribed antibiotics",
            "Consume only boiled or bottled drinking water",
            "Eat freshly cooked, hot food",
            "Practice rigorous handwashing before eating"
        ]
    },
    "hepatitis A": {
        "description": "A highly contagious liver infection caused by the Hepatitis A virus, transmitted through contaminated food or water.",
        "severity": "Moderate to High",
        "doctor": "Hepatologist / Gastroenterologist",
        "precautions": [
            "Get rest and allow the liver to recover naturally",
            "Avoid alcohol and medications metabolized by the liver",
            "Eat nutrient-dense, low-fat meals",
            "Wash hands thoroughly after using the bathroom"
        ]
    },
    "Hepatitis B": {
        "description": "A serious liver infection caused by the Hepatitis B virus, which can become chronic and lead to liver cirrhosis or failure.",
        "severity": "High",
        "doctor": "Hepatologist",
        "precautions": [
            "Undergo antiviral therapy as prescribed",
            "Avoid alcohol consumption strictly",
            "Get family members vaccinated for Hepatitis B",
            "Use barrier protection during close contact"
        ]
    },
    "Hepatitis C": {
        "description": "A viral infection caused by HCV that causes liver inflammation, often leading to serious liver damage if untreated.",
        "severity": "High",
        "doctor": "Hepatologist",
        "precautions": [
            "Take direct-acting antiviral (DAA) medications as directed",
            "Avoid alcohol completely",
            "Do not share personal razors or toothbrushes",
            "Maintain regular liver enzyme and viral load testing"
        ]
    },
    "Hepatitis D": {
        "description": "A serious liver disease caused by the Hepatitis D virus, which only occurs in people who are already infected with Hepatitis B.",
        "severity": "High",
        "doctor": "Hepatologist",
        "precautions": [
            "Follow treatment for Hepatitis B infection",
            "Avoid alcohol and hepatotoxic drugs",
            "Undergo routine liver imaging and enzyme monitoring",
            "Maintain a healthy, low-fat liver-supportive diet"
        ]
    },
    "Hepatitis E": {
        "description": "A liver disease caused by the Hepatitis E virus, usually transmitted via contaminated drinking water, particularly risky during pregnancy.",
        "severity": "Moderate to High",
        "doctor": "Hepatologist / General Physician",
        "precautions": [
            "Drink safe, boiled, or purified water",
            "Avoid uncooked shellfish and raw produce",
            "Ensure adequate rest and hydration",
            "Seek immediate care if pregnant and experiencing symptoms"
        ]
    },
    "Alcoholic hepatitis": {
        "description": "Liver inflammation caused by drinking alcohol heavily over many years, leading to jaundice, fluid accumulation, and liver failure.",
        "severity": "High to Critical",
        "doctor": "Hepatologist / Addiction Specialist",
        "precautions": [
            "Abstain from alcohol immediately and permanently",
            "Follow a high-protein, calorie-rich nutritional plan",
            "Take prescribed liver support medications",
            "Enroll in alcohol cessation support programs"
        ]
    },
    "Tuberculosis": {
        "description": "A potentially serious infectious disease caused by Mycobacterium tuberculosis that mainly affects the lungs, causing chronic cough with blood.",
        "severity": "High",
        "doctor": "Pulmonologist / Infectious Disease Specialist",
        "precautions": [
            "Complete full 6-to-9 month course of anti-TB drugs without skipping doses",
            "Wear a mask to prevent airborne transmission to others",
            "Ensure good room ventilation and direct sunlight exposure",
            "Eat a high-protein, nutritious diet"
        ]
    },
    "Common Cold": {
        "description": "A mild viral infection of the upper respiratory tract involving nose and throat, causing sneezing, runny nose, and sore throat.",
        "severity": "Low",
        "doctor": "General Physician",
        "precautions": [
            "Get plenty of rest and stay warm",
            "Drink warm fluids like soup, tea, and warm water",
            "Use saline nasal sprays or steam inhalation",
            "Wash hands frequently to avoid spreading virus"
        ]
    },
    "Pneumonia": {
        "description": "An infection that inflames air sacs in one or both lungs, which may fill with fluid or pus, causing cough with phlegm, fever, chills, and difficulty breathing.",
        "severity": "High",
        "doctor": "Pulmonologist / General Physician",
        "precautions": [
            "Take prescribed antibiotics or antivirals fully",
            "Rest extensively and stay well hydrated",
            "Use a humidifier or warm steam to loosen phlegm",
            "Seek emergency evaluation if breathing worsens"
        ]
    },
    "Dimorphic hemmorhoids(piles)": {
        "description": "Swollen veins in your anus and lower rectum, similar to varicose veins, causing bleeding, pain, and discomfort during bowel movements.",
        "severity": "Moderate",
        "doctor": "Proctologist / General Surgeon",
        "precautions": [
            "Eat high-fiber foods (fruits, vegetables, whole grains)",
            "Drink plenty of water daily",
            "Avoid straining during bowel movements",
            "Take warm sitz baths for 15-20 minutes daily"
        ]
    },
    "Heart attack": {
        "description": "A medical emergency where blood flow to a part of the heart muscle is severely blocked, usually by a blood clot in coronary arteries.",
        "severity": "Critical",
        "doctor": "Cardiologist / Emergency Physician",
        "precautions": [
            "CALL EMERGENCY SERVICES IMMEDIATELY",
            "Chew an aspirin if recommended by emergency responders",
            "Rest quietly while waiting for emergency team",
            "Undergo immediate cardiac evaluation and intervention"
        ]
    },
    "Varicose veins": {
        "description": "Gnarled, enlarged veins, most commonly appearing in legs and feet due to weakened vein walls and valves.",
        "severity": "Moderate",
        "doctor": "Vascular Surgeon / Dermatologist",
        "precautions": [
            "Wear compression stockings as recommended",
            "Elevate your legs when sitting or lying down",
            "Avoid long periods of standing or sitting still",
            "Exercise regularly to improve leg circulation"
        ]
    },
    "Hypothyroidism": {
        "description": "A condition in which the thyroid gland doesn't produce enough crucial thyroid hormones, slowing down metabolism, causing fatigue and weight gain.",
        "severity": "Moderate",
        "doctor": "Endocrinologist",
        "precautions": [
            "Take daily levothyroxine hormone replacement as prescribed",
            "Have TSH blood levels monitored regularly",
            "Maintain a balanced diet rich in iodine and fiber",
            "Avoid taking calcium/iron supplements simultaneously with thyroid meds"
        ]
    },
    "Hyperthyroidism": {
        "description": "Overactivity of the thyroid gland, resulting in an excess of thyroid hormones and accelerated metabolism, rapid heartbeat, and weight loss.",
        "severity": "Moderate to High",
        "doctor": "Endocrinologist",
        "precautions": [
            "Take antithyroid medications or beta-blockers as directed",
            "Avoid excessive iodine in diet and supplements",
            "Monitor heart rate and blood pressure regularly",
            "Manage anxiety and stress through relaxation techniques"
        ]
    },
    "Hypoglycemia": {
        "description": "A condition characterized by an abnormally low level of blood sugar (glucose), leading to shakiness, confusion, sweating, and dizziness.",
        "severity": "High (Acute)",
        "doctor": "Endocrinologist / General Physician",
        "precautions": [
            "Consume 15-20 grams of fast-acting carbs (fruit juice, candy) immediately",
            "Recheck blood glucose after 15 minutes",
            "Carry fast-acting glucose tablets or gel at all times",
            "Eat regular meals and snacks on a consistent schedule"
        ]
    },
    "Osteoarthristis": {
        "description": "A type of arthritis that occurs when flexible tissue at the ends of bones wears down over time, causing joint pain and stiffness.",
        "severity": "Moderate",
        "doctor": "Orthopedic Specialist / Rheumatologist",
        "precautions": [
            "Engage in low-impact exercise like swimming or walking",
            "Maintain a healthy weight to reduce joint stress",
            "Apply hot or cold compresses to painful joints",
            "Use supportive joint braces or walking aids if recommended"
        ]
    },
    "Arthritis": {
        "description": "Inflammation of one or more joints, causing pain, swelling, stiffness, and limited range of motion.",
        "severity": "Moderate",
        "doctor": "Rheumatologist",
        "precautions": [
            "Follow prescribed anti-inflammatory therapy",
            "Perform gentle daily range-of-motion exercises",
            "Protect joints from excessive strain and repetitive trauma",
            "Use anti-inflammatory dietary choices (omega-3 fatty acids)"
        ]
    },
    "(vertigo) Paroymsal  Positional Vertigo": {
        "description": "Benign Paroxysmal Positional Vertigo (BPPV) is a disorder arising from the inner ear causing short episodes of intense spinning sensations triggered by head movements.",
        "severity": "Moderate",
        "doctor": "ENT Specialist / Neurologist",
        "precautions": [
            "Perform Epley maneuver under specialist guidance",
            "Change head positions slowly and deliberately",
            "Avoid sudden head movements or bending down quickly",
            "Sit down immediately when feeling dizzy to prevent falls"
        ]
    },
    "Acne": {
        "description": "A skin condition that occurs when hair follicles become plugged with oil and dead skin cells, causing pimples, blackheads, and scarring.",
        "severity": "Low",
        "doctor": "Dermatologist",
        "precautions": [
            "Wash face twice daily with a mild non-comedogenic cleanser",
            "Avoid squeezing or popping pimples to prevent scarring",
            "Use non-comedogenic skincare and cosmetic products",
            "Apply topical benzoyl peroxide or salicylic acid as advised"
        ]
    },
    "Urinary tract infection": {
        "description": "An infection in any part of the urinary system (kidneys, bladder, urethra), causing burning sensation during urination and frequent urge to urinate.",
        "severity": "Moderate",
        "doctor": "Urologist / General Physician",
        "precautions": [
            "Drink plenty of water to flush bacteria from urinary tract",
            "Complete prescribed antibiotic regimen completely",
            "Avoid bladder irritants like alcohol, caffeine, and spicy foods",
            "Maintain proper personal hygiene"
        ]
    },
    "Psoriasis": {
        "description": "A skin disease that causes skin cells to multiply up to 10 times faster than normal, resulting in bumpy red patches covered with white scales.",
        "severity": "Moderate",
        "doctor": "Dermatologist",
        "precautions": [
            "Keep skin moist with thick creams or ointments",
            "Avoid skin triggers like stress, smoking, and skin injuries",
            "Get brief, controlled sun exposure",
            "Use prescribed topical corticosteroids or phototherapy"
        ]
    },
    "Impetigo": {
        "description": "A highly contagious bacterial skin infection causing red sores that can break open, ooze, and develop yellow-brown crusts, mostly around nose and mouth.",
        "severity": "Low to Moderate",
        "doctor": "Dermatologist / Pediatrician",
        "precautions": [
            "Gently wash sores with mild soap and water",
            "Apply prescribed topical or oral antibiotic ointment",
            "Keep fingernails trimmed short to prevent scratching",
            "Wash clothing, linens, and towels separately in hot water"
        ]
    }
}

DEFAULT_DISEASE_INFO = {
    "description": "Detailed clinical medical profile currently undergoing expanded research and validation.",
    "severity": "Moderate",
    "doctor": "General Physician",
    "precautions": [
        "Consult a certified medical professional for diagnosis",
        "Monitor symptoms and keep a symptom log",
        "Ensure proper rest and balanced hydration",
        "Seek emergency care if symptoms rapidly deteriorate"
    ]
}


def get_disease_info(disease_name: str) -> dict:
    """Return disease details with fallback for minor dataset key variations."""
    clean_name = disease_name.strip() if disease_name else ""
    if clean_name in DISEASE_DETAILS:
        return DISEASE_DETAILS[clean_name]

    # Case-insensitive match check
    for key, info in DISEASE_DETAILS.items():
        if key.strip().lower() == clean_name.lower():
            return info

    return DEFAULT_DISEASE_INFO
