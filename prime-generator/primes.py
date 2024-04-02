limit = input("To what number do you want to generate primes?: ")
limit = int(limit)

def primes(limit):
	numbers = [i for i in range(2, limit+1)]
	index = 0

	for num in numbers:
		divisor = numbers[index]
		for num in numbers:
			if (num % divisor == 0) and (num != divisor) and (num in numbers):
				numbers.remove(num)
		index += 1

	print(len(numbers))
	return numbers
print(primes(limit))