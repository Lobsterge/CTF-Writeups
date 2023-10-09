function clean(input)
	local cleaned = ""
	for i = 1, #input, 2 do
		local pair = input:sub(i, i + 1)
		local num = tonumber(pair)
		num = num % 26 + 65
		cleaned = cleaned .. string.char(num)
	end
	return cleaned
end

function generateOrder()
	local pinSeed = ""
	for i = 1, 20 do
		pinSeed = pinSeed .. i
	end
	return pinSeed
end

print(clean(generateOrder()))