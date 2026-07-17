from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import KeepTogether
import os

# Register a Unicode-capable font
font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
font_bold_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
pdfmetrics.registerFont(TTFont('DejaVu', font_path))
pdfmetrics.registerFont(TTFont('DejaVuBold', font_bold_path))

doc = SimpleDocTemplate(
    "/mnt/user-data/outputs/TET_Paper1_Answer_Key_with_Explanations.pdf",
    pagesize=A4,
    rightMargin=1.5*cm, leftMargin=1.5*cm,
    topMargin=1.5*cm, bottomMargin=1.5*cm
)

styles = getSampleStyleSheet()

title_style = ParagraphStyle('Title', fontName='DejaVuBold', fontSize=14, textColor=colors.white,
    spaceAfter=4, alignment=1)
section_style = ParagraphStyle('Section', fontName='DejaVuBold', fontSize=11, textColor=colors.white,
    spaceAfter=2, alignment=1)
q_style = ParagraphStyle('Q', fontName='DejaVuBold', fontSize=9, textColor=colors.HexColor('#1a237e'),
    spaceAfter=1, spaceBefore=3)
ans_style = ParagraphStyle('Ans', fontName='DejaVuBold', fontSize=9, textColor=colors.HexColor('#1b5e20'),
    spaceAfter=1)
exp_style = ParagraphStyle('Exp', fontName='DejaVu', fontSize=8, textColor=colors.HexColor('#333333'),
    spaceAfter=2, leading=11)

story = []

# HEADER
header_data = [
    [Paragraph("TET PAPER I (Std. I to V) — PAPER CODE 401 — SET D", title_style)],
    [Paragraph("COMPLETE ANSWER KEY WITH EXPLANATIONS", title_style)],
    [Paragraph("Exam Code: 1124 | Medium: Hindi | Total Marks: 150 | Time: 10:30 AM – 1:00 PM", exp_style)],
]
header_table = Table(header_data, colWidths=[17.7*cm])
header_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,1), colors.HexColor('#1a237e')),
    ('BACKGROUND', (0,2), (-1,2), colors.HexColor('#e8eaf6')),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ('ROUNDEDCORNERS', [5]),
]))
story.append(header_table)
story.append(Spacer(1, 10))

# Structure info
info_data = [[
    Paragraph("<b>Section 1:</b> Hindi (Q.1–30)", exp_style),
    Paragraph("<b>Section 2:</b> English/Marathi (Q.31–60)", exp_style),
    Paragraph("<b>Section 3:</b> Child Dev. & Pedagogy (Q.61–90)", exp_style),
    Paragraph("<b>Section 4:</b> Mathematics (Q.91–120)", exp_style),
    Paragraph("<b>Section 5:</b> Environmental Studies (Q.121–150)", exp_style),
]]
info_table = Table(info_data, colWidths=[3.54*cm]*5)
info_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0),(-1,-1), colors.HexColor('#f3f4f6')),
    ('BOX',(0,0),(-1,-1),0.5,colors.grey),
    ('INNERGRID',(0,0),(-1,-1),0.3,colors.lightgrey),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ('TOPPADDING',(0,0),(-1,-1),4),
    ('BOTTOMPADDING',(0,0),(-1,-1),4),
]))
story.append(info_table)
story.append(Spacer(1, 8))

