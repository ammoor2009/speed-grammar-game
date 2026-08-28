import json
import random
from camel_tools.disambig.mle import MLEDisambiguator
from camel_tools.tokenizers.word import simple_word_tokenize

# 1. تحميل المحلل الصرفي لـ CAMeL Tools
mle = MLEDisambiguator.pretrained()

# 2. بنك النصوص الأدبية والنقدية (يمكنك زيادة الجمل هنا بحرية)
sentences = [
    "القصيدةُ الجاهليةُ مليئةٌ بالصورِ الفنيةِ.",
    "الناقدُ المتعمقُ يفككُ الخطابَ السرديَّ.",
    "الدراسةُ البلاغيةُ دقيقةٌ في تحليلِ التبئيرِ.",
    "الباحثونَ المتميزونَ يستنطقونَ النصَّ الأدبيَّ.",
    "الشاعرةُ المبدعةُ تلقي القصيدةَ برصانةٍ.",
    "المخطوطةُ القديمةُ محققةٌ بعنايةٍ فائقةٍ.",
    "الروائيُ البارعُ يوظفُ الفضاءَ المكانيَّ."
]

questions_bank = []

# 3. تحليل الجمل بواسطة CAMeL Tools واستخراج الأسئلة
for sentence in sentences:
    tokens = simple_word_tokenize(sentence)
    disambig = mle.disambiguate(tokens)
    
    for i, (word, d) in enumerate(zip(tokens, disambig)):
        feats = d.selected_features
        pos = feats.get('pos')  # نوع الكلمة (adj = صفة)
        gen = feats.get('gen')  # الجنس (m = مذكر, f = مؤنث)
        
        # استهداف الصفات لبناء مطابقة النعت والمطابق
        if pos == 'adj':
            correct_word = word
            
            # توليد الخيار الخاطئ نحوياً بعكس التذكير والتأنيث
            if gen == 'f':
                wrong_word = word.replace('ة', '').replace('ية', 'ي')
            else:
                wrong_word = word + 'ة' if not word.endswith('ٌ') else word[:-1] + 'ةٌ'
                
            # بناء السؤال واستبدال الكلمة المستهدفة بـ ___
            q_tokens = tokens.copy()
            q_tokens[i] = "___"
            q_text = " ".join(q_tokens)
            
            questions_bank.append({
                "q": q_text,
                "options": [correct_word, wrong_word],
                "answer": correct_word
            })

# 4. حفظ الأسئلة في ملف JSON
with open('easy_bank.json', 'w', encoding='utf-8') as f:
    json.dump(questions_bank, f, ensure_ascii=False, indent=4)

print(f"✅ تم توليد {len(questions_bank)} سؤالاً بنجاح بواسطة CAMeL Tools.")
