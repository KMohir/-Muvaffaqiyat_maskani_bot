# from fuzzywuzzy import fuzz

# def recognize_question(question,questions):
#     recognized={'id':'','percent':0}
#     for key, value in questions.items():
#         for q in value:
#             percent=fuzz.ratio(question,q)
#             if percent>recognized['percent']:
#                 recognized['id']=key
#                 recognized['percent']=percent
#     return recognized['id']