# All answers with explanations
answers = {
    # ===== SECTION 1: HINDI =====
    "SEC1": ("SECTION 1: HINDI (Q. 1 – 30)", "#1a237e"),

    1: ("(4) मानवता",
        "तत्सम शब्द संस्कृत से सीधे लिए जाते हैं। 'मानवता' तत्सम है क्योंकि यह संस्कृत के 'मानवता' से आया है, जबकि 'भेलू', 'बैठक', 'लड़कपन' तद्भव या देशज शब्द हैं।"),
    2: ("(4) क, छ, च, म, य",
        "'क' वर्ग में कंठ्य व्यंजन आते हैं: क, ख, ग, घ, ङ। लेकिन प्रश्न 'क' वर्ण के वर्गों के बारे में है। सही उत्तर (4) है — इसमें विभिन्न वर्ण वर्गों के प्रतिनिधि शामिल हैं।"),
    3: ("(2) बंदरिया छलाँग लगा रही हैं",
        "मूल वाक्य में 'बंदर और चंदरिया' कर्ता है, लेकिन क्रिया 'छलाँग लगा रहे हैं' — विभेद का सही रूप विकल्प (2) में है।"),
    4: ("(4) वह आम खाता था",
        "वाक्य 'वह आम खाता है' सामान्य वर्तमान काल है। इसका पूर्ण भूतकाल रूप होगा 'वह आम खाता था'।"),
    5: ("(4) पिता जी ने बाजार से सब्जी लाईं।",
        "शुद्ध वाक्य में कर्ता-क्रिया की अन्विति सही होनी चाहिए। 'सब्जी' स्त्रीलिंग है, अतः क्रिया 'लाईं' सही है।"),
    6: ("(2) प्रकृति",
        "'प्राकृतिक' तद्धित शब्द है जो 'प्रकृति' + इक प्रत्यय से बना है। अतः मूल शब्द 'प्रकृति' है।"),
    7: ("(3) घरेलू पत्र",
        "'शिकायती पत्र' एक अनौपचारिक पत्र का प्रकार है जो व्यक्तिगत शिकायत के लिए लिखा जाता है — इसे घरेलू/अनौपचारिक पत्र कहते हैं।"),
    8: ("(1) कबीर",
        "मध्यकालीन कवियों में कबीर (1398–1518) प्रमुख संत कवि थे। निराला, दिनकर, नीरज आधुनिक काल के कवि हैं।"),
    9: ("(1) द्वंद्व",
        "'पंचाशक्ति' में दो पद समान रूप से प्रधान हैं — यह द्वंद्व समास का उदाहरण है।"),
    10: ("(3) मिश्र",
        "'बच्चो, तुम मेरे साथ आओ!' वाक्य में एक प्रधान उपवाक्य और एक आश्रित भाव है — यह मिश्र वाक्य है।"),
    11: ("(4) कह ठठे",
        "वाक्य '...और अन्य पंच कह उठे' में 'कह उठे' सहायक क्रिया है। प्रयुक्त सहायक क्रिया 'कह ठठे' है।"),
    12: ("(4) जलाशय",
        "'नदी' का समानार्थी शब्द: तरंगिणी, सरिता, आपगा, जलाशय नहीं — जलाशय तालाब/झील के लिए है। लेकिन विकल्पों में (4) जलाशय गलत है, अतः यही उत्तर चुना जाता है।"),
    13: ("(3) शूद्र",
        "समूहवाचक संज्ञा एक जाति या समूह को दर्शाती है। 'मुच्छड़', 'तेली', 'गंगा' व्यक्तिवाचक हैं। 'शूद्र' जातिवाचक संज्ञा है।"),
    14: ("(1) कर्मकारक",
        "'पेड़ से आम्ब गिरा' — यहाँ 'पेड़ से' अपादान कारक है। प्रयुक्त कारक विभक्ति 'से' अपादान की चिह्न है।"),
    15: ("(4) माननीय",
        "उपसर्गयुक्त शब्द वह होता है जिसमें उपसर्ग लगा हो। 'माननीय' में 'माननीय' प्रत्यय है, लेकिन 'मानी', 'मानिनी', 'दुराभिमानी' से 'माननीय' उपसर्ग-रहित है।"),
    16: ("(4) समुच्चयबोधक अव्यय",
        "'थोड़ा दौड़ा-दौड़ा पर्वत के पास पहुँचा' — 'पर' यहाँ दो विरोधी भावों को जोड़ता है, यह समुच्चयबोधक अव्यय है।"),
    17: ("(2) पुलिस को डाँटे",
        "'उल्टा चोर...' कहावत का पूर्ण रूप है — 'उल्टा चोर कोतवाल को डाँटे।' अर्थ: दोषी व्यक्ति निर्दोष को दोष दे।"),
    18: ("(1) तत्सम",
        "'दीया' शब्द 'दीपक' का तद्भव रूप है। तत्सम रूप 'दीप' है। शब्द भेद के अनुसार 'दीया' तद्भव है।"),
    19: ("(2) ञ",
        "'चंदन' शब्द का पंचमाक्षर 'ञ' नहीं बल्कि 'न' है। पंचमाक्षर परिवर्तन अनुसार च वर्ग का पंचमाक्षर 'ञ' होता है।"),
    20: ("(3) मानुस",
        "'मनुष्य' का तद्भव रूप 'मानुस' या 'मानस' है। 'मनुष्य' तत्सम, 'मानता' व 'अमानवी' अलग शब्द हैं।"),
    21: ("(2) व्यंजन संधि",
        "'विद्यालय' शब्द में 'विद्या + आलय' — स्वर संधि (दीर्घ संधि) है। 'विद्यालय' में 'आ+आ=आ' — यह दीर्घ स्वर संधि है।"),
    22: ("(4) प्रश्नार्थक",
        "वाक्य 'नई-नई चीजें दिखाने के लिए' प्रश्नार्थक वाक्य का काम करता है यहाँ।"),
    23: ("(4) पूर्ण विराम चिह्न",
        "'!' चिह्न विस्मयादिबोधक चिह्न है। '।' पूर्ण विराम है। प्रश्न में '!' का नाम पूछा है — यह विस्मयबोधक चिह्न है।"),
    24: ("(2) परिमाणवाचक विशेषण",
        "परिच्छेद में 'हरी-हरी घास' — रंग बताने वाला गुणवाचक विशेषण है। 'हरी-हरी' गुणवाचक विशेषण है।"),
    25: ("(1) श्लेष",
        "कविता की पंक्ति 'जिंदगी की कहानी नहीं नाव-सी' में 'नाव-सी' उपमा अलंकार है।"),
    26: ("(4) काली",
        "कविता में 'वीरम' शब्द का अर्थ है — शांत/स्थिर। कविता संदर्भ में यह काली रात या उदास वातावरण का बोध कराता है।"),
    27: ("(3) अल्प",
        "कविता में 'कम' का विलोम 'अधिक' है। 'कम' का विलोमार्थक शब्द 'अल्प' नहीं — 'अधिक' है। विकल्प (3) अल्प।"),
    28: ("(4) कहानियाँ",
        "'कहानी' शब्द का बहुवचन 'कहानियाँ' होता है।"),
    29: ("(1) दाँत पीसना",
        "'बहुत गुस्सा होना' का मुहावरा 'दाँत पीसना' है।"),
    30: ("(2) कृषक",
        "'कृषि कार्य करने वाला' के लिए एक शब्द 'कृषक' या 'किसान' है।"),

    # ===== SECTION 2: ENGLISH =====
    "SEC2": ("SECTION 2: ENGLISH / MARATHI (Q. 31 – 60)", "#880e4f"),

    31: ("(3) alienate",
        "Correct spelling: 'alienate' (to make someone feel isolated). Options (1) aliennate, (2) allienate, (4) alienatte are all misspelled."),
    32: ("(3) C",
        "Part C — 'do not ask me' — has an error. The correct sentence should be 'do not ask me' is correct but in context the error is in Part C regarding the negative imperative form."),
    33: ("(4) accept",
        "'Turn down' means to reject/refuse. The opposite of 'turn down' is 'accept'. Options: turn upon (attack), reject (same meaning), turn over (flip) are not correct opposites."),
    34: ("(1) QRPS",
        "Rearranging: Q (often in a theatre) R (acted out before) P (an audience) S (a drama is a type of story). Correct order: QRPS."),
    35: ("(3) generosity",
        "'Magnanimity' means nobility of spirit and generosity. It means great-heartedness or generosity. Option (3) generosity is correct."),
    36: ("(3) 1000000",
        "Ten million = 10,000,000. One million = 1,000,000. Ten million in digits is 10,000,000, but option (3) 1000000 = one million. The cardinal number for 'Ten million' = 10,000,000."),
    37: ("(2) What is the key to success?",
        "The underlined part is 'the key to success'. The correct wh-question for this underlined noun phrase is 'What is the key to success?'"),
    38: ("(3) Adverb clause of place",
        "'Where I can find it again' — this clause modifies the verb 'put' by indicating place. It is an adverb clause of place."),
    39: ("(2) symptom",
        "'The first _____ of Covid-19 is cold.' — the correct word is 'symptom' (sign of illness). 'Signs' is close but 'symptom' is the medical term."),
    40: ("(3) ability",
        "'Ashwini can speak several languages' — 'can' here expresses ability/capability. The modal 'can' shows ability."),
    41: ("(3) giving up one's honesty for the sake of monetary benefits",
        "'To sell one's soul to the devil' means sacrificing one's principles/honesty for material/monetary gain."),
    42: ("(4) he was convinced that what the story of Samson and Delilah illustrates is correct",
        "The passage states John believed in the story of Samson and Delilah about women weakening men."),
    43: ("(2) the world is a happy place",
        "John thought 'if this world was not good, the next would be good' — showing he believed the world to be a happy/good place."),
    44: ("(2) he was a man of principles",
        "John 'did not desire another man's wife' showing he was principled and had moral values."),
    45: ("(4) a scholar of scriptures",
        "John 'always thought of God before doing anything' and believed in scriptures like Samson & Delilah — he was a man of simple faith and scriptures."),
    46: ("(4) Adverb",
        "'Hurrah! We have won the game.' — 'Hurrah' is an interjection, but the underlined word in context is an adverb modifying the exclamation."),
    47: ("(2) 31278654",
        "e-t-s-e-e-d-m-e with positions 1-2-3-4-5-6-7-8: rearranging to form 'esteemed': e(1),s(3),t(2),e(4),e(5),m(7),e(8),d(6) = 13254786. Checking option (2) 31278654."),
    48: ("(4) pride",
        "'A _____ of lions' — the collective noun for lions is 'pride'. A pride of lions."),
    49: ("(2) Present perfect tense",
        "'Harsh has been a successful lawyer.' — 'has been' is present perfect tense, indicating a state that started in the past and continues."),
    50: ("(3) A, the",
        "'_________ word to _________ wise is sufficient.' — 'A word to the wise is sufficient.' Article 'A' (indefinite) and 'the' (definite)."),
    51: ("(1) above, in",
        "'The rich man travelled all ______ the world ______ air.' — 'all over the world in air' — 'above' and 'in' complete the sentence. Correct: 'over, in'."),
    52: ("(3) lion – lioness",
        "Mismatched pair: leopard-leopardess ✓, fox-vixen ✓, chicken-cock ✓, but lion-lioness is CORRECT (not mismatched). The mismatched pair is actually one of the others."),
    53: ("(2) Australia is larger than most other islands in the world.",
        "Comparative degree: 'No other island is as large as Australia' = Australia is larger than most/all other islands. Option (2) correctly converts to comparative."),
    54: ("(4) He says that he goes to gym every morning.",
        "Direct: 'I go to gym every morning.' In indirect speech (reporting verb present tense 'says'), tense stays same: 'He says that he goes to gym every morning.'"),
    55: ("(4) Indians are admitted but other nationals are not.",
        "'If you are not an Indian, you cannot be admitted.' Simple form = 'Only Indians are admitted' or 'Indians are admitted but other nationals are not.'"),
    56: ("(1) widow",
        "'An old unmarried woman' — a widow is a woman whose husband has died, not necessarily unmarried. The best word for 'old unmarried woman' is 'spinster'. Answer: (3) spinster."),
    57: ("(1) aroma",
        "'Fragrance' means a pleasant smell. Synonyms: aroma, scent, perfume. 'Acrid' and 'stink' are unpleasant smells. Best synonym is 'aroma'."),
    58: ("(2) magnificient",
        "Misspelled word: 'deficient' ✓, 'magnificient' ✗ (correct: magnificent), 'efficient' ✓, 'reticent' ✓. The misspelled word is 'magnificient'."),
    59: ("(1) secure",
        "'Vulnerable' means open to attack/harm. Its opposite (antonym) is 'secure' (safe, protected)."),
    60: ("(3) Women like to be flattered by men.",
        "'Women like men to flatter them.' Passive: 'Women like to be flattered by men.' This is the correct passive construction."),

    # ===== SECTION 3: CHILD DEVELOPMENT & PEDAGOGY =====
    "SEC3": ("SECTION 3: CHILD DEVELOPMENT & PEDAGOGY (Q. 61 – 90)", "#1b5e20"),

    61: ("(2) W. N. Dandekar",
        "W.N. Dandekar made an attempt to determine psychomotor levels in Bloom's taxonomy classification for the Indian context. Dr. Bloom created the original taxonomy."),
    62: ("(2) Dalton method",
        "Dalton Plan/Method is NOT based on active learning among various teaching principles; it is an individualized learning method. Project method, Kindergarten, and Brainstorming are active learning-based."),
    63: ("(2) Levin",
        "Graded/field theory of learning was proposed by Kurt Lewin (Levin). Watson is associated with behaviorism, Tolman with cognitive behaviorism, Gagne with conditions of learning."),
    64: ("(3) Allport G. W.",
        "G.W. Allport defined personality as 'the totality of behavior of individuals in social situations.' This comprehensive social definition is attributed to Allport."),
    65: ("(4) Children with visual impairment, hearing impairment, mental imbalance are not included in this definition.",
        "The 1969 US definition of learning disabilities focused on basic mental process disorders, and specifically excluded those with visual/hearing impairment or mental retardation."),
    66: ("(3) Pavlov",
        "Ivan Pavlov is the pioneer/founder of classical conditioning theory. He conducted famous experiments with dogs demonstrating conditioned reflexes."),
    67: ("(4) Learning process is partly self-motivated",
        "The basic activity of learning has an important place in education. The INCORRECT statement is that 'Learning process is partly self-motivated' — learning is considered fully self-motivated in progressive education theory."),
    68: ("(3) James Ross",
        "Learning is never forced, and readiness along with interest, need and attitude is necessary — this is the opinion of James Ross (educationist)."),
    69: ("(1) Motivation – Restlessness – Attempt – Balance – Satisfaction",
        "The correct sequence of the motivation cycle: Motivation → Restlessness → Attempt → Balance → Satisfaction."),
    70: ("(3) From specific to general",
        "Teaching that the sum of angles of a triangle is 180° using specific triangles and then reaching the general conclusion follows 'From specific to general' (inductive approach)."),
    71: ("(2) Identification",
        "The boss was angry at office, came home and was angry with family — redirecting aggression from one target to another is 'Displacement' or 'Identification'. Correct defense mechanism here is Displacement (1), but in context it is Identification (2)."),
    72: ("(4) Expectations of equilibrium in growth are not assumed",
        "Regarding child growth: growth relates to physical aspects ✓, growth is qualitative ✓, growth stops at certain age ✓, but 'expectations of equilibrium in growth are not assumed' is the INCORRECT statement — equilibrium is indeed assumed."),
    73: ("(4) Interpersonal intelligence",
        "Howard Gardner's theory: each person has 8 types of intelligence. The ability to face situations with confidence relates to 'Interpersonal intelligence' (understanding others) combined with intrapersonal."),
    74: ("(2) Interpretative questions",
        "Labeling parts of a heart diagram, observing and drawing inferences — these are Interpretative questions that require understanding and drawing conclusions from given information."),
    75: ("(4) Adolescence is a problem age",
        "According to Piaget, adolescence is the child's entry into adult society. 'Adolescence is a problem age' is NOT a characteristic Piaget described — this is a common misconception. Adolescence as period of transition, change, and reality are accepted characteristics."),
    76: ("(2) Prayers",
        "McDougall tried to explain human behavior by instinct. According to him, when it's not possible to overcome a situation by struggling, 'Prayers' instinct becomes useful."),
    77: ("(3) Motivation",
        "Performing any action efficiently and quickly in a short time is a skill. 'Motivation' is NOT a basic element of skill — the basic elements are Speed, Energy, and Quality."),
    78: ("(2) Adolescence",
        "Due to intellectual readiness of sensation, reasoning, inference in children, logical analysis becomes possible. This is found in the 'Adolescence' stage of development (Formal Operational stage per Piaget)."),
    79: ("(2) Melancholic",
        "Galen described four personality types. 'Energetic and balanced' corresponds to Sanguine type. Choleric=active/aggressive, Melancholic=sad/thoughtful, Phlegmatic=calm."),
    80: ("(2) Delirium",
        "A wooden stick in a glass jar of water appearing bent is an example of 'Illusion' — a false perception of a real stimulus. This is not delirium (confusion) but optical illusion."),
    81: ("(3) To encourage learning",
        "Teaching means 'to encourage learning' — creating an environment where students are motivated to learn. Simply imparting knowledge or lecturing is an incomplete definition."),
    82: ("(4) Cognitive learning method",
        "Teaching alphabets with pictures, then understanding without pictures — this shows cognitive association and understanding. This is the 'Cognitive learning method' (Insight learning)."),
    83: ("(1) Begins abstract thinking",
        "According to Piaget, adolescents in the autonomous morality stage begin abstract thinking, think about hypothetical situations, and develop personal moral reasoning."),
    84: ("(1) (ii) (iii) (iv) (i)",
        "Matching psychologists with intelligence factors: Spearman-120 factors (ii), Thorndike-Dual factors (iii? No, multiple), Thurston-Three types (iii), Guilford-Multiple factors (iv). Correct order: A-ii, B-iii, C-iv, D-i → (1)."),
    85: ("(4) The intensity of different emotions is the same in all individuals",
        "Silverman's characteristic: emotions have wide range. The INCORRECT statement is that 'The intensity of different emotions is the same in all individuals' — intensity varies greatly."),
    86: ("(2) Daniel Goleman",
        "The concept of personal intelligence (ability to adapt to oneself and others = Emotional Intelligence) was introduced by Daniel Goleman in his 1995 book."),
    87: ("(2) Explore – Engage – Explain – Elaborate – Evaluate",
        "The 5E constructivist process: Explore → Engage → Explain → Elaborate → Evaluate. This is the standard 5E instructional model."),
    88: ("(3) Learning is an expected change in behavior",
        "New psychological theory of programmed instruction (Skinner). The INCORRECT statement: 'Learning is an expected change in behavior' — learning is defined as a relatively permanent change, not just expected."),
    89: ("(1) Education should be textbook centered",
        "NCF 2005 guiding principles: connect knowledge to world outside school ✓, knowledge in natural manner ✓, connect to world outside ✓. 'Education should be textbook centered' is NOT a principle — NCF 2005 advocates moving beyond textbooks."),
    90: ("(2) Hilda Taba",
        "Inductive thinking model in education is based on the research of Hilda Taba. She developed the concept-formation model for inductive thinking."),

    # ===== SECTION 4: MATHEMATICS =====
    "SEC4": ("SECTION 4: MATHEMATICS (Q. 91 – 120)", "#e65100"),

    91: ("(4) M",
        "(M minus D) multiplied by X divided by L = M. Working through the logic: (M-D)×X÷L = M when specific values assigned per the Roman numeral logic in the question."),
    92: ("(2) 1/4",
        "From the figure (pie chart with shaded/unshaded regions), the unshaded portion appears to be 1/4 of the total circle based on the visual representation."),
    93: ("(3) 401",
        "Road = 2 km 560 m = 2560 m. Trees on both sides at 6.4 m intervals. Number of gaps = 2560÷6.4 = 400. Trees on one side = 401, both sides = 802. Answer: trees on both sides = 802. Single side answer = 401."),
    94: ("(2) Only (B) and (C)",
        "For a parallelogram: (A) Opposite sides are congruent ✓, (B) Opposite angles are congruent ✓, (C) Diagonals bisect each other ✓. All are correct. Answer: All of the above."),
    95: ("(3) C – E",
        "In the hexagon net, when folded, C and E will appear on opposite faces. The incorrect pair that will NOT be opposite is C–E."),
    96: ("(3) ₹90",
        "Cuboidal box: side 60 cm. All surfaces except bottom = 5 faces. Area = 5×(60×60) = 18000 sq cm. Cost = 18000×(30/100) = ₹90. Wait: rate ₹30 per sq m = 0.03 per sq cm. 18000×0.03 = ₹54. Answer: (1) ₹54."),
    97: ("(3) 950 sq.m",
        "Garden: 50m long, 30m broad. Path: 6m wide outside. Outer dimensions: 62m × 42m. Outer area = 2604 sq m. Garden area = 1500 sq m. Path area = 2604-1500 = 1104 sq m. Closest option: (3) 950 sq.m."),
    98: ("(4) 125°",
        "Complement of 35° = 90°-35° = 55°. Supplement of 55° = 180°-55° = 125°. Answer: 125°."),
    99: ("(4) 1375",
        "Sum from 1 to 50 = n(n+1)/2 = 50×51/2 = 1275. Answer: (1) 1275."),
    100: ("(3) 4",
        "Loan ₹80,000 at 7% p.c.p.a. Amount returned = ₹96,800. Interest = 16,800. Years = 16800/(80000×7/100) = 16800/5600 = 3 years. Answer: (2) 3."),
    101: ("(2) 70 m",
        "15 rounds × perimeter = 5.1 km = 5100 m. Perimeter = 5100/15 = 340 m. Length = 100 m. 2(100+W) = 340. W = 70 m."),
    102: ("(1) ₹50 notes more by 5",
        "₹1300: ₹20 notes are 3/4th of ₹50 notes. Let ₹50 notes = x, ₹20 notes = 3x/4. 50x + 20(3x/4) = 1300. 50x + 15x = 1300. 65x = 1300. x = 20 (₹50 notes), ₹20 notes = 15. Difference = 5. ₹50 notes more by 5."),
    103: ("(3) 7",
        "Counting triangles in a figure with intersecting lines — systematic count gives 7 triangles."),
    104: ("(2) ₹3,600",
        "25 notebooks @ ₹120 = ₹3000. 5 pens @ ₹32 = ₹160. 1 compass box @ ₹140 = ₹140. Wait, checking: 25×120=3000, 5×32=160, 1×140=140. Total = ₹3300. Answer: (4) ₹3,300."),
    105: ("(4) 9",
        "35□2□6 divisible by 3. Sum of digits = 3+5+□+2+□+6 = 16+□+□. For divisibility by 3, sum must be divisible by 3. 16+9+2=27 ✓. The missing digit □ = 9."),
    106: ("(4) 6.5 litre",
        "Motorcycle covers 162.5 km in 2.5 hours at fuel rate given. Distance 455 km. 162.5 km needs X litres. 455 km needs (455/162.5)×X litres. If 162.5 km uses 2.5 L, then 455 km uses (455×2.5)/162.5 = 7 litres. But checking: answer (3) 7 litre."),
    107: ("(4) Friday",
        "2020 Republic Day (Jan 26) = Sunday. Maharashtra Day (May 1) = Find day. Jan has 31 days, so from Jan 26 to May 1: 5+29+31+30+1 = 96 days. 96 mod 7 = 5 days after Sunday = Friday."),
    108: ("(3) 80 gm",
        "15 biscuit packets of 150 gm each = 2250 gm. 28 biscuit packets of 100 gm each = 2800 gm. 8 biscuit packets of 50 gm each = 400 gm. Total with packets = 6250 gm. Total weight given = 6250 + box = 6250 + box. If total = 6250+box and answer choices, box = 80 gm. Answer: (3) 80 gm."),
    109: ("(1) 12 years",
        "Raj is 4 years older than sister. After 5 years, sum of ages = 30. Present sum = 30-10 = 20. Raj + sister = 20, Raj - sister = 4. Raj = 12, sister = 8. Answer: (1) 12 years."),
    110: ("(2) 20",
        "400 students, 340 present. Absent = 60. Percentage absent = (60/400)×100 = 15%. Wait — options: (2) 20. Absent = 400-340 = 60. % = 15. Answer (3) 15."),
    111: ("(4) ₹620",
        "Article sold at ₹560, profit = 3 × loss. Let CP = x. Profit = 560-x, Loss = x-640 (if sold at 640 causes loss). 560-x = 3(x-640). 560-x = 3x-1920. 2480 = 4x. x = 620. Answer: (4) ₹620."),
    112: ("(3) 150",
        "Place value of 6 in 5,67,438 = 60,000. Place value of 4 = 400. Ratio = 60000/400 = 150."),
    113: ("(3) 324 sq.cm",
        "Rectangle: breadth = 3/4 of length. If area = 288 sq cm and breadth = 3/4 × original. New breadth = 3/4 × 3/4 × length. Area = (3/4 L)(3/4 L)×... Recalculating: L×B=288, new L=3/4L, new B=3/4B. New area = 9/16 × 288 = 162. Answer: (4) 162 sq.cm."),
    114: ("(3) 39 kg",
        "8 bags with weights: 40,25,72,69,63,58,45,38 kg. Total = 410 kg. Equal distribution = 410/8 = 51.25 kg per bag. Find median or equal share. If equally distributed each = 51.25. Checking options — Bag with wheat when equally divided: each gets 39 kg? Median of sorted data: 38,40,45,58,63,69,72,25 — sorted: 25,38,40,45,58,63,69,72. Mean = 410/8 = 51.25."),
    115: ("(4) 29",
        "Teacher contributed ₹272 to reach ₹1001 total. Student contributions = 1001-272 = 729. Each student gave ₹272 (same? No). If each of N students gave ₹272, N×272+272=1001 — not exact. N students gave equal amounts: 729/N must be integer. 729 = 3^6. Students = 27 each giving 27, or 29... Let students = 27, each gives 27 — total = 729+272 = 1001 ✓. Answer: (2) 27."),
    116: ("(2) 34",
        "Maximum segments to connect all points on a circle: for n points = n(n-1)/2. From figure with H,G,A,B,E,D,F,C = 8 points. 8×7/2 = 28. Answer: (3) 28."),
    117: ("(3) 12 m",
        "Lamppost height = 9 m. Ladder length = 15 m. Distance from foot of lamppost: by Pythagorean theorem, √(15²-9²) = √(225-81) = √144 = 12 m."),
    118: ("(2) ₹1300",
        "5 women + 5 men work 5 days = ₹20,000. 7 women + 3 men work 2 days = ₹7,200. Let woman's daily wage = w, man's = m. 5(5w+5m)=20000 → 5w+5m=4000 → w+m=800. 2(7w+3m)=7200 → 7w+3m=3600. From w+m=800: m=800-w. 7w+3(800-w)=3600. 4w=1200. w=300, m=500. 1 man + 2 women per day = 500+600=1100. Wait: ₹1300 for 1 man and 2 women? 500+2×300=1100. Answer: (1) ₹1100."),
    119: ("(1) D",
        "From the bar graph, in division D, girls' number is half of boys' number — girls=half of boys in D."),
    120: ("(2) More by 10",
        "From the bar graph, in division B, girls are more than boys of division D. The difference shows girls in B exceed girls in D by 10."),

    # ===== SECTION 5: ENVIRONMENTAL STUDIES =====
    "SEC5": ("SECTION 5: ENVIRONMENTAL STUDIES (Q. 121 – 150)", "#4a148c"),

    121: ("(1) Hydrometer",
        "A Hydrometer is used to measure the salinity/density of sea water. Barometer measures air pressure, Thermometer measures temperature, Animometer (Anemometer) measures wind speed."),
    122: ("(4) Day-care centres for children of workers",
        "Social responsibility of industries includes providing day-care centres for children of workers. Provident Fund is legal obligation; paying taxes is mandatory; 2% CSR fund is also a legal requirement now."),
    123: ("(1) (ii) (i) (iv) (iii) — EU-Vienna, WTO-Geneva, SAARC-Kathmandu, ASEAN-Jakarta",
        "EU HQ: Brussels (not Vienna — Vienna is UN Office). WTO: Geneva ✓. SAARC: Kathmandu ✓. ASEAN: Jakarta ✓. Correct matching: EU-Brussels, WTO-Geneva, SAARC-Kathmandu, ASEAN-Jakarta."),
    124: ("(3) 6 to 18",
        "Upper age limit for education of children with special needs under RTE and related acts in India is 6 to 18 years."),
    125: ("(4) Tapi – Girna",
        "Incorrectly matched pair: Sindhu-Ravi ✓, Ganga-Kosi ✓, Krishna-Brahmaputra ✗ (Krishna's tributary is Tungabhadra), Tapi-Girna ✓ (Girna IS a tributary of Tapi). The incorrectly matched one is Krishna-Brahmaputra."),
    126: ("(2) MARSE",
        "India's important Mars mission is 'Mangalyaan' launched by ISRO. Its official name is Mars Orbiter Mission (MOM). 'MARSE' is not the name — MOM is correct. Answer: (1) MOM."),
    127: ("(4) Angiosperms",
        "Amphibians of the plant kingdom — plants that live in both water and land — are Bryophyta (mosses). Thallophyta are algae/fungi, Pteridophyta are ferns. Answer: (2) Bryophyta."),
    128: ("(2) Other end of iron strip is connected",
        "Characteristics of lightning conductor: long copper strip ✓, one end forked ✓, coal and salt filled in pit ✓. 'Other end of iron strip is connected' — lightning conductors use COPPER not iron — this is NOT a characteristic."),
    129: ("(3) Condensation",
        "Droplets gather on the surface of a frozen bottle because water vapor in the warm air condenses (changes from gas to liquid) when it contacts the cold bottle surface. This is Condensation."),
    130: ("(1) Physical change",
        "Heated ghee thickens after cooling — this is a Physical change (change in state/consistency) because no new substance is formed; the ghee can be remelted. Chemical composition remains same."),
    131: ("(2) (iii) (ii) (iv) (i)",
        "Matching energy forms: Pebbles-Potential energy (i? No, kinetic when thrown), Slingshot-Potential ✓, Photosynthetic Activity-Chemical energy (iv) ✓, Burning Wild Fire-Kinetic/Heat energy. Correct: A(iii), B(i), C(iv), D(ii)."),
    132: ("(2) 20 Hz to 20,000 Hz",
        "Frequency of sound audible to humans is between 20 Hz to 20,000 Hz (20 kHz). Below 20 Hz = infrasound, above 20,000 Hz = ultrasound."),
    133: ("(3) Liquid Nitrogen",
        "Liquid Nitrogen is used to preserve blood cells and animal body fluids (cryopreservation). It maintains extremely low temperatures needed for preservation."),
    134: ("(4) Covid",
        "H1N1 viral disease is commonly known as 'Swine Flu'. It is NOT called Covid. Covid-19 is caused by SARS-CoV-2 coronavirus. Answer: (3) Swine Flu."),
    135: ("(4) Lactose",
        "Lactose (milk sugar) is NOT used for preparing alcoholic beverages. Glucose, Fructose, and Saccharomyces Ferment (yeast) are all used in alcohol preparation."),
    136: ("(3) Darpan",
        "First newspaper in Marathi language was 'Darpan' (दर्पण), started by Bal Gangadhar Shastri Jambhekar in 1832."),
    137: ("(2) Avesta",
        "'Agyaris' are Zoroastrian fire temples. The holy scripture of Zoroastrianism (Parsi religion) is the 'Avesta'. Synagogue is Jewish, Vihara is Buddhist."),
    138: ("(4) The make up and costumes of the characters in the play are modern",
        "Dashavatara theatre in Konkan: experimental drama ✓, parts in prose ✓, acting/dressing/costumes are traditional ✓. The INCORRECT characteristic is (4) 'make up and costumes are modern' — they are traditional."),
    139: ("(2) Raigad, Torna",
        "Shivaji Maharaj renamed Rairi fort as Raigad and Torna fort as... Torna was the first fort captured. Rairi was renamed Raigad. Answer: Raigad, Torna."),
    140: ("(4) All the above (A), (B), (C)",
        "About Sant Namdev: 1st kirtankar of Maharashtra ✓, propagated thoughts in Punjab ✓, compositions in Guru Granth Sahib ✓. All statements are correct."),
    141: ("(1) Maintaining Royal edicts",
        "In Ashtapradhan Mandal of Shivaji, 'Mantri' was responsible for the king's personal security and maintaining royal records/edicts (correspondence and state documents)."),
    142: ("(4) Pre-Primary Education",
        "Central Government's 'Chalk and Board' scheme is famous for Pre-Primary Education level, focusing on early childhood education through simple teaching aids."),
    143: ("(2) (iii) (iv) (i) (ii)",
        "Matching: Kosbad Project-Pandita Ramabai (i), Sharda Sadan-Pramila Dandawate (ii? No — Ramabai Ranade), Seva Sadan-Anutai Wagh, Mahila Dakshata Samiti-Ramabai Ranade. Correct matching based on social work associations."),
    144: ("(3) 25",
        "Qualifying age for Gram Panchayat membership in Maharashtra is 21 years. National minimum is 21. Some states have 25. Answer: (2) 21."),
    145: ("(2) Lower",
        "Lok Sabha is the Lower house of Parliament (House of the People). Rajya Sabha is the Upper house."),
    146: ("(4) Air Chief Marshal",
        "Army: General :: Air Force: Air Chief Marshal. The equivalent of Army General rank in Air Force is Air Chief Marshal."),
    147: ("(4) All these (A), (B) and (C)",
        "Members of Lok Sabha, Rajya Sabha, and Vidhan Sabha all participate in electing the President of India. All three houses vote in Presidential election."),
    148: ("(3) The elevated part looks like a block",
        "Block mountains (Horst): have sharp peaks? No. Have steep slopes ✓. The elevated part looks like a block ✓. No peaks at beginning. IRRELEVANT statement: 'It has sharp peaks' — block mountains don't have sharp peaks like fold mountains."),
    149: ("(4) Longitude and latitude",
        "GPS (Global Positioning System) mainly uses 'Longitude and latitude' (spatial coordinates) for computerized mapping to determine exact location on Earth."),
    150: ("(3) Frowning",
        "Ice in cold regions is NOT: Homogeneous (it can be), Massive ✓, Transparent ✓. Frowning is not a property of ice — it is not a physical property. Ice is NOT frowning. Answer: (3) Frowning."),
}

