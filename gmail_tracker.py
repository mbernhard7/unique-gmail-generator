import os
import sys

def get_local_directory():
	file_directory=str(__file__).split('/') 
	del file_directory[-1:]
	return '/'.join(file_directory)

def dotter(start,rest,emails,needed):
	if len(rest)==1 or 2**len(start.replace(".",""))>=needed:
		emails.append(start+rest)
	else:
		dotter(start+rest[:1],rest[1:],emails,needed)
		dotter(start+rest[:1]+".",rest[1:],emails,needed)

def format_text_block(text):
	out=""
	lines=0
	for word in text.split(" "):
		out+=word+" "
		if (len(out)>lines*45):
			out+="\n"
			lines+=1
	return out
def check_email(email):
	return "@" in email and "gmail.com" in email.split("@")[1] and len(email.split("@")[0])>=2

def print_help():
	print(format_text_block("The purpose of this program is to provide a way to track how companies and individuals use and share your email. Not many people know this, but the use of periods in your gmail is completely arbitrary; no matter where you put the periods, the email will reach the same address. However, when you provide a website, company, or individual with your email, they will include the periods in the email. By giving different entities different 'versions' of the same email using different placement of periods, you can track how determine who shared your email when you get an email from an unknown address, or spam."))
	print("\n")
	print(format_text_block("To use the program, first enter your base email. You can change base emails using option 1. Then, you can generate new combinations of periods for the same email using option 2. Whenever you give someone an email, record which version of your email you used and who you gave it to using option 3. To see who you gave a specific email to, use option 4. To see what email a certain entity was given, use option 5. To delete all records for a base email, use option 6. To save and quit, use option 7."))

def print_options():
	print("1. Switch base email\n2. Generate new emails\n3. Add new use of email\n4. Check uses of email\n5. Check email for use\n6. Delete current base email\n7. Save and Quit")

def delete_base_email(base):
		print(format_text_block("Are you sure you want to delete this base email? Doing so will clear all records."))
		sure=input("Type yes or no and press enter: ")
		if (sure=="yes"):
			try:
				os.remove(get_local_directory()+"/base_emails/"+base.base_email.split("@")[0]+".txt")
				del base
				return intro()
			except OSError:
				pass

def intro():
	print("----------------------------------------")
	email=input("Enter your base gmail address, or type 'help', and press enter: ")
	if (email=="help"):
		print_help()
		return intro()
	else:
		if (not check_email(email)):
			print("Incorrectly formatted email (or not a gmail). Please paste the whole email!")
			return intro()
		else:
			base=Base_Email_Class(email)
			base.get_list_by_base_email()
			print_options()
			base.main_loop()

class Base_Email_Class:
	def __init__(self,base_email):
		self.base_email=base_email
		self.email_uses={}
		self.get_list_by_base_email()

	def get_list_by_base_email(self):
		self.email_uses={}
		if (os.path.isfile(get_local_directory()+"/base_emails/"+self.base_email.split("@")[0]+".txt")):
			rfile=open(get_local_directory()+"/base_emails/"+self.base_email.split("@")[0]+".txt", "r") 
			lines=rfile.readlines()
			rfile.close()
			for line in lines:
				self.email_uses[line.split("*")[0]]=line.split("*")[1].split("&")
		else:
			self.save_list_by_base_email()
	
	def save_list_by_base_email(self):
		if not os.path.exists(get_local_directory()+"/base_emails/"):
			os.makedirs(get_local_directory()+"/base_emails/")
		rfile=open(get_local_directory()+"/base_emails/"+self.base_email.split("@")[0]+".txt", "w+")
		for key in self.email_uses.keys():
			uses=""
			for site in self.email_uses[key]:
				uses+=site+"&"
			rfile.write(key+"*"+uses[:-1])
		rfile.close()

	def generate_addresses(self):
		prefix=self.base_email.split("@")[0]
		suffix=self.base_email.split("@")[1]
		emails=[]
		count=int(input("Enter how many you want: "))
		tomake=count/2
		while len(emails)<count:
			tomake=tomake*2
			dotter("",prefix,emails,tomake)
			if prefix in emails:
				del emails[emails.index(prefix)]
			for key in self.email_uses.keys():
				del emails[emails.index(key.split("@")[0])]
		emails=emails[:count]
		print("Generated "+str(len(emails))+ " emails.")
		for x in range(count):
			print(emails[x]+"@"+suffix)

	def add_new_entry(self):
		email=input("Enter the email that you used: ")
		site=input("Enter who you gave the email to: ")
		if (email not in self.email_uses.keys()):
			self.email_uses[email]=[]
		self.email_uses[email].append(site)
		self.save_list_by_base_email()
		print("Succesfully added "+site+" to list of uses of "+email+".")

	def search_by_email(self):
		email=input("Enter the email you would like to check: ")
		if (email not in self.email_uses.keys()):
			print("This email has not been given out yet.")
		else:
			print("This email has been given to:")
			for site in self.email_uses[email]:
				print("     "+site)

	def search_by_site(self):
		site=input("Enter who you want the email for: ")
		found=False
		for key in self.email_uses.keys():
			for listing in self.email_uses[key]:
				if (site==listing):
					found=True
					print("The email for "+site+" is "+key+".")
					break
		if (not found):
			print("There are no emails associated with this site.")
	

	def main_loop(self):
		print("----------------------------------------\nBase email: "+self.base_email+"\nType help for help, or options to see options.")
		choice=input("Type the number and press enter: ")
		print("----------------------------------------")
		if (choice=="options"):
			print_options()
		elif (choice=="1"):
			self.save_list_by_base_email()
			while True:
				email=input("Type your full gmail and press enter: ")
				if (not check_email(email)):
					print("Incorrectly formatted email (or not a gmail). Please paste the whole email!")
				else:
					self.base_email=email
					print("Succesfully changed to base email "+self.base_email)
					self.get_list_by_base_email()
					break
		elif (choice=="2"):
			self.generate_addresses()
		elif (choice=="3"):
			self.add_new_entry()
		elif (choice=="4"):
			self.search_by_email()
		elif (choice=="5"):
			self.search_by_site()
		elif (choice=="6"):
			return delete_base_email(self)
		elif (choice=="help"):
			print_help()
		elif (choice=="7"):
			self.save_list_by_base_email()
			sys.exit()
		else:
			print(format_text_block("Invalid selection. Next time, type the number of the option you want, and then press enter."))
		return self.main_loop()
		
intro()