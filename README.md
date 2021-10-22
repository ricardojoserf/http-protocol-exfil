# http-protocol-exfil

## Create listener 

To run the listener use listener.py with one optional argument: the port it will be listening in.

```
python3 listener.py [PORT]
```

Example:

```
python3 listener.py 8080
```


## Send a file

To send a file use sender.py with two mandatory arguments: the file path and the url of the listener; and one optional argument: the name of the file created remotely (if not used, the name of the input file is used).

```
python3 sender.py -u URL -i INPUTFILE [-o OUTPUTFILE]
```

Example:

```
python3 sender.py -i test.zip -u "http://127.0.0.1:8080" -o output_test.zip
```