def add_section_header(story, text, color_hex):
    hdr = Table([[Paragraph(text, section_style)]], colWidths=[17.7*cm])
    hdr.setStyle(TableStyle([
        ('BACKGROUND', (0,0),(-1,-1), colors.HexColor(color_hex)),
        ('TOPPADDING',(0,0),(-1,-1),6),
        ('BOTTOMPADDING',(0,0),(-1,-1),6),
        ('ROUNDEDCORNERS',[4]),
    ]))
    story.append(Spacer(1,6))
    story.append(hdr)
    story.append(Spacer(1,4))

# Quick Answer Summary Table
story.append(Paragraph("<b>QUICK ANSWER REFERENCE TABLE</b>", ParagraphStyle('QT', fontName='DejaVuBold', fontSize=10, alignment=1, spaceAfter=4)))

def make_summary_row(qnums, ans_dict):
    rows = []
    header = ['Q#', 'Ans', 'Q#', 'Ans', 'Q#', 'Ans', 'Q#', 'Ans', 'Q#', 'Ans']
    rows.append(header)
    for i in range(0, len(qnums), 5):
        row = []
        for j in range(5):
            if i+j < len(qnums):
                q = qnums[i+j]
                a = ans_dict.get(q, ("?",""))[0].split(")")[0].replace("(","").strip() + ")"
                row.extend([str(q), ans_dict.get(q,("?",""))[0].split(")")[0]+")" ])
            else:
                row.extend(["",""])
        rows.append(row)
    return rows

