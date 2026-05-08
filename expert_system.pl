
% ------------------------------------------------------------
%   SECTION 1: SYMPTOM FACTS
%   Format: symptom(Disease, Symptom).
%   Each fact links a disease to ONE of its symptoms.
% ------------------------------------------------------------

% --- Flu ---
symptom(flu, fever).
symptom(flu, cough).
symptom(flu, sore_throat).
symptom(flu, body_aches).
symptom(flu, fatigue).

% --- Common Cold ---
symptom(cold, runny_nose).
symptom(cold, sneezing).
symptom(cold, sore_throat).
symptom(cold, mild_cough).
symptom(cold, congestion).

% --- COVID-19 ---
symptom(covid19, fever).
symptom(covid19, dry_cough).
symptom(covid19, loss_of_smell).
symptom(covid19, loss_of_taste).
symptom(covid19, shortness_of_breath).
symptom(covid19, fatigue).

% --- Diabetes ---
symptom(diabetes, frequent_urination).
symptom(diabetes, excessive_thirst).
symptom(diabetes, blurred_vision).
symptom(diabetes, fatigue).
symptom(diabetes, slow_healing).

% --- Hypertension (High Blood Pressure) ---
symptom(hypertension, headache).
symptom(hypertension, dizziness).
symptom(hypertension, chest_pain).
symptom(hypertension, shortness_of_breath).
symptom(hypertension, nosebleed).

% --- Malaria ---
symptom(malaria, high_fever).
symptom(malaria, chills).
symptom(malaria, sweating).
symptom(malaria, headache).
symptom(malaria, nausea).
symptom(malaria, vomiting).

% --- Asthma ---
symptom(asthma, shortness_of_breath).
symptom(asthma, wheezing).
symptom(asthma, chest_tightness).
symptom(asthma, cough).
symptom(asthma, difficulty_breathing).

% --- Gastroenteritis (Stomach Flu) ---
symptom(gastroenteritis, nausea).
symptom(gastroenteritis, vomiting).
symptom(gastroenteritis, diarrhea).
symptom(gastroenteritis, stomach_cramps).
symptom(gastroenteritis, fever).

% --- Anemia ---
symptom(anemia, fatigue).
symptom(anemia, pale_skin).
symptom(anemia, dizziness).
symptom(anemia, shortness_of_breath).
symptom(anemia, cold_hands).

% --- Migraine ---
symptom(migraine, severe_headache).
symptom(migraine, nausea).
symptom(migraine, sensitivity_to_light).
symptom(migraine, sensitivity_to_sound).
symptom(migraine, blurred_vision).

% ------------------------------------------------------------
%   SECTION 2: TREATMENT FACTS
%   Format: treatment(Disease, Treatment).
% ------------------------------------------------------------

treatment(flu,            'Rest, drink fluids, take paracetamol for fever, use antiviral drugs if severe.').
treatment(cold,           'Rest, stay hydrated, use decongestants, gargle with salt water.').
treatment(covid19,        'Isolate yourself, rest, drink fluids, consult a doctor for antivirals if needed.').
treatment(diabetes,       'Maintain healthy diet, exercise regularly, monitor blood sugar, take insulin/medication as prescribed.').
treatment(hypertension,   'Reduce salt intake, exercise, avoid stress, take prescribed antihypertensive medication.').
treatment(malaria,        'Take antimalarial drugs (e.g., chloroquine), rest, stay hydrated, see a doctor immediately.').
treatment(asthma,         'Use prescribed inhalers, avoid triggers, follow an asthma action plan.').
treatment(gastroenteritis,'Stay hydrated with oral rehydration salts, eat bland food, rest, avoid solid food until vomiting stops.').
treatment(anemia,         'Eat iron-rich foods, take iron supplements, treat underlying cause, consult a doctor.').
treatment(migraine,       'Rest in a quiet dark room, take pain relievers (ibuprofen), stay hydrated, avoid triggers.').

% ------------------------------------------------------------
%   SECTION 3: DIAGNOSIS RULES
%   Logic: count how many of the user-entered symptoms
%          match a disease. If matches >= MinRequired, diagnose.
% ------------------------------------------------------------

% count_matches(+Disease, +SymptomList, -Count)
% Counts how many symptoms in SymptomList belong to Disease.
count_matches(_, [], 0).
count_matches(Disease, [H|T], Count) :-
    count_matches(Disease, T, Rest),
    ( symptom(Disease, H) -> Count is Rest + 1 ; Count is Rest ).

% diagnose(+SymptomList, -Disease, -Score)
% Returns all diseases with their match score, filtered by threshold.
diagnose(SymptomList, Disease, Score) :-
    disease(Disease),
    count_matches(Disease, SymptomList, Score),
    Score >= 2.   % At least 2 symptoms must match to suggest a disease

% ------------------------------------------------------------
%   SECTION 4: ALL KNOWN DISEASES
%   Used to iterate over diseases during diagnosis.
% ------------------------------------------------------------

disease(flu).
disease(cold).
disease(covid19).
disease(diabetes).
disease(hypertension).
disease(malaria).
disease(asthma).
disease(gastroenteritis).
disease(anemia).
disease(migraine).

% ------------------------------------------------------------
%   SECTION 5: HELPER — GET TREATMENT
%   get_treatment(+Disease, -Treatment)
% ------------------------------------------------------------

get_treatment(Disease, Treatment) :-
    treatment(Disease, Treatment).

% ------------------------------------------------------------
%   SECTION 6: LIST ALL SYMPTOMS FOR A DISEASE
%   Useful for displaying what symptoms each disease has.
% ------------------------------------------------------------

all_symptoms(Disease, Symptoms) :-
    findall(S, symptom(Disease, S), Symptoms).
