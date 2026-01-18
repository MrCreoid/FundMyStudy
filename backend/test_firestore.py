from google.cloud import firestore

db = firestore.Client(project="fundmystudy-527")

profile = db.collection("profiles").document("eDYCUg5suEPgPVOZLysl1qyIqNR2").get()

if profile.exists:
    print(profile.to_dict())
else:
    print("Profile document does not exist")
