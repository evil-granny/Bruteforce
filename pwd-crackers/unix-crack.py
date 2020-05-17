import argparse
import crypt
import threading

from multiprocessing import Pool, Queue

queue = Queue()

def test_pass(user, crypt_pass, dict_words):
    salt = crypt_pass[0:2]
    for word in dict_words:
        crypt_word = crypt.crypt(word, salt)
        if crypt_word.strip() == crypt_pass.strip():
            queue.put('Password for %s is: %s' % (user, word))
            return
    queue.put('Password for %s not found' % user)


class UnixPasswordCracker(object):
    """
    Uses a simple dictionary based brute-force attack to guess a user's
    password by hashing the dictionary word and then checking for equality
    against the existing hash.  
    passwords.txt
    dictionary.txt
    """
    pool = Pool(processes=5)

    def use_threading(self, func, args):
        thread = threading.Thread(target=func, args=args)
        thread.start()
        thread.join()
        
    def use_multithreaded_pools(self, func, args):
        return self.pool.apply_async(func, args)
        
    def main(self, mode=None):
        dictionary = 'dictionary.txt'
        with open(dictionary, 'r') as f:
            dict_words = [line.strip('\n').strip() for line in f.readlines()]
        
        passwords = 'passwords.txt'
        with open(passwords, 'r') as f:
            for line in f.readlines():
                if ":" in line:
                    user = line.split(':')[0]
                    crypt_pass = line.split(':')[1].strip(' ')
                    args = [user, crypt_pass, dict_words]
                    
                    if mode == 'threading':
                        self.use_threading(test_pass, args)
                    elif mode == 'pool':
                        self.use_multithreaded_pools(test_pass, args)
                    else:
                        test_pass(*args)

        self.pool.close()
        self.pool.join()        

        # print the queue items
        while not queue.empty():
            print(queue.get())
        

if __name__ == "__main__":
    mode = None
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", help="Valid choices: 'pool' and 'threading'")
    args = parser.parse_args()
    if args.mode:
        mode = args.mode
    UnixPasswordCracker().main(mode=mode)
