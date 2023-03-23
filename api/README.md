# QueryParser

Install Python 3.7

### Run following commands
 
 pip install requirements.txt
 
 python -m spacy download en
 <!--  python -m spacy download en_core_web_lg -->
 uvicorn main:app --reload

### API URL
  
	http://127.0.0.1:8000/pre_process_query?text= Best burger best pizza
### Method: GET

### API Response
[
   
	 {
        "review_type": "FOOD",
        "text": "burger",
        "sentiment_text": "Best",
        "sentiment": "POSITIVE"
    },
		
    {
        "review_type": "FOOD",
        "text": "pizza",
        "sentiment_text": "best",
        "sentiment": "POSITIVE"
    }
		
]