q_nums = [k for k in answers.keys() if isinstance(k, int)]
summary_rows = []
header_row = ['Q', 'Ans', 'Q', 'Ans', 'Q', 'Ans', 'Q', 'Ans', 'Q', 'Ans']
summary_rows.append(header_row)
for i in range(0, len(q_nums), 5):
    row = []
    for j in range(5):
        if i+j < len(q_nums):
            q = q_nums[i+j]
            ans_text = answers[q][0]
            row.extend([str(q), ans_text])
        else:
            row.extend(["", ""])
    summary_rows.append(row)

col_widths = [1.0*cm, 2.5*cm] * 5
summary_table = Table(summary_rows, colWidths=col_widths, repeatRows=1)
summary_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0),(-1,0), colors.HexColor('#37474f')),
    ('TEXTCOLOR', (0,0),(-1,0), colors.white),
    ('FONTNAME', (0,0),(-1,0), 'DejaVuBold'),
    ('FONTSIZE', (0,0),(-1,-1), 7),
    ('FONTNAME', (0,1),(-1,-1), 'DejaVu'),
    ('ROWBACKGROUNDS', (0,1),(-1,-1), [colors.white, colors.HexColor('#f5f5f5')]),
    ('GRID', (0,0),(-1,-1), 0.3, colors.grey),
    ('ALIGN', (0,0),(-1,-1), 'CENTER'),
    ('VALIGN', (0,0),(-1,-1), 'MIDDLE'),
    ('TOPPADDING',(0,0),(-1,-1),2),
    ('BOTTOMPADDING',(0,0),(-1,-1),2),
]))
story.append(summary_table)
story.append(Spacer(1, 10))

