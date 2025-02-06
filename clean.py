s = open("test_A_uncov.txt").read().split("\n")[2:-5]
s = [x.split(" ")[0] for x in s]
s = "\n".join(s)
open("test_A_uncov_clean.txt","w").write(s)
print(s)