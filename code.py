from tkinter import *
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize
from langdetect import detect

a=Tk()
a.title('tk')
a.geometry('750x500')
z=Label (a, text="TEXT SUMMARIZER", font="none 24 bold")
z.config(anchor=CENTER)
z.pack()

text = Text(a, width=80, height=20)
text.pack()
Label(a,text=" ").pack()
Label(a,text='Summarized text✔',font="none 18 bold").pack()

s = Text(a, width=80, height=20)
s.pack()
def p():
    thetext = text.get('1.0', 'end')
    text_str = thetext
    if(detect(text_str)=='ta'):
        a=[]
        with open('tamil Stop words.txt', 'r', encoding='utf-8') as f:
            a+=f.readlines()
            f.close()
        for i in range(0,len(a)):
            a[i]=a[i].rstrip('\n')
        stopWords = a
    elif(detect(text_str)=='en'):
        stopWords = set(stopwords.words("english"))
    elif(detect(text_str)=='hi'):
        a=[]
        with open('hindi stopwords.txt', 'r', encoding='utf-8') as f:
            a+=f.readlines()
        f.close()
        for i in range(0,len(a)):
            a[i]=a[i].rstrip('\n')
        stopWords = a
    def _create_frequency_table(text_string) -> dict:
    
    
        words = word_tokenize(text_string)
        ps = PorterStemmer()

        freqTable = dict()
        for word in words:
            word = ps.stem(word)
            if word in stopWords:
                continue
            if word in freqTable:
                freqTable[word] += 1
            else:
                freqTable[word] = 1

        return freqTable


    def _score_sentences(sentences, freqTable) -> dict:
    

        sentenceValue = dict()

        for sentence in sentences:
            word_count_in_sentence = (len(word_tokenize(sentence)))
            word_count_in_sentence_except_stop_words = 0
            for wordValue in freqTable:
                if wordValue in sentence.lower():
                    word_count_in_sentence_except_stop_words += 1
                    if sentence in sentenceValue:
                        sentenceValue[sentence] += freqTable[wordValue]
                    else:
                        sentenceValue[sentence] = freqTable[wordValue]

            if sentence in sentenceValue:
                sentenceValue[sentence] = sentenceValue[sentence] / word_count_in_sentence_except_stop_words

        
        
        return sentenceValue
    


    def _find_average_score(sentenceValue) -> int:
    
        sumValues = 0
        for entry in sentenceValue:
            sumValues += sentenceValue[entry]

    # Average value of a sentence from original text
        average = (sumValues / len(sentenceValue))

        return average


    def _generate_summary(sentences, sentenceValue, threshold):
        sentence_count = 0
        summary = ''

        for sentence in sentences:
            if sentence in sentenceValue and sentenceValue[sentence] >= (threshold):
                summary += " " + sentence
                sentence_count += 1

        return summary


    def run_summarization(text):
    # 1 Create the word frequency table
        freq_table = _create_frequency_table(text)

    

    # 2 Tokenize the sentences
        sentences = sent_tokenize(text)

    # 3 Important Algorithm: score the sentences
        sentence_scores = _score_sentences(sentences, freq_table)

    # 4 Find the threshold
        threshold = _find_average_score(sentence_scores)

    # 5 Important Algorithm: Generate the summary
        summary = _generate_summary(sentences, sentence_scores, 1.0 * threshold)

        return summary


    
    result = run_summarization(text_str)
    
    s.insert(INSERT,result)

Button(a,text='Text Ranking Summarize',command=p).pack()


a.mainloop()
