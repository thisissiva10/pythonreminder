
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer


row=0

def fillDays():
	day=[]

	day.append("today")
	day.append("tommorow")
	day.append("dayaftertommorow")
	day.append("monday")
	day.append("tuesday")
	day.append("wednesday")
	day.append("thrusday")
	day.append("friday")
	day.append("saturday")
	day.append("sunday")
	return day


def fillTime():
	time=[]
	for i in range(1,13):
		time.append(str(i))
		for j in range(1,60):

			time.append(str(i)+":"+str(j)+"am")
			time.append(str(i)+":"+str(j)+"pm")
			time.append(str(i)+":"+str(j))
			

	return time	



def findTheWord(eventList,checkList):
	global row
	for i in range(row):
		if eventList[i][0] in checkList:
			return True
	
	return False



def isEventIsThere(eventList):
	
	global row
	

	for i in eventList:
		row+=1

	

	for i in range(row):
		if eventList[i][1]=="VBP" or eventList[i][1]=="VBZ" or eventList[i][1]=="VB":
			return True
	
	return False


def isVenueIsThere(eventList):
	global row
	for i in range(row):
		if eventList[i][1]=="NN" or eventList[i][1]=="NNS":
			return True
	
	return False


def fillEvent():
	event=[]
	event.append("meet")
	event.append("gather")
	event.append("assemble")
	event.append("come")
	event.append('wake')
	event.append('remind')
	return event


def analysis(isEventThere,isVenueThere,isDayThere,isTimeThere):
	if isEventThere and isVenueThere:
		return True

	if (isEventThere and isDayThere) or (isEventThere and isTimeThere) or (isEventThere and isVenueThere):
		return True

	
	return False	


#main function

def main(message):
	isDayThere=False
	isVenueThere=False
	isTimeThere=False
	isEventThere=False

	#getting the message

	ps = PorterStemmer()
	#print(message)
	#tokenizing each message
	message_tokens=word_tokenize(message)

	#getting the stop words for english
	stop_words = set(stopwords.words('english'))


	#getting the days and time
	day=fillDays()
	time=fillTime()
	event=fillEvent()


	#print(nltk.pos_tag(message_tokens))

	#filtering the message
	filtered_message = [w for w in message_tokens if not w in stop_words or  not w =="%20"]



	for i in range(len(filtered_message)):
		temp=filtered_message[i]
		filtered_message.remove(filtered_message[i])
		filtered_message.insert(i,ps.stem(temp))

	for i in range(len(filtered_message)):

		if i==len(filtered_message):
			break

		if filtered_message[i] in time:
			isTimeThere=True
			filtered_message.remove(filtered_message[i])

		if i==len(filtered_message):
			break

		if filtered_message[i] in day:
			isDayThere=True
			filtered_message.remove(filtered_message[i])

		if i==len(filtered_message):
			break
		
		
	#tagging the tags
	message_tag=nltk.pos_tag(filtered_message)

	#print(message_tag)
	isEventThere=isEventIsThere(message_tag)
	isVenueThere=isVenueIsThere(message_tag)



	if isEventThere==False and isVenueThere==True:
		
		if findTheWord(message_tag,event):
			isEventThere=True

	#print("Event  "+str(isEventThere))
	#print("Day  "+str(isDayThere))
	#print("Venue  "+str(isVenueThere))
	#print("time  "+str(isTimeThere))

	result=analysis(isEventThere,isVenueThere,isDayThere,isTimeThere)
	if result==True:
		return "Set a reminder"
	else:
		return "Don't set a reminder"
		

print(main(input()))