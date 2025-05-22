# 1. Define your secret and the exact JSON body string
SECRET="mysecretK3y!"
JSON_BODY_STRING='{"message":"Hello, Webhook!","timestamp":1625875200,"user_id":123}'

# 2. Generate the HMAC SHA256 hash and then Base64 encode it
#    - `echo -n "$JSON_BODY_STRING"`: Prints the JSON body string.
#      The `-n` is crucial to prevent a trailing newline, which would alter the hash.
#    - `openssl dgst -sha256 -hmac "$SECRET" -binary`: Computes the HMAC SHA256 hash.
#      - `-sha256`: Specifies the SHA256 algorithm.
#      - `-hmac "$SECRET"`: Specifies the secret key for HMAC.
#      - `-binary`: Outputs the raw binary hash.
#    - `openssl base64`: Encodes the binary input from the pipe into Base64.
#      (On some systems, you might use the `base64` command directly instead of `openssl base64`)

GENERATED_SIGNATURE=$(echo -n "$JSON_BODY_STRING" | openssl dgst -sha256 -hmac "$SECRET" -binary | openssl base64)

# Print the generated signature
echo "$GENERATED_SIGNATURE"