### openssl 로 인증서 패스워드 확인하기 from file 

```
openssl rsa -in secured_ssl.pem -out dec_00_key -passin file:./pass.txt &> /dev/null
```
