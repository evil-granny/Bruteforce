import zipfile
from tqdm import tqdm

def main():
	"""
	Zipfile password cracker using a brute-force dictionary attack
	"""
	zipfilename = 'test.zip'
	dictionary = 'dictionary.txt'
	wordlist = "rockyou.txt"

	password = None
	zip_file = zipfile.ZipFile(zipfilename)

	n_words = len(list(open(wordlist, "rb")))
	print("Total passwords to test:", n_words)

	with open(wordlist, "rb") as wordlist:
		for word in tqdm(wordlist, total=n_words, unit="word"):
			try:
				zip_file.extractall(pwd=word.strip())
			except:
				continue
			else:
				print("[+] Password found:", word.decode().strip())
				exit(0)
	print("[!] Password not found, try other wordlist.")

if __name__ == '__main__':
	main()