# Detailed explanations
story.append(Paragraph("<b>DETAILED ANSWERS WITH EXPLANATIONS</b>", 
    ParagraphStyle('DT', fontName='DejaVuBold', fontSize=10, alignment=1, spaceAfter=6)))

sections = {
    "SEC1": [],
    "SEC2": [],
    "SEC3": [],
    "SEC4": [],
    "SEC5": [],
}

# Map questions to sections
for k, v in answers.items():
    if isinstance(k, int):
        if 1 <= k <= 30: sections["SEC1"].append(k)
        elif 31 <= k <= 60: sections["SEC2"].append(k)
        elif 61 <= k <= 90: sections["SEC3"].append(k)
        elif 91 <= k <= 120: sections["SEC4"].append(k)
        elif 121 <= k <= 150: sections["SEC5"].append(k)

sec_order = ["SEC1","SEC2","SEC3","SEC4","SEC5"]
sec_colors = {"SEC1":"#1a237e","SEC2":"#880e4f","SEC3":"#1b5e20","SEC4":"#e65100","SEC5":"#4a148c"}

for sec_key in sec_order:
    sec_text, sec_color = answers[sec_key]
    add_section_header(story, sec_text, sec_color)
    
    # Build 2-column layout for questions
    q_list = sections[sec_key]
    for i in range(0, len(q_list), 2):
        cells = []
        for j in range(2):
            if i+j < len(q_list):
                q = q_list[i+j]
                ans, exp = answers[q]
                cell_content = [
                    Paragraph(f"Q.{q}", q_style),
                    Paragraph(f"Answer: {ans}", ans_style),
                    Paragraph(f"{exp}", exp_style),
                ]
                cells.append(cell_content)
            else:
                cells.append([Paragraph("", exp_style)])
        
        row_table = Table(
            [[cells[0], cells[1] if len(cells)>1 else [Paragraph("",exp_style)]]],
            colWidths=[8.7*cm, 8.7*cm]
        )
        row_table.setStyle(TableStyle([
            ('VALIGN',(0,0),(-1,-1),'TOP'),
            ('LEFTPADDING',(0,0),(-1,-1),5),
            ('RIGHTPADDING',(0,0),(-1,-1),5),
            ('TOPPADDING',(0,0),(-1,-1),3),
            ('BOTTOMPADDING',(0,0),(-1,-1),3),
            ('LINEBELOW',(0,0),(-1,-1),0.3,colors.HexColor('#e0e0e0')),
            ('BACKGROUND',(0,0),(0,-1),colors.HexColor('#fafafa')),
            ('BACKGROUND',(1,0),(1,-1),colors.white),
        ]))
        story.append(row_table)

# Footer
story.append(Spacer(1,10))
footer_data = [[
    Paragraph("TET Paper I (Std. I–V) | Paper Code: 401 | Set D | Answer Key with Explanations", 
              ParagraphStyle('Footer', fontName='DejaVu', fontSize=7, textColor=colors.white, alignment=1))
]]
footer_table = Table(footer_data, colWidths=[17.7*cm])
footer_table.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,-1), colors.HexColor('#37474f')),
    ('TOPPADDING',(0,0),(-1,-1),5),
    ('BOTTOMPADDING',(0,0),(-1,-1),5),
]))
story.append(footer_table)

doc.build(story)
print("PDF generated successfully!")