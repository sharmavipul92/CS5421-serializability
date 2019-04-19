from subprocess import Popen, PIPE

S = 10
E = 10
P = 2
I = ['READ UNCOMMITTED', 'READ COMMITTED', 'REPEATABLE READ', 'SERIALIZABLE']


process = Popen(['python', 'run_experiments.py', str(S), str(E), str(P), I], stdout=PIPE)
(output, err) = process.communicate()
exit_code = process.wait()

print output

temp1 = output.split("\n")
temp11 = temp1[0].split(" ")[1]
temp12 = temp1[1].split(" ")[1]

print temp11
print temp12