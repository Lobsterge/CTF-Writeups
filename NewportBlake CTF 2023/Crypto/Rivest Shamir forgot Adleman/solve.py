from Crypto.Util.number import long_to_bytes
e =  123589168751396275896312856328164328381265978316578963271231567137825613822284638216416
ct =  159269674251793083518243077048685663852794473778188330996147339166703385101217832722333
print(long_to_bytes(ct^e))