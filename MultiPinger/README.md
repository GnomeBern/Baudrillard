## MultiPinger
    
Multiprocessing ping for testing ifrastructure

_Note: for linux, don't work in windows_
    
``` MultiPinger(host_list, iteration_sleep, ping_timeout, ping_attempts, show_success, show_failed) ```      
Constructor
- *host_list* - list of ip addresses as string
- *iteration_sleep* - pause between ping cycles. Default is 0,5 sec.
- *ping_timeout* - wait ping request. Default is 2 sec
- *ping_attemptts* - count of ping attemptts. Default is 2
- *show_success* - allow print a available hosts. Default is False
- *show_failed* - allow print a unavailable hosts. Default is True

``` start() ```      
Start endless pings

### Before using
You need write ip addresses to devices list. Example:
```
if __name__ == "__main__":
    devices = ['192.168.10.1', '172.22.3.3', '172.22.3.4', '172.22.3.5', '172.22.3.6', '172.22.3.7', '172.22.3.8']
    ...
```

### Using
``` 
./pings.py > ping.log & tail -f ping.log
[1] 14410
08:26:40 14-02-2020 host 172.22.3.3     is down
08:26:40 14-02-2020 host 172.22.3.6     is down
08:26:40 14-02-2020 host 172.22.3.4     is down
... ... ...
kill -9 14410
```      